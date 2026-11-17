/* PEÇONHA+ · catálogo de espécies */

let especies = [];
let grupoAtivo = "";

const filtros = document.getElementById("filtros-grupo");
filtros.insertAdjacentHTML(
  "beforeend",
  Object.entries(GRUPOS)
    .filter(([id]) => id !== "desconhecido")
    .map(([id, g]) => `<button class="chip" data-grupo="${id}" aria-pressed="false">${g.emoji} ${g.nome}</button>`)
    .join("")
);
filtros.addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  grupoAtivo = chip.dataset.grupo;
  filtros.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
  render();
});

function render() {
  const lista = especies.filter((e) => !grupoAtivo || e.grupo === grupoAtivo);
  document.getElementById("lista-especies").innerHTML = lista
    .map(
      (e) => `
      <button class="card card-link card-especie" data-id="${e.id}">
        <span class="emoji" aria-hidden="true">${GRUPOS[e.grupo].emoji}</span>
        <h3>${esc(e.nome)}</h3>
        <p class="cientifico">${esc(e.cientifico)}</p>
        <div class="badges"><span class="badge badge-perigo-${e.perigo}">${PERIGO[e.perigo]}</span>
          ${e.soros.length ? soroBadges(e.soros) : '<span class="badge">Sem soro específico</span>'}</div>
      </button>`
    )
    .join("");
}

document.getElementById("lista-especies").addEventListener("click", (ev) => {
  const card = ev.target.closest(".card-especie");
  if (!card) return;
  abrir(especies.find((e) => e.id === card.dataset.id));
});

function abrir(e) {
  document.getElementById("modal-titulo").textContent = `${GRUPOS[e.grupo].emoji} ${e.nome}`;
  document.getElementById("modal-cientifico").textContent = e.cientifico;
  const soroTxt = e.soros.length
    ? `Soro ${e.soros.map((s) => SOROS[s].nome).join(", ")}`
    : "Não há soro específico de uso rotineiro";
  document.getElementById("modal-corpo").innerHTML = `
    <div class="badges"><span class="badge badge-perigo-${e.perigo}">${PERIGO[e.perigo]}</span><span class="badge badge-destaque">${esc(soroTxt)}</span></div>
    <h3>Como reconhecer</h3><p>${esc(e.descricao)}</p>
    <h3>Onde vive</h3><p>${esc(e.habitat)}</p>
    <h3>Sintomas da picada</h3><p>${esc(e.sintomas)}</p>
    <h3>Como prevenir</h3><p>${esc(e.prevencao)}</p>
    <div class="card-unidade-acoes" style="margin-top:16px">
      <a class="btn btn-alerta" href="/emergencia?animal=${e.grupo}">Fui picado por este animal</a>
      ${e.soros.length ? `<a class="btn btn-contorno" href="/mapa">Onde tem soro</a>` : ""}
    </div>`;
  document.getElementById("modal-especie").showModal();
}

document.getElementById("modal-especie").addEventListener("click", (e) => {
  if (e.target.tagName === "DIALOG") e.target.close(); // clique fora fecha
});

api("/especies")
  .then((d) => {
    especies = d;
    render();
  })
  .catch((err) => {
    document.getElementById("lista-especies").innerHTML = `<p class="erro">Erro: ${esc(err.message)}</p>`;
  });
