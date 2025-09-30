import pytest
import uuid
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def generate_unique_email(name_prefix="user"):
    return f"{name_prefix}_{uuid.uuid4().hex[:8]}@example.com"

def generate_unique_name(name_prefix="User"):
    return f"{name_prefix}_{uuid.uuid4().hex[:4]}"

def test_add_user(client):
    name = generate_unique_name("priyanshi")
    email = generate_unique_email("priyanshi")
    rv = client.post("/users/add", data={"name": name, "email": email}, follow_redirects=True)
    assert rv.status_code == 200
    assert bytes(name, "utf-8") in rv.data

def test_update_user(client):
    name = generate_unique_name("danny")
    email = generate_unique_email("danny")
    client.post("/users/add", data={"name": name, "email": email}, follow_redirects=True)
    
    user = User.query.filter_by(name=name).first()
    
    new_name = generate_unique_name("daniel")
    new_email = generate_unique_email("daniel")
    rv = client.post(f"/users/{user.id}/update", data={"name": new_name, "email": new_email}, follow_redirects=True)
    assert rv.status_code == 200
    assert bytes(new_name, "utf-8") in rv.data

def test_delete_user(client):
    name = generate_unique_name("jesse")
    email = generate_unique_email("jesse")
    client.post("/users/add", data={"name": name, "email": email}, follow_redirects=True)
    
    user = User.query.filter_by(name=name).first()
    assert user is not None  

    client.post(f"/users/{user.id}/delete", follow_redirects=True)
    
    deleted_user = User.query.filter_by(name=name).first()
    assert deleted_user is None

