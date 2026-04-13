from sqlalchemy import (
    Column, Integer, String, LargeBinary, DateTime, Enum as SqlEnum, 
    func, Boolean, ForeignKey, Table, CHAR
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import logs
Base = declarative_base()

# Enum de status
class Status(enum.Enum):
    ACTIVE = "ativo"
    INACTIVE = "inativo"
    SUSPENDED = "suspenso"

# Tabela associativa N:N
user_robot_association = Table(
    'user_robot',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('robot_id', Integer, ForeignKey('robots.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    # relacionamento N:N com User
    users = relationship('User', secondary='user_roles', back_populates='roles')
    # relacionamento N:N com Claim
    claims = relationship('Claim', secondary='role_claims', back_populates='roles')


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class Claim(Base):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    # relacionamento N:N com Role
    roles = relationship('Role', secondary='role_claims', back_populates='claims')

role_claims = Table(
    'role_claims',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('claim_id', Integer, ForeignKey('claims.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)  # <--- adicione esta
    email = Column(String)  # <--- adicione esta
    username = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    status = Column(SqlEnum(Status), default=Status.ACTIVE, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    # Relacionamento N:N com Robo
    robots = relationship('Robot', secondary=user_robot_association, back_populates='users')
    # Relacionamento 1:N com User
    log_access = relationship("LogAccess", back_populates="users", cascade="all, delete-orphan")
# Classe Robo
class Robot(Base):
    __tablename__ = 'robots'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_origin = Column(Integer, nullable=False)
    robot = Column(String(100), unique=True, nullable=False)
    description = Column(String(2000))
    activated = Column(Boolean, nullable=False)
    interval = Column(Integer)
    action = Column(CHAR(1))
    screen = Column(CHAR(1))
    executable_path = Column(String(200))
    time_limit = Column(Integer)
    activation_file = Column(String(200))
    executable_name = Column(String(45))
    workbook = Column(String(200))
    spreadsheet_repository = Column(String(200))
    notified = Column(String(1000))
    activated_program1 = Column(String(45))
    activated_program2 = Column(String(45))
    robot_sequence = Column(Integer)
    robot_user = Column(String(45))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relacionamento N:N com User
    users = relationship('User', secondary=user_robot_association, back_populates='robots')


class LogAccess(Base):
    __tablename__ = 'log_access'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = (Column(Integer, ForeignKey('users.id')))
    level = Column(String(20))
    message = Column(String(2000))
    created_at = Column(DateTime, server_default=func.now())
    users = relationship("User", back_populates="log_access")


