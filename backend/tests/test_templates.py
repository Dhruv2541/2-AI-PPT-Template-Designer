import pytest
from app import create_app, db
from app.models.user import User
from app.models.template import Template
from flask_jwt_extended import create_access_token


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-secret",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def auth_client(app):
    with app.app_context():
        user = User(email="test@example.com", name="Test User")
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id))

    client = app.test_client()
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client, user


def test_list_public_templates(app):
    with app.app_context():
        # Setup data
        t1 = Template(title="T1", schema_data={}, is_public=True, category="Education")
        t2 = Template(title="T2", schema_data={}, is_public=True, category="Business")
        t3 = Template(title="T3", schema_data={}, is_public=False)
        db.session.add_all([t1, t2, t3])
        db.session.commit()

    client = app.test_client()

    # Test all public
    res = client.get("/api/templates")
    assert res.status_code == 200
    assert len(res.json) == 2

    # Test category filter
    res2 = client.get("/api/templates?category=Business")
    assert res2.status_code == 200
    assert len(res2.json) == 1
    assert res2.json[0]["title"] == "T2"


def test_create_and_duplicate_template(auth_client, app):
    client, user = auth_client

    # 1. Create Template
    create_res = client.post(
        "/api/templates",
        json={
            "title": "My Custom Template",
            "schema_data": {"slide1": "content"},
            "category": "Creative",
        },
    )
    assert create_res.status_code == 201
    template_id = create_res.json["id"]

    # 2. Duplicate Template
    dup_res = client.post(f"/api/templates/{template_id}/duplicate")
    assert dup_res.status_code == 201

    assert dup_res.json["title"] == "Copy of My Custom Template"
    assert dup_res.json["user_id"] == str(user.id)
