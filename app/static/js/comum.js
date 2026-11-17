/* PEÇONHA+ · utilitários compartilhados */

const SOROS = {
  botropico:    { nome: "Botrópico",    animal: "Jararaca" },
  crotalico:    { nome: "Crotálico",    animal: "Cascavel" },
  elapidico:    { nome: "Elapídico",    animal: "Coral" },
  laquetico:    { nome: "Laquético",    animal: "Surucucu" },
  escorpionico: { nome: "Escorpiônico", animal: "Escorpião" },
  loxoscelico:  { nome: "Loxoscélico",  animal: "Aranha-marrom" },
  foneutrico:   { nome: "Fonêutrico",   animal: "Armadeira" },
  lonomico:     { nome: "Lonômico",     animal: "Taturana" },
};

const GRUPOS = {
  escorpiao:    { nome: "Escorpião",     emoji: "🦂" },
  serpente:     { nome: "Cobra",         emoji: "🐍" },
  aranha:       { nome: "Aranha",        emoji: "🕷️" },
  lagarta:      { nome: "Lagarta",       emoji: "🐛" },
  abelha:       { nome: "Abelha / vespa", emoji: "🐝" },
  desconhecido: { nome: "Não sei",       emoji: "❓" },
};

const PERIGO = { alto: "Perigo alto", medio: "Perigo médio", baixo: "Perigo baixo" };

async function api(caminho) {
  const resp = await fetch(`/api${caminho}`);
  if (!resp.ok) {
    const corpo = await resp.json().catch(() => ({}));
    throw new Error(corpo.erro || `Erro ${resp.status}`);
  }
  return resp.json();
}

function esc(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

function telLink(telefone) {
  if (!telefone) return "";
  const primeiro = telefone.split("/")[0];
  return "tel:" + primeiro.replace(/[^\d]/g, "");
}

function rotaLink(u) {
  const destino = encodeURIComponent(`${u.nome}, ${u.endereco || ""}, ${u.municipio} - SP`);
  return `https://www.google.com/maps/search/?api=1&query=${destino}`;
}

function soroBadges(codigos, destaque = []) {
  return codigos
    .map((c) => `<span class="badge ${destaque.includes(c) ? "badge-destaque" : ""}" title="${esc(SOROS[c]?.animal)}">${esc(SOROS[c]?.nome || c)}</span>`)
    .join("");
}

function cardUnidade(u, destaque = []) {
  const dist = u.distancia_km != null ? `<span class="distancia">${u.distancia_km.toLocaleString("pt-BR")} km</span>` : "";
  return `
    <article class="card-unidade">
      <div class="card-unidade-topo">
        <div>
          <h3>${esc(u.nome)}</h3>
          <p class="muted">${esc(u.endereco || "")} · ${esc(u.municipio)}</p>
        </div>
        ${dist}
      </div>
      <div class="badges">${soroBadges(u.soros, destaque)}</div>
      <div class="card-unidade-acoes">
        ${u.telefone ? `<a class="btn btn-verde btn-sm" href="${telLink(u.telefone)}">📞 Ligar ${esc(u.telefone.split("/")[0])}</a>` : ""}
        <a class="btn btn-contorno btn-sm" href="${rotaLink(u)}" target="_blank" rel="noopener">🧭 Como chegar</a>
      </div>
    </article>`;
}

/* Ícone de marcador no mapa com as cores da marca */
function iconeUnidade(completa) {
  return L.divIcon({
    className: "",
    html: `<span class="pino ${completa ? "pino-completo" : ""}"></span>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
    popupAnchor: [0, -10],
  });
}

function popupUnidade(u) {
  return `<strong>${esc(u.nome)}</strong><br>${esc(u.municipio)}<br>
    <small>${u.soros.map((s) => SOROS[s].nome).join(", ")}</small><br>
    ${u.telefone ? `<a href="${telLink(u.telefone)}">${esc(u.telefone)}</a> · ` : ""}
    <a href="${rotaLink(u)}" target="_blank" rel="noopener">Como chegar</a>`;
}

function novoMapa(id, centro = [-22.4, -48.6], zoom = 6) {
  const mapa = L.map(id, { scrollWheelZoom: false }).setView(centro, zoom);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(mapa);
  return mapa;
}
