import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///historico.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HistoricoMensagem(Base):
    __tablename__ = "historico_mensagens"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), index=True)
    role = Column(String(20)) # 'user' ou 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Cria as tabelas na base de dados SQLite
Base.metadata.create_all(bind=engine)

def salvar_mensagem(session_id: str, role: str, content: str):
    """Guarda uma mensagem na base de dados relacional."""
    db = SessionLocal()
    try:
        nova_msg = HistoricoMensagem(session_id=session_id, role=role, content=content)
        db.add(nova_msg)
        db.commit()
    finally:
        db.close()

def carregar_historico_recente(session_id: str, limite: int = 6):
    """Recupera as últimas mensagens ordenadas cronologicamente."""
    db = SessionLocal()
    try:
        mensagens = (
            db.query(HistoricoMensagem)
            .filter(HistoricoMensagem.session_id == session_id)
            .order_by(HistoricoMensagem.timestamp.desc())
            .limit(limite)
            .all()
        )
        # Inverte para manter a ordem cronológica correta (mais antiga para a mais recente)
        mensagens_ordenadas = mensagens[::-1]
        return [{"role": m.role, "content": m.content} for m in mensagens_ordenadas]
    finally:
        db.close()

# Teste local do módulo
if __name__ == "__main__":
    print("A testar base de dados relacional com SQLAlchemy...")
    sessao_teste = "sessao_demo_01"
    
    salvar_mensagem(sessao_teste, "user", "Olá, preciso de ajuda com um tamanho.")
    salvar_mensagem(sessao_teste, "assistant", "Olá! Diga-me qual o modelo e a medida do seu pé.")
    
    historico = carregar_historico_recente(sessao_teste)
    print(f"\nMensagens recuperadas para a sessão '{sessao_teste}':")
    for msg in historico:
        print(f"[{msg['role']}]: {msg['content']}")
    print("\nTeste concluído com sucesso!")