/* PEÇONHA+ · fluxo principal: animal → primeiros socorros → unidade mais próxima */

const estado = {
  grupo: null,     // escorpiao, serpente, ...
  soros: [],       // soros exigidos para a busca
  municipios: [],
  mapa: null,
};

const DESCRICOES = {
  escorpiao: "Picada com dor forte",
  serpente: "Qualquer tipo de cobra",
  aranha: "Marrom, armadeira…",
  lagarta: "Taturana, lagarta com pelos",
  abelha: "Uma ou várias picadas",
  desconhecido: "Não vi o animal",
};

/* ---------- Navegação entre passos ---------- */
function irPara(n) {
  document.querySelectorAll(".passo").forEach((el) => (el.hidden = el.id !== `passo-${n}`));
  document.querySelectorAll(".passos li").forEach((li) => {
    const p = Number(li.dataset.passo);
    li.className = p < n ? "feito" : p === n ? "atual" : "";
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
  const url = new URL(location);
  url.searchParams.set("passo", n);
  if (estado.grupo) url.searchParams.set("animal", estado.grupo);
  history.replaceState(null, "", url);
}

document.querySelectorAll("[data-voltar]").forEach((b) =>
  b.addEventListener("click", () => irPara(Number(b.dataset.voltar)))
);
document.getElementById("recomecar").addEventListener("click", () => {
  estado.grupo = null;
  estado.soros = [];
  document.querySelectorAll(".opcao").forEach((o) => o.setAttribute("aria-pressed", "false"));
  document.getElementById("ir-2").disabled = true;
  document.getElementById("resultado").innerHTML = "";
  irPara(1);
});

/* ---------- Passo 1 ---------- */
const containerOpcoes = document.getElementById("opcoes-animal");
containerOpcoes.innerHTML = Object.entries(GRUPOS)
  .map(([id, g]) => `
    <button class="opcao" data-grupo="${id}" aria-pressed="false">
      <span class="opcao-emoji" aria-hidden="true">${g.emoji}</span>
      <span class="opcao-nome">${g.nome}</span>
      <span class="opcao-desc">${DESCRICOES[id]}</span>
    </button>`)
  .join("");

function selecionarGrupo(grupo) {
  estado.grupo = grupo;
  containerOpcoes.querySelectorAll(".opcao").forEach((o) =>
    o.setAttribute("aria-pressed", String(o.dataset.grupo === grupo))
  );
  document.getElementById("sub-serpente").hidden = grupo !== "serpente";
  document.getElementById("sub-aranha").hidden = grupo !== "aranha";
  document.getElementById("ir-2").disabled = false;
}

containerOpcoes.addEventListener("click", (e) => {
  const op = e.target.closest(".opcao");
  if (op) selecionarGrupo(op.dataset.grupo);
});

function configurarChips(id) {
  const box = document.getElementById(id);
  box.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    box.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
  });
}
configurarChips("opcoes-serpente");
configurarChips("opcoes-aranha");

function soroEspecifico() {
  const box = estado.grupo === "serpente" ? "opcoes-serpente" : estado.grupo === "aranha" ? "opcoes-aranha" : null;
  if (!box) return null;
  return document.querySelector(`#${box} .chip[aria-pressed="true"]`)?.dataset.soro || null;
}

document.getElementById("ir-2").addEventListener("click", async () => {
  irPara(2);
  await carregarPrimeirosSocorros();
});

/* ---------- Passo 2 ---------- */
function lista(itens) {
  return `<ul>${itens.map((i) => `<li><span>${esc(i)}</span></li>`).join("")}</ul>`;
}

async function carregarPrimeirosSocorros() {
  const alvo = document.getElementById("ps-conteudo");
  try {
    const d = await api(`/primeiros-socorros/${estado.grupo}`);
    const especifico = soroEspecifico();
    // Soros necessários para a busca de unidades
    if (especifico) estado.soros = [especifico];
    else if (["escorpiao", "lagarta"].includes(estado.grupo)) estado.soros = d.soros;
    else if (estado.grupo === "serpente") estado.soros = ["botropico", "crotalico"]; // cobertura mais comum
    else if (estado.grupo === "aranha") estado.soros = ["loxoscelico", "foneutrico"];
    else estado.soros = [];

    document.getElementById("ps-titulo").textContent = d.titulo;
    alvo.innerHTML = `
      <div class="bloco bloco-extra"><h3>⚠️ Importante neste caso</h3>${lista(d.extra)}</div>
      <div class="bloco bloco-faca"><h3>✅ O que fazer</h3>${lista(d.faca)}</div>
      <div class="bloco bloco-nao"><h3>🚫 O que NÃO fazer</h3>${lista(d.nao_faca)}</div>
      <div class="bloco bloco-alarme"><h3>🚑 Ligue 192 se aparecer</h3>${lista(d.sinais_alarme)}</div>
      <p class="fonte">Fonte: ${esc(d.fonte)}.</p>`;
  } catch (err) {
    alvo.innerHTML = `<p class="erro">Não foi possível carregar as orientações (${esc(err.message)}). Ligue 192.</p>`;
  }
}

