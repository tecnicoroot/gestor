from database.connection import SessionLocal
from models.models import Claim

class ClaimRepository:
    # Cria um novo usuário a partir de uma instância de claim
    def create(self, claim: Claim):
        session = SessionLocal()
        session.add(claim)
        session.commit()
        session.refresh(claim)  # Para garantir ID atualizado etc.
        session.close()
        return claim

    # Busca e retorna claim pelo name
    def find_by_name(self, name: str) -> Claim | None:
        session = SessionLocal()
        claim = session.query(Claim).filter_by(name=name).first()
        session.close()
        return claim

    # Busca e retorna claim pelo id
    def find_by_id(self, id: int) -> Claim | None:
        session = SessionLocal()
        claim = session.query(Claim).filter_by(id=id).first()
        session.close()
        return claim

    # Retorna todos os usuários como lista de claim
    def get_all(self) -> list[Claim]:
        session = SessionLocal()
        claims = session.query(Claim).all()
        session.close()
        return claims

    # Deleta um usuário a partir de um objeto claim
    def delete(self, claim: Claim):
        session = SessionLocal()
        claim_db = session.query(claim).filter_by(id=claim.id).first()
        if claim_db:
            session.delete(claim_db)
            session.commit()
        session.close()

    # Atualiza um usuário a partir de uma instância de claim (id deve existir)
    def update(self, claim: Claim):
        session = SessionLocal()
        claim_db = session.query(claim).filter_by(id=claim.id).first()
        if not claim_db:
            session.close()
            return None

        # Atualize campos individualmente, exceto o id
        claim_db.name = claim.name
        claim_db.description = claim.description

        session.commit()
        session.refresh(claim_db)
        session.close()
        return claim_db