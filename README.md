# 🐍 PEÇONHA+ — Prevenção e Informação sobre Animais Peçonhentos

> Aplicativo móvel voltado à informação científica, prevenção de acidentes e conscientização sobre animais peçonhentos no Brasil. Projeto desenvolvido para o programa **FMU Tech Inovação**.

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

O **PEÇONHA+** reúne recursos de saúde pública e informações científicas em uma única plataforma, atuando diretamente na prevenção e na ação rápida pós-acidente.

**Funcionalidades Planejadas**
1. **Mapeamento de Unidades de Saúde**: Localização e busca de pontos de atendimento de saúde e soro antiofídico.
2. **Prevenção e Primeiros Socorros**: Guia de conduta segura em emergências de saúde e esclarecimento de mitos.
3. **Catálogo de Espécies**: Consulta de fotografias, características biológicas e nível de periculosidade toxicológica.
4. **Registro Comunitário de Avistamentos**: Mapeamento participativo de ocorrências para alertar populações locais.
5. **Identificação Assistida por IA (Perspectiva Futura)**: Auxílio na triagem inicial do animal por imagem, acelerando a decisão clínica e a busca por socorro adequado.

## 🛠️ 3. Arquitetura, Tecnologias e Justificativas

* **Prototipagem de Interface**: Figma. Justificativa: Permite rápida ideação, criação de componentes reutilizáveis e colaboração em tempo real entre o grupo.
* **Desenvolvimento Mobile**: React Native + TypeScript. Justificativa: Possibilita a criação de um aplicativo multiplataforma (iOS e Android) com uma base de código única, enquanto o TypeScript garante tipagem estática, reduzindo bugs durante o desenvolvimento.
* **API / Backend**: Python + FastAPI. Justificativa: Python oferece excelente suporte para manipulação de dados, e o FastAPI garante alta performance nas requisições do app, além de gerar documentação automática (Swagger) para facilitar a integração.
* **Banco de Dados & Geoprocessamento**: PostgreSQL + PostGIS. Justificativa: Robustez para armazenar dados relacionais e suporte nativo essencial (PostGIS) para as queries de geolocalização do mapa de avistamentos e postos de saúde.
* **Mapas**: OpenStreetMap. Justificativa: Alternativa open-source e gratuita com dados cartográficos confiáveis para a base do mapa interativo.
* **Versionamento**: Git + GitHub. Justificativa: Padrão de mercado para controle de versão e colaboração em equipe.

## 🎨 4. Identidade Visual Inicial

* **Logo**: Disponibilizado na pasta `docs/identidade-visual/` deste repositório.
* **Paleta de Cores**:
  * **Verde Preservação**: Conexão com o meio ambiente e biologia das espécies.
  * **Amarelo / Laranja Alerta**: Sinalização de atenção, prevenção e urgência médica.
  * **Cinza / Branco Neutro**: Fundo de alta legibilidade para leitura de conteúdos de saúde pública.
* **Tipografia**: Fontes do tipo Sans-serif (ex.: Inter / Roboto) voltadas à boa usabilidade e leitura em telas móveis.

## ⚡ 5. Pitch Inicial

"O **PEÇONHA+** é uma solução voltada à prevenção de acidentes com animais peçonhentos e orientação ágil em saúde pública no Brasil. Seu diferencial é integrar em uma única plataforma intuitiva a busca por unidades de atendimento de saúde, orientações oficiais de primeiros socorros e catálogo de espécies, focando integralmente na meta do ODS 3 de promover o bem-estar e salvar vidas em momentos de vulnerabilidade."

## 👥 6. Integrantes do Grupo
* Eduardo Prado da Silva
* Daniel dos Santos Bonilho Passiani
* Augusto Andrade Silva
* Letícia Souza Pessoa
* Pedro de Siqueira Torres

*Projeto submetido para a avaliação do Checkpoint 1 — FMU Tech Inovação.*
