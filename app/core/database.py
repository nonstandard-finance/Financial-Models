from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import relationship, declarative_base

from app.core.constants import SQLALCHEMY_DATABASE_URL
from app.monitoring.services import monitoring

Base = declarative_base()


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,  # Adjust based on your app's concurrency requirements
    max_overflow=5,  # Allows for extra connections in times of high demand
    pool_timeout=120,  # Reduces wait time for a connection
    pool_recycle=18000,  # Recycles connections every 30 minutes
    # echo_pool='debug',  # Logs pool checkouts/checkins (remove in production)
    pool_pre_ping=True,
    # Any idle transaction request past 20seconds will be terminated
    # connect_args={"options": "-c idle_in_transaction_session_timeout=20000"},
)

monitoring.instrument_sqlalchemy(engine=engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_session_with_ctx_manager():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
