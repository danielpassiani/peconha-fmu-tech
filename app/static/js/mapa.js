/* PEÇONHA+ · mapa de unidades com soro */

const mapa = novoMapa("mapa");
const camada = L.layerGroup().addTo(mapa);
let todas = [];
let soroAtivo = "";

const filtros = document.getElementById("filtros-soro");
filtros.insertAdjacentHTML(
  "beforeend",
  Object.entries(SOROS)
    .map(([c, s]) => `<button class="chip" data-soro="${c}" aria-pressed="false" title="${s.animal}">${s.nome} · ${s.animal}</button>`)
    .join("")
);

filtros.addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  soroAtivo = chip.dataset.soro;
  filtros.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
  render();
});

document.getElementById("busca").addEventListener("input", render);

function normalizar(t) {
  return t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

function render() {
  const termo = normalizar(document.getElementById("busca").value.trim());
  const visiveis = todas.filter(
    (u) =>
      (!soroAtivo || u.soros.includes(soroAtivo)) &&
      (!termo || normalizar(`${u.municipio} ${u.nome}`).includes(termo))
  );

  camada.clearLayers();
  visiveis.forEach((u) =>
    L.marker([u.latitude, u.longitude], { icon: iconeUnidade(u.soros.length >= 7) })
      .bindPopup(popupUnidade(u))
      .addTo(camada)
  );
  if (visiveis.length && termo) {
    mapa.fitBounds(visiveis.map((u) => [u.latitude, u.longitude]), { padding: [40, 40], maxZoom: 12 });
  }

  document.getElementById("contador").textContent = `${visiveis.length} de ${todas.length} unidades`;
  document.getElementById("lista").innerHTML = visiveis.length
    ? visiveis.map((u) => cardUnidade(u, soroAtivo ? [soroAtivo] : [])).join("")
    : `<p class="muted">Nenhuma unidade encontrada com esses filtros.</p>`;
}

api("/unidades")
  .then((dados) => {
    todas = dados;
    render();
  })
  .catch((err) => {
    document.getElementById("lista").innerHTML = `<p class="erro">Erro ao carregar unidades: ${esc(err.message)}</p>`;
  });
