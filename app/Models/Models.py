from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LogMensagem(Base):
    __tablename__ = "log_mensagens"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(String(50), index=True)         # tamanho definido para indexação
    nome = Column(String(100))
    telefone = Column(String(50), index=True)          # tamanho fixo para permitir índice
    mensagem_enviada = Column(Text)
    mensagem_recebida_ia = Column(Text)
    data_acionamento = Column(DateTime, default=datetime.utcnow)
    data_resposta_ia = Column(DateTime, nullable=True)
    feedback_usuario = Column(String(100), nullable=True)

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(20), unique=True, index=True)
    nome = Column(String(100))
    telefone = Column(String(50), unique=True, index=True)
    setor = Column(String(50))
    cargo = Column(String(50))
    data_entrada_empresa = Column(DateTime)
    data_nascimento = Column(DateTime)
    email_corporativo = Column(String(100), unique=True)

class Autenticacao(Base):
    __tablename__ = "autenticacoes"
    id = Column(Integer, primary_key=True, index=True)
    telefone = Column(String(50), index=True)
    codigo_verificacao = Column(String(10), nullable=True)
    verificado = Column(String(1), default="N")  # 'S' para sim, 'N' para não
    data_solicitacao = Column(DateTime, default=datetime.utcnow)
