import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Models.Models import Base, Funcionario

DATABASE_URL = ""

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def incluir_funcionario():
    db = SessionLocal()
    try:
        novo_funcionario = Funcionario(
            matricula="12345",
            nome="Márcio",
            telefone="5511945122773", 
            setor="TI",
            cargo="Desenvolvedor",
            data_entrada_empresa=datetime.datetime(2020, 1, 1),
            data_nascimento=datetime.datetime(2000, 1, 1),
            email_corporativo="marcio_mota@usp.br" 
        )
        db.add(novo_funcionario)
        db.commit()
        db.refresh(novo_funcionario)
        print(f"Funcionário incluído com sucesso. ID gerado: {novo_funcionario.id}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao incluir funcionário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    incluir_funcionario()
