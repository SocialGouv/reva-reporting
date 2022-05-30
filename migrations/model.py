from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TIMESTAMP, BOOLEAN, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Candidacy(Base):
    __tablename__ = 'candidacy'

    id = Column(VARCHAR(255), primary_key=True)
    deviceId = Column(VARCHAR(255))
    keycloak_sub = Column(VARCHAR(255))
    companion_id = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))
    certification_id = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    phone = Column(VARCHAR(255))


class Goal(Base):
    __tablename__ = 'goal'

    id = Column(VARCHAR(255), primary_key=True)
    label = Column(VARCHAR(255))
    is_active = Column(BOOLEAN)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))
    needs_additional_information = Column(BOOLEAN)
    order = Column(INTEGER)
