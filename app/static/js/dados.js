/* PEÇONHA+ · painel de dados (Sinan 2023) */

const VERDE = "#15803D";
const LARANJA = "#F59E0B";
const CINZA = "#CBD5E1";
const fmt = (n) => n.toLocaleString("pt-BR");

Chart.defaults.font.family = "Inter, system-ui, sans-serif";
Chart.defaults.color = "#4B5563";
Chart.defaults.plugins.legend.display = false;
Chart.defaults.maintainAspectRatio = false;

api("/estatisticas").then((d) => {
  const e = d.escorpiao;

  document.getElementById("kpis").innerHTML = `
    <div class="kpi"><div class="kpi-valor">${fmt(e.casos)}</div><div class="kpi-rotulo">acidentes com escorpião em ${d.ano}</div></div>
    <div class="kpi"><div class="kpi-valor">${fmt(e.obitos_sinan)}</div><div class="kpi-rotulo">óbitos notificados no Sinan</div></div>
    <div class="kpi"><div class="kpi-valor laranja">${fmt(e.casos_mes_pico)}</div><div class="kpi-rotulo">casos em ${e.mes_pico.toLowerCase()}, o mês de pico</div></div>
    <div class="kpi"><div class="kpi-valor">${d.rede_sp.unidades}</div><div class="kpi-rotulo">unidades com soro em ${d.rede_sp.municipios_atendidos} cidades de SP no app</div></div>`;

  // Casos por UF, ordenado, SP em destaque
  const ufs = [...e.por_uf].sort((a, b) => b.casos - a.casos);
  new Chart(document.getElementById("g-uf"), {
    type: "bar",
    data: {
      labels: ufs.map((u) => u.uf),
      datasets: [{ data: ufs.map((u) => u.casos), backgroundColor: ufs.map((u) => (u.uf === "SP" ? LARANJA : VERDE)), borderRadius: 4 }],
    },
    options: {
      indexAxis: "y",
      scales: { x: { grid: { color: "#F1F5F9" }, ticks: { callback: (v) => fmt(v) } }, y: { grid: { display: false }, ticks: { autoSkip: false, font: { size: 11 } } } },
      plugins: {
        tooltip: {
          callbacks: {
            title: (i) => ufs[i[0].dataIndex].nome,
            label: (i) => {
              const u = ufs[i.dataIndex];
              return [`${fmt(u.casos)} casos`, `${u.incidencia.toLocaleString("pt-BR")} por 100 mil hab.`, `${u.obitos} óbitos`];
            },
          },
        },
      },
    },
  });

  // Letalidade por faixa etária
  new Chart(document.getElementById("g-idade"), {
    type: "bar",
    data: {
      labels: e.faixa_etaria.map((f) => f.faixa),
      datasets: [{ data: e.faixa_etaria.map((f) => f.letalidade), backgroundColor: e.faixa_etaria.map((f) => (f.faixa === "0–9" ? LARANJA : VERDE)), borderRadius: 4 }],
    },
    options: {
      scales: { y: { title: { display: true, text: "Letalidade (%)" }, grid: { color: "#F1F5F9" } }, x: { grid: { display: false }, title: { display: true, text: "Idade (anos)" } } },
      plugins: { tooltip: { callbacks: { label: (i) => { const f = e.faixa_etaria[i.dataIndex]; return [`Letalidade: ${f.letalidade.toLocaleString("pt-BR")}%`, `${fmt(f.casos)} casos · ${f.obitos} óbitos`]; } } } },
    },
  });

  // Local da picada
  const locais = Object.entries(e.local_picada).filter(([k]) => k !== "Ignorado");
  new Chart(document.getElementById("g-local"), {
    type: "bar",
    data: {
      labels: locais.map(([k]) => k),
      datasets: [{ data: locais.map(([, v]) => v), backgroundColor: locais.map(([k]) => (["Mãos", "Pés"].includes(k) ? VERDE : CINZA)), borderRadius: 4 }],
    },
    options: {
      indexAxis: "y",
      scales: { x: { ticks: { callback: (v) => v + "%" }, grid: { color: "#F1F5F9" } }, y: { grid: { display: false } } },
      plugins: { tooltip: { callbacks: { label: (i) => `${i.raw.toLocaleString("pt-BR")}% dos casos` } } },
    },
  });

  // Rede de soros
  const soros = d.rede_sp.por_soro;
  new Chart(document.getElementById("g-soro"), {
    type: "bar",
    data: { labels: soros.map((s) => s.nome), datasets: [{ data: soros.map((s) => s.unidades), backgroundColor: VERDE, borderRadius: 4 }] },
    options: {
      scales: { y: { title: { display: true, text: "Unidades" }, grid: { color: "#F1F5F9" }, ticks: { precision: 0 } }, x: { grid: { display: false } } },
      plugins: { tooltip: { callbacks: { label: (i) => `${i.raw} unidades` } } },
    },
  });

  document.getElementById("fonte").innerHTML = `Fonte: <a href="${d.fonte_url}" target="_blank" rel="noopener">${esc(d.fonte)}</a>. Rede de soros: lista oficial de hospitais de referência do Ministério da Saúde (estado de SP).`;
});
