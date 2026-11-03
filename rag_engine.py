import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

def fatiar_texto(texto: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    chunks = []
    inicio = 0
    tamanho_total = len(texto)
    while inicio < tamanho_total:
        fim = inicio + chunk_size
        chunk = texto[inicio:fim].strip()
        if chunk:
            chunks.append(chunk)
        inicio += (chunk_size - overlap)
    return chunks

class RAGEngine:
    def __init__(self, db_path: str = "./chroma_db"):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="conhecimento_calcados",
            metadata={"hnsw:space": "cosine"}
        )

    def indexar_documento(self, doc_id: str, texto: str, metadados: dict):
        embedding = self.encoder.encode(texto).tolist()
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[texto],
            metadatas=[metadados]
        )

    def buscar_contexto(self, pergunta: str, n_resultados: int = 4) -> str:
        pergunta_embedding = self.encoder.encode(pergunta).tolist()
        resultados = self.collection.query(
            query_embeddings=[pergunta_embedding],
            n_results=n_resultados
        )
        documentos_recuperados = resultados.get("documents", [[]])[0]
        if not documentos_recuperados:
            return ""
        return "\n\n".join([f"- {doc}" for doc in documentos_recuperados])

def popular_dados_iniciais(rag: RAGEngine):
    # 1. Políticas da loja
    politicas = [
        ("pol_trocas", "Política de Trocas da Pampa Calçados: Troca por tamanho, modelo ou cor em até 30 dias corridos com produto sem uso e nota fiscal. Arrependimento em até 7 dias corridos.", {"tipo": "politica"}),
        ("pol_formas", "Guia de Formas: Forma padrão. Para tênis de corrida e esportivos recomenda-se 1 número maior. Tabela: 25cm=38, 26cm=39, 26.5cm=40, 27.5cm=41, 28cm=42.", {"tipo": "guia"}),
        ("pol_atendimento", "Atendimento Humano: Para finalizar a compra, reservar produto ou falar com um vendedor, orientar o cliente a falar com nosso atendente no WhatsApp (11) 99999-8888.", {"tipo": "contato"})
    ]
    for doc_id, txt, meta in politicas:
        rag.indexar_documento(doc_id, txt, meta)

    # 2. Carrega catálogo do CSV se existir
    csv_path = "estoque_pampa.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            doc_id = f"prod_{row['sku']}"
            texto_produto = (
                f"Marca: {row['marca']} | Categoria: {row['categoria']} | "
                f"Disponibilidade: {row['status']} | Grade: {row['tamanhos_disponiveis']} (2 pares de cada número em estoque)."
            )
            rag.indexar_documento(doc_id, texto_produto, {"tipo": "estoque", "marca": str(row['marca']).lower()})

if __name__ == "__main__":
    print("Atualizando base de conhecimento vetorial com estoque...")
    rag = RAGEngine()
    popular_dados_iniciais(rag)
    print("Base atualizada! Testando busca:")
    print(rag.buscar_contexto("Vocês têm tênis da Olympikus ou Nike tamanho 40?"))