# db_service.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional


class Database:
    """Singleton-style DB loader: Engine + Session factory."""

    _engine = None
    _SessionLocal = None

    @classmethod
    def init(cls, db_url: str):
        """Initialize engine and sessionmaker once."""
        if cls._engine is not None:  # Prevent accidental re-init
            return

        cls._engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False,
            future=True,
        )

        cls._SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls._engine, future=True
        )

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise RuntimeError(
                "Database engine not initialized. Call Database.init() first."
            )
        return cls._engine

    @classmethod
    def get_session(cls):
        if cls._SessionLocal is None:
            raise RuntimeError(
                "Session factory not initialized. Call Database.init() first."
            )
        return cls._SessionLocal()