/* ---------- Passo 3 ---------- */
document.getElementById("ir-3").addEventListener("click", () => {
  irPara(3);
  const resumo = document.getElementById("resumo-soro");
  if (estado.soros.length) {
    const nomes = estado.soros.map((s) => SOROS[s].nome).join(" e ");
    resumo.innerHTML = `Mostrando unidades com soro <strong>${esc(nomes)}</strong>, do mais perto para o mais longe.`;
  } else if (estado.grupo === "abelha") {
    resumo.textContent = "Não há soro específico de uso rotineiro: procure o pronto-socorro mais próximo. Abaixo, unidades de referência para acidentes com animais.";
  } else {
    resumo.textContent = "Mostrando as unidades de referência mais próximas. As marcadas em verde têm todos os tipos de soro.";
  }
  carregarMunicipios();
});

async function carregarMunicipios() {
  if (estado.municipios.length) return;
  estado.municipios = await api("/municipios");
  document.getElementById("lista-municipios").innerHTML = estado.municipios
    .map((m) => `<option value="${esc(m.nome)}">`)
    .join("");
}

document.getElementById("municipio").addEventListener("change", (e) => {
  const nome = e.target.value.trim().toLowerCase();
  const m = estado.municipios.find((x) => x.nome.toLowerCase() === nome);
  if (m) buscarProximas(m.latitude, m.longitude, `centro de ${m.nome}`);
});

document.getElementById("usar-localizacao").addEventListener("click", () => {
  const res = document.getElementById("resultado");
  if (!navigator.geolocation) {
    res.innerHTML = `<p class="erro">Seu navegador não permite localização. Escolha a cidade.</p>`;
    return;
  }
  res.innerHTML = `<p class="carregando">Obtendo sua localização…</p>`;
  navigator.geolocation.getCurrentPosition(
    (pos) => buscarProximas(pos.coords.latitude, pos.coords.longitude, "sua localização"),
    () => (res.innerHTML = `<p class="erro">Não foi possível obter a localização. Escolha a cidade no campo acima.</p>`),
    { enableHighAccuracy: true, timeout: 10000 }
  );
});

async function buscarProximas(lat, lon, origem) {
  const res = document.getElementById("resultado");
  res.innerHTML = `<p class="carregando">Buscando unidades…</p>`;
  try {
    const params = new URLSearchParams({ lat, lon, limite: 5 });
    if (estado.soros.length) params.set("soro", estado.soros.join(","));
    const unidades = await api(`/unidades/proximas?${params}`);
    if (!unidades.length) {
      res.innerHTML = `<p class="erro">Nenhuma unidade encontrada com esse soro. Ligue 192.</p>`;
      return;
    }
    const maisPerto = unidades[0];
    res.innerHTML = `
      <div id="mapa-emergencia" class="mapa mapa-pequeno"></div>
      <p class="fonte">Distâncias em linha reta a partir de ${esc(origem)}. A posição das unidades é aproximada (centro do município ou bairro).</p>
      <h2 style="margin-top:20px">Mais perto: ${esc(maisPerto.municipio)} · ${maisPerto.distancia_km.toLocaleString("pt-BR")} km</h2>
      <div class="lista-unidades">${unidades.map((u) => cardUnidade(u, estado.soros)).join("")}</div>
      <p class="aviso" style="margin-top:16px">Ligue antes para confirmar a disponibilidade do soro. Dados: lista oficial de hospitais de referência do Ministério da Saúde.</p>`;
    desenharMapa(lat, lon, unidades);
  } catch (err) {
    res.innerHTML = `<p class="erro">Erro ao buscar unidades (${esc(err.message)}). Ligue 192.</p>`;
  }
}

function desenharMapa(lat, lon, unidades) {
  if (estado.mapa) estado.mapa.remove();
  estado.mapa = novoMapa("mapa-emergencia", [lat, lon], 10);
  const pontos = [[lat, lon]];
  L.marker([lat, lon], {
    icon: L.divIcon({ className: "", html: '<span class="pino-voce"></span>', iconSize: [18, 18], iconAnchor: [9, 9] }),
  }).addTo(estado.mapa).bindPopup("Você está aqui");
  unidades.forEach((u) => {
    L.marker([u.latitude, u.longitude], { icon: iconeUnidade(u.soros.length >= 7) })
      .addTo(estado.mapa)
      .bindPopup(popupUnidade(u));
    pontos.push([u.latitude, u.longitude]);
  });
  estado.mapa.fitBounds(pontos, { padding: [30, 30], maxZoom: 13 });
}

/* ---------- Estado inicial pela URL (permite compartilhar o link) ---------- */
const inicial = new URLSearchParams(location.search).get("animal");
if (inicial && GRUPOS[inicial]) selecionarGrupo(inicial);
irPara(1);
