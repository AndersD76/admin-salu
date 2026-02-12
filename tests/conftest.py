import os
import sys
import pytest

# Set test environment variables BEFORE any app imports
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["CRON_SECRET"] = "test-cron-secret"

# Ensure project root is in path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(__file__))
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.models.property import Property
from app.models.broker import Broker
from app.models.contact import Contact, ContactType, ContactStatus
from app.main import app
import uuid


# Test database setup
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    # Reset rate limiter between tests
    from app.api.auth import _login_attempts
    _login_attempts.clear()

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Clean up test.db file
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass


@pytest.fixture
def db():
    """Get a test database session."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """Get a test client."""
    return TestClient(app)


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User(
        id=str(uuid.uuid4()),
        name="Admin Test",
        email="admin@test.com",
        password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    user = User(
        id=str(uuid.uuid4()),
        name="Regular User",
        email="user@test.com",
        password=get_password_hash("user123"),
        role=UserRole.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(admin_user):
    """Get auth headers for admin user (generates token directly)."""
    token = create_access_token(data={"sub": str(admin_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_property(db):
    """Create a sample property."""
    prop = Property(
        id=str(uuid.uuid4()),
        external_code="TEST-001",
        property_type="Apartamento",
        purpose="Venda",
        city="Sao Paulo",
        neighborhood="Centro",
        is_active=True,
        view_count=100,
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@pytest.fixture
def sample_broker(db):
    """Create a sample broker."""
    broker = Broker(
        id=str(uuid.uuid4()),
        name="Broker Test",
        email="broker@test.com",
        is_active=True,
    )
    db.add(broker)
    db.commit()
    db.refresh(broker)
    return broker


@pytest.fixture
def sample_contact(db, sample_property):
    """Create a sample contact."""
    contact = Contact(
        id=str(uuid.uuid4()),
        property_id=sample_property.id,
        name="Lead Test",
        email="lead@test.com",
        message="Quero mais informacoes",
        type=ContactType.INFO,
        status=ContactStatus.NEW,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
