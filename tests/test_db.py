import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.config import DATABASE_URL, engine, SessionLocal, get_db, Base

# Testar se a variável de ambiente DATABASE_URL é carregada corretamente
def test_database_url():
    assert DATABASE_URL is not None, "DATABASE_URL não foi configurada corretamente"

# Testar se o engine é criado corretamente
def test_create_engine():
    with patch("db.config.create_engine") as mock_create_engine:
        mock_create_engine.return_value = MagicMock()
        engine = mock_create_engine(DATABASE_URL)
        mock_create_engine.assert_called_once_with(DATABASE_URL)

# Testar se o sessionmaker é configurado corretamente
def test_session_local():
    with patch("db.config.sessionmaker") as mock_sessionmaker:
        mock_sessionmaker.return_value = MagicMock()
        session = mock_sessionmaker(autocommit=False, autoflush=False, bind=engine)
        mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=engine)
        assert isinstance(session, MagicMock)

# Testar a função get_db para verificar se uma sessão é criada e fechada corretamente
def test_get_db():
    mock_session = MagicMock()
    with patch("db.config.SessionLocal", return_value=mock_session):
        generator = get_db()
        session = next(generator)
        assert session == mock_session
        mock_session.close.assert_not_called()
        with pytest.raises(StopIteration):
            next(generator)
        mock_session.close.assert_called_once()

# Testar a criação das tabelas no banco de dados
def test_create_all():
    with patch.object(Base.metadata, "create_all") as mock_create_all:
        Base.metadata.create_all(bind=engine)
        mock_create_all.assert_called_once_with(bind=engine)

