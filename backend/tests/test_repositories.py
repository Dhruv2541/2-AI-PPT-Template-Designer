import pytest
from app import create_app, db
from app.models.user import User
from app.models.presentation import Presentation, GenerationMode
from app.models.slide import Slide
from app.repositories.presentation_repository import PresentationRepository
from app.repositories.slide_repository import SlideRepository


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_user(app):
    user = User(email="test@example.com", name="Test User")
    db.session.add(user)
    db.session.commit()
    return user


def test_presentation_repository_create_and_get(app, test_user):
    repo = PresentationRepository()

    # Create
    presentation = Presentation(
        user_id=test_user.id,
        title="My First Presentation",
        generation_mode=GenerationMode.FAST,
    )
    created = repo.create(presentation)
    assert created.id is not None
    assert created.title == "My First Presentation"

    # Get by ID
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.user_id == test_user.id
    assert fetched.generation_mode == GenerationMode.FAST

    # Get by User ID
    user_presentations = repo.get_by_user_id(test_user.id)
    assert len(user_presentations) == 1
    assert user_presentations[0].id == created.id


def test_slide_repository_cascade_delete(app, test_user):
    p_repo = PresentationRepository()
    s_repo = SlideRepository()

    presentation = p_repo.create(Presentation(user_id=test_user.id, title="Test"))

    slide1 = s_repo.create(Slide(presentation_id=presentation.id, order_index=0))
    s_repo.create(Slide(presentation_id=presentation.id, order_index=1))

    slides = s_repo.get_by_presentation_id(presentation.id)
    assert len(slides) == 2
    assert slides[0].id == slide1.id

    # Delete presentation should cascade to slides
    p_repo.delete(presentation)

    slides_after_delete = s_repo.get_by_presentation_id(presentation.id)
    assert len(slides_after_delete) == 0
