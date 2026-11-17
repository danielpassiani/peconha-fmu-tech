// PEÇONHA+ - Busca das unidades de saúde mais próximas

const resultado = document.getElementById("resultado");
const grupo = resultado.dataset.grupo;
let mapa = null;

// Botão "Usar minha localização"
document.getElementById("botao-localizacao").addEventListener("click", function () {
  if (!navigator.geolocation) {
    resultado.innerHTML = '<p class="erro">Seu navegador não permite localização. Escolha a cidade.</p>';
    return;
  }
  resultado.innerHTML = '<p class="carregando">Obtendo sua localização...</p>';
  navigator.geolocation.getCurrentPosition(
    function (posicao) {
      buscarUnidades(posicao.coords.latitude, posicao.coords.longitude);
    },
    function () {
      resultado.innerHTML = '<p class="erro">Não foi possível obter a localização. Escolha a cidade na lista.</p>';
    }
  );
});

// Lista de cidades
document.getElementById("cidade").addEventListener("change", function () {
  if (this.value === "") return;
  const partes = this.value.split(",");
  buscarUnidades(partes[0], partes[1]);
});

// Chama a API do Flask e mostra o resultado
function buscarUnidades(lat, lon) {
  resultado.innerHTML = '<p class="carregando">Buscando unidades...</p>';

  fetch("/api/unidades/proximas?lat=" + lat + "&lon=" + lon + "&grupo=" + grupo)
    .then(function (resposta) {
      return resposta.json();
    })
    .then(function (unidades) {
      if (unidades.length === 0) {
        resultado.innerHTML = '<p class="erro">Nenhuma unidade encontrada. Ligue 192.</p>';
        return;
      }
      mostrarUnidades(unidades);
      mostrarMapa(lat, lon, unidades);
    })
    .catch(function () {
      resultado.innerHTML = '<p class="erro">Erro ao buscar as unidades. Ligue 192.</p>';
    });
}

function mostrarUnidades(unidades) {
  let html = '<div id="mapa-atendimento" class="mapa mapa-pequeno"></div>';
  html += '<p class="fonte">Distância em linha reta. A posição das unidades no mapa é aproximada.</p>';

  for (const u of unidades) {
    const telefone = u.telefone ? u.telefone.split("/")[0] : "";
    const rota = "https://www.google.com/maps/search/?api=1&query=" +
      encodeURIComponent(u.nome + ", " + u.endereco + ", " + u.municipio + " - SP");

    let badges = "";
    for (const s of u.soros) {
      badges += '<span class="badge">' + SOROS[s].nome + "</span>";
    }

    html += `
      <article class="card-unidade">
        <div class="card-unidade-topo">
          <div>
            <h3>${u.nome}</h3>
            <p class="muted">${u.endereco} · ${u.municipio}</p>
          </div>
          <span class="distancia">${u.distancia_km} km</span>
        </div>
        <div class="badges">${badges}</div>
        <div class="card-unidade-acoes">
          ${telefone ? `<a class="btn btn-verde btn-sm" href="tel:${telefone.replace(/\D/g, "")}">📞 Ligar ${telefone}</a>` : ""}
          <a class="btn btn-contorno btn-sm" href="${rota}" target="_blank">🧭 Como chegar</a>
        </div>
      </article>`;
  }

  html += '<p class="aviso">Ligue antes para confirmar se o soro está disponível.</p>';
  resultado.innerHTML = html;
}

function mostrarMapa(lat, lon, unidades) {
  mapa = L.map("mapa-atendimento").setView([lat, lon], 10);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap",
  }).addTo(mapa);

  // você
  L.circleMarker([lat, lon], { radius: 9, color: "#fff", weight: 3, fillColor: "#2563EB", fillOpacity: 1 })
    .addTo(mapa)
    .bindPopup("Você está aqui");

  // unidades
  const pontos = [[lat, lon]];
  for (const u of unidades) {
    L.circleMarker([u.latitude, u.longitude], { radius: 9, color: "#fff", weight: 3, fillColor: "#15803D", fillOpacity: 1 })
      .addTo(mapa)
      .bindPopup("<strong>" + u.nome + "</strong><br>" + u.municipio);
    pontos.push([u.latitude, u.longitude]);
  }
  mapa.fitBounds(pontos, { padding: [30, 30] });
}
