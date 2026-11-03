import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
import openai
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from prompts import SYSTEM_PROMPT
from rag_engine import RAGEngine, popular_dados_iniciais
from database import salvar_mensagem, carregar_historico_recente

# 1. Carregamento de variáveis de ambiente
load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# 2. Configuração da página Streamlit
st.set_page_config(
    page_title="Agente RAG | Pampa Calçados",
    page_icon="👟",
    layout="wide"
)

st.title("👟 Agente Inteligente de Atendimento — Pampa Calçados")
st.caption("Arquitetura RAG Vetorial (ChromaDB + SentenceTransformers) orquestrada com Azure OpenAI e SQLAlchemy.")

# 3. Inicialização dos recursos partilhados (Cache)
@st.cache_resource
def iniciar_recursos():
    cliente = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    motor_rag = RAGEngine()
    popular_dados_iniciais(motor_rag)
    return cliente, motor_rag

cliente_azure, motor_rag = iniciar_recursos()

# 4. Gestão da Sessão do Utilizador
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

# 5. Função de chamada resiliente à API Azure OpenAI
@retry(
    retry=retry_if_exception_type((openai.RateLimitError, openai.APIConnectionError)),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    stop=stop_after_attempt(3)
)
def gerar_resposta_resiliente(mensagens_payload):
    return cliente_azure.chat.completions.create(
        model=deployment_name,
        messages=mensagens_payload,
        max_completion_tokens=400,
    )

# 6. Carregar histórico do banco relacional para a sessão do Streamlit
if "chat_history" not in st.session_state:
    historico_banco = carregar_historico_recente(st.session_state.session_id, limite=10)
    if historico_banco:
        st.session_state.chat_history = historico_banco
    else:
        mensagem_boas_vindas = "Olá! Seja bem-vindo à Pampa Calçados. 👟 Em que posso ajudar hoje? (Dúvidas sobre tamanhos, trocas ou calçado desportivo?)"
        st.session_state.chat_history = [{"role": "assistant", "content": mensagem_boas_vindas}]
        salvar_mensagem(st.session_state.session_id, "assistant", mensagem_boas_vindas)

# 7. Exibição do histórico de mensagens na interface
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 8. Entrada de nova mensagem do utilizador
if prompt := st.chat_input("Coloque a sua dúvida sobre produtos, tamanhos ou trocas..."):
    # Exibe e persiste a mensagem do utilizador
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    salvar_mensagem(st.session_state.session_id, "user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Execução do RAG: Recuperação semântica no ChromaDB
    with st.spinner("A consultar base de conhecimento vetorial e a processar resposta..."):
        contexto_recuperado = motor_rag.buscar_contexto(prompt, n_resultados=2)
        
        # Montagem do Payload aumentado com RAG
        instrucao_sistema = f"{SYSTEM_PROMPT}\n\n### CONTEXTO DE SUPORTE RECUPERADO (RAG):\n{contexto_recuperado}"
        
        payload = [{"role": "system", "content": instrucao_sistema}]
        
        # Adiciona histórico recente para manter a coerência
        for h in st.session_state.chat_history[-4:]:
            payload.append({"role": h["role"], "content": h["content"]})

        try:
            resposta_api = gerar_resposta_resiliente(payload)
            conteudo_resposta = resposta_api.choices[0].message.content
            
            # Exibe a resposta do assistente
            with st.chat_message("assistant"):
                st.markdown(conteudo_resposta)
                
                # Exibição transparente do contexto RAG para fins de demonstração técnica
                if contexto_recuperado:
                    with st.expander("🔍 Detalhes da Recuperação Semântica (ChromaDB)"):
                        st.info(contexto_recuperado)

            # Persiste no histórico local e no SQLite
            st.session_state.chat_history.append({"role": "assistant", "content": conteudo_resposta})
            salvar_mensagem(st.session_state.session_id, "assistant", conteudo_resposta)

        except Exception as e:
            st.error(f"Erro na comunicação com a API Azure OpenAI: {e}")