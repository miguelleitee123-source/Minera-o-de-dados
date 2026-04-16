# 📡 BGP Analytics - Monitoramento de Prefixos em Tempo Real

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Framework-lightgrey?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge" alt="Status">
</p>

## 🎯 Sobre o Projeto

O **BGP Analytics** é uma ferramenta de monitoramento e mineração de dados para redes, focada na análise de prefixos BGP através do Looking Glass do IX.br. O sistema detecta automaticamente mudanças de rota, saltos de rede (AS Path) e identifica se o tráfego está sob mitigação de ataques DDoS.

Este projeto foi desenvolvido para simplificar a visualização técnica de roteamento BGP, transformando logs brutos de Telnet em um dashboard visual, intuitivo e moderno.

---

## 🚀 Funcionalidades

- [x] **Mineração Automatizada**: Coleta periódica via Telnet (IX.br).
- [x] **Análise de Status**: Identificação de mitigadores (UPX, Huge Networks, etc).
- [x] **Dashboard Real-time**: Visualização no navegador com atualização automática.
- [x] **Persistence**: Histórico completo armazenado em banco de dados SQLite.
- [x] **Análise de Saltos**: Contagem e rastreio de saltos no AS Path.

---

## 🛠️ Stack Tecnológica

O projeto utiliza o que há de mais prático e moderno para scripts de infraestrutura e dashboards web:

| Camada | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Backend** | `Python 3` | Lógica de mineração, Regex e Telnet. |
| **API/Server** | `Flask` | Servidor web leve para disponibilizar os dados. |
| **Banco de Dados** | `SQLite` | Armazenamento local rápido e eficiente. |
| **Frontend** | `HTML5 / CSS3` | Interface responsiva com Dark Mode e glassmorphism. |
| **Gráficos** | `Chart.js` | Visualização dinâmica de métricas de rede. |

---

## 📐 Arquitetura

O sistema é dividido em dois motores principais que funcionam de forma independente:

1.  **Motor de Coleta (`webscrapping.py`)**: O "trabalhador" que consulta o Looking Glass e alimenta o banco de dados.
2.  **Motor de Visualização (`dashboard_server.py`)**: A interface que expõe os dados para o usuário final no `localhost:5000`.

---

## 🔧 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/bgp-analytics.git
    ```

2.  **Instale as dependências:**
    ```bash
    pip install flask
    ```

3.  **Inicie a coleta de dados:**
    ```bash
    python webscrapping.py
    ```

4.  **Ligue o Dashboard:**
    ```bash
    python dashboard_server.py
    ```

5.  **Acesse:** `http://localhost:5000`

---

<p align="center">
  Desenvolvido com ❤️ para a Faculdade e para a Comunidade de Redes.
</p>
