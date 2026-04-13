from database.connection import SessionLocal
from models.models import Role, Claim

class RoleRepository:
    # Não recebe Role/Claim no construtor, pois já foram importados

    def create(self, role: Role):
        with SessionLocal() as session:
            session.add(role)
            session.commit()
            session.refresh(role)
            return role

    def find_by_name(self, name: str) -> Role | None:
        with SessionLocal() as session:
            return session.query(Role).filter_by(name=name).first()

    def find_by_id(self, id: int) -> Role | None:
        with SessionLocal() as session:
            return session.query(Role).filter_by(id=id).first()

    def get_all_role(self) -> list[Role]:
        with SessionLocal() as session:

            return session.query(Role).all()

    def get_all_claim(self) -> list[Claim]:
        with SessionLocal() as session:
            return session.query(Claim).all()

    def delete(self, role_id: int):
        with SessionLocal() as session:
            role_db = session.query(Role).filter_by(id=role_id).first()
            if role_db:
                session.delete(role_db)
                session.commit()

    def update(self, role: Role):
        with SessionLocal() as session:
            role_db = session.query(Role).filter_by(id=role.id).first()
            if not role_db:
                return None

            role_db.name = role.name
            role_db.description = role.description

            session.commit()
            session.refresh(role_db)
            return role_db

    def set_claims_for_role(self, role_id, claim_ids):
        with SessionLocal() as session:
            role = session.query(Role).filter_by(id=role_id).first()
            if not role:
                return False

            claims = session.query(Claim).filter(Claim.id.in_(claim_ids)).all()
            role.claims = claims
            session.commit()
            return True
    
    def get_claims_by_role(self, role_id):
        with SessionLocal() as session:
            role = session.query(Role).filter_by(id=role_id).first()
            if not role:
                return []

            return role.claims