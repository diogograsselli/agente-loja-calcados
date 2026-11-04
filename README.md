# 👟 Agente Inteligente Passo Certo — Pampa Calçados

Agente de atendimento ao cliente para e-commerce e lojas de calçados, desenvolvido com arquitetura RAG Vetorial (ChromaDB + SentenceTransformers), orquestração via Azure AI Foundry, persistência relacional com SQLAlchemy e interface interativa em Streamlit.

---

## 🎯 Objetivo do Projeto
Resolver os principais gargalos de atendimento no varejo de calçados:
- Dúvidas recorrentes sobre tabela de medidas e formas (+1 número para corrida).
- Consulta rápida de marcas e disponibilidade de estoque.
- Transbordo inteligente com direcionamento para fechamento de venda via WhatsApp.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Frontend / Interface:** Streamlit
- **LLM & Nuvem:** Azure AI Foundry (Azure OpenAI)
- **Banco Vetorial (RAG):** ChromaDB + SentenceTransformers (`all-MiniLM-L6-v2`)
- **Persistência Relacional:** SQLAlchemy (SQLite para histórico de conversas)
- **Manipulação de Dados:** Pandas
- **Resiliência:** Tenacity (tratamento de retries e rate limits)

---

## 📐 Engenharia de Prompt (Framework COSTAR)
O agente foi construído utilizando a metodologia COSTAR:
- **Context:** Atendente especialista em calçados com acesso a RAG local.
- **Objective:** Sanar dúvidas técnicas de produto e direcionar a conversão.
- **Style:** Consultivo e dinâmico.
- **Tone:** Empático e prestativo.
- **Audience:** Clientes finais de calçados e vestuário.
- **Response:** Respostas curtas, com formatação clara e botões de ação/contato.

---

## 🚀 Como Executar o Projeto Localmente

1. **Clone o repositório:**
```bash
git clone [https://github.com/diogograsselli/agente-loja-calcados.git](https://github.com/diogograsselli/agente-loja-calcados.git)
cd agente-loja-calcados
