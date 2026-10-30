# 🐍 PEÇONHA+ — Prevenção e Informação sobre Animais Peçonhentos

> Web App responsivo voltado à informação científica, prevenção de acidentes e conscientização sobre animais peçonhentos no Brasil. Projeto desenvolvido para o programa **FMU Tech Inovação**.

## 🎯 1. Descrição do Problema e Aderência ao ODS 3

**O Problema de Saúde Pública**
Os acidentes envolvendo animais peçonhentos (como escorpiões, serpentes e aranhas) representam um desafio constante de saúde pública no Brasil. A escassez de dados centralizados e a dispersão de orientações preventivas dificultam o acesso rápido a informações confiáveis em momentos de emergência, atrasando os primeiros socorros.

**Aderência ao Desafio: ODS 3 (Saúde e Bem-Estar)**
O projeto atende diretamente ao Objetivo de Desenvolvimento Sustentável 3 da ONU, focando em:
* Redução de agravos à saúde pública causados por animais peçonhentos.
* Divulgação acessível de protocolos de primeiros socorros.
* Facilitação do acesso a unidades de saúde e soros antiofídicos.

**Bases de Dados Públicas Utilizadas**
* Dados epidemiológicos oficiais do Sistema de Informação de Agravos de Notificação (SINAN / Ministério da Saúde).
* Dados cartográficos e de geolocalização do OpenStreetMap.

## 💡 2. Proposta de Solução Tecnológica

O **PEÇONHA+** reúne recursos de saúde pública e informações científicas em uma única plataforma web (acessível via navegadores móveis e desktop), atuando diretamente na prevenção e na ação rápida pós-acidente.

**Funcionalidades Planejadas**
1. **Mapeamento de Unidades de Saúde**: Localização e busca de pontos de atendimento de saúde e soro antiofídico.
2. **Prevenção e Primeiros Socorros**: Guia de conduta segura em emergências de saúde e esclarecimento de mitos.
3. **Catálogo de Espécies**: Consulta de fotografias, características biológicas e nível de periculosidade toxicológica.
4. **Registro Comunitário de Avistamentos**: Mapeamento participativo de ocorrências para alertar populações locais.

## 🛠️ 3. Arquitetura, Tecnologias e Justificativas

A arquitetura do projeto foi pensada para aplicar os fundamentos de Engenharia de Software e Banco de Dados adquiridos até o 2º semestre de Análise e Desenvolvimento de Sistemas:

* **Prototipagem de Interface**: Figma. Justificativa: Permite rápida ideação, criação de wireframes e colaboração em tempo real entre a equipe.
* **Frontend (Interface Web)**: HTML5, CSS3 e JavaScript. Justificativa: Tecnologias fundamentais e consolidadas para o desenvolvimento de um Web App responsivo, garantindo que o sistema seja acessível por qualquer celular sem a necessidade de instalar aplicativos.
* **Backend / API**: Python + Flask (ou FastAPI). Justificativa: Aproveita o forte domínio da equipe na linguagem Python para a criação de uma API REST leve e eficiente, responsável por gerenciar a lógica de negócios e o fornecimento de dados para o frontend.
* **Banco de Dados**: PostgreSQL (ou SQLite para ambiente de desenvolvimento). Justificativa: Aplicação prática da disciplina de Banco de Dados, utilizando modelagem relacional para gerenciar o catálogo de espécies, registros de usuários e as unidades de saúde.
* **Mapas**: Integração web com OpenStreetMap (via biblioteca Leaflet.js). Justificativa: Solução open-source para renderização de mapas interativos diretamente no navegador utilizando JavaScript.
* **Versionamento**: Git + GitHub. Justificativa: Padrão da indústria para controle de versão, essencial para organizar as entregas colaborativas da equipe.

## 🎨 4. Identidade Visual Inicial

![Guia de Identidade Visual - PEÇONHA+](docs/identidade-visual/Identidade%20visual.png)

* **Logo**: Composição em vetor que integra um escudo de proteção/saúde com a silhueta da fauna peçonhenta e a cruz médica.
* **Paleta de Cores**:
  * **Verde Preservação** (`#15803D`): Conexão com o meio ambiente e biologia das espécies.
  * **Amarelo / Laranja Alerta** (`#F59E0B`): Sinalização de atenção, prevenção e urgência médica.
  * **Cinza / Branco Neutro** (`#F8FAFC`): Fundo de alta legibilidade para leitura de conteúdos de saúde pública.
* **Tipografia**: **Montserrat** para títulos (moderna e impactante) e **Inter** para textos (alta legibilidade em dispositivos móveis).

## ⚡ 5. Pitch Inicial

"O **PEÇONHA+** é uma solução voltada à prevenção de acidentes com animais peçonhentos e orientação ágil em saúde pública no Brasil. Seu diferencial é integrar em um Web App intuitivo a busca por unidades de atendimento de saúde, orientações oficiais de primeiros socorros e catálogo de espécies, focando integralmente na meta do ODS 3 de promover o bem-estar e salvar vidas em momentos de vulnerabilidade."

## 👥 6. Integrantes do Grupo
* Eduardo Prado da Silva
* Daniel dos Santos Bonilho Passiani (https://github.com/danielpassiani)
* Augusto Andrade Silva (https://github.com/augustoandradesilva7-art)
* Letícia Souza Pessoa
* Pedro de Siqueira Torres

*Projeto submetido para a avaliação do Checkpoint 1 — FMU Tech Inovação.*
