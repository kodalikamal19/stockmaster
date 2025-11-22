import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            login_id='testuser',
            email='test@example.com'
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()
        return user


def test_signup_success(client):
    """Test successful user signup"""
    response = client.post('/api/auth/signup', json={
        'login_id': 'newuser',
        'email': 'newuser@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'user' in data
    assert data['user']['login_id'] == 'newuser'


def test_signup_duplicate_login_id(client, test_user):
    """Test signup with duplicate login_id"""
    response = client.post('/api/auth/signup', json={
        'login_id': 'testuser',
        'email': 'different@example.com',
        'password': 'Test123!',
        'confirm_password': 'Test123!'
    })
    assert response.status_code == 400


def test_signup_invalid_password(client):
    """Test signup with invalid password"""
    response = client.post('/api/auth/signup', json={
        'login_id': 'newuser',
        'email': 'newuser@example.com',
        'password': 'weak',
        'confirm_password': 'weak'
    })
    assert response.status_code == 400


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post('/api/auth/login', json={
        'login_id': 'testuser',
        'password': 'Test123!'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'login_id': 'testuser',
        'password': 'WrongPassword123!'
    })
    assert response.status_code == 401

