import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from app.core.database import get_session
from app.core.security import create_access_token
from app.main import app
from app.core.config import settings
from sqlalchemy.exc import SQLAlchemyError
from app.models.urls import Urls
from app.services.urlshortener import url_shortener
from app.schemas.user import Get_current_user



DB_URL = f"{settings.DB_DRIVER}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test"
engine = create_engine(DB_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)

@pytest.fixture
def session():
     # before testing starts creates the various tables
    SQLModel.metadata.create_all(engine)
    
    # creates test_session instance
    with Session(engine) as test_session:
        try:
            yield test_session
        except SQLAlchemyError as e:
            test_session.rollback()
            raise e
        finally:
            test_session.close()



# create a database session instance for each test func
@pytest.fixture
def client(session):
    # session override logic
    def overide_get_session():
            try:
                yield session
            except SQLAlchemyError as e:
                session.rollback()
                raise e
            finally:
                session.close()
                
    # overides the development session dependency with the test dependencies
    app.dependency_overrides[get_session] = overide_get_session
    # returns the test client instance to facilitate testing
    yield TestClient(app)
    # after testing concludes deletes all tables
    SQLModel.metadata.drop_all(engine)
    
# test user create
@pytest.fixture
def test_user(client):
    user_data = {"email": "heri@example.com", "password": "password123"}
    res = client.post("/auth/register", json=user_data)
    assert res.status_code == 201
    new_user = {}
    new_user['username'] = user_data['email']
    new_user["password"] = user_data["password"]
    return new_user

# test jwt token creation
@pytest.fixture
def token(client, test_user):
    res = client.post("/auth/login", data=test_user)
    token = res.json().get("access_token")
    token_type = res.json().get("token_type")
    return [token, token_type]

# test authorization. pass token to the authoriztion header upon every request
@pytest.fixture
def authorized_user(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"{token[1]} {token[0]}"
    }
    return client

# test get logged in user
@pytest.fixture
def get_loggedIn_user(authorized_user):
    res = authorized_user.get("/users/logged_in")
    user = Get_current_user(**res.json())
    return [ res, user]

# test urls in db
@pytest.fixture
def test_urls(get_loggedIn_user, session):
    urls_data = [{
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example1.com",
        "Shortened_url": f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example1.com")}", 
        "clicks": 0, 
        "created_at": None
    }, {
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example2.com",
        "Shortened_url": f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example2.com")}", 
        "clicks": 0, 
        "created_at": None
    },{
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example3.com",
        "Shortened_url": f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example3.com")}", 
        "clicks": 0, 
        "created_at": None
    },{
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example4.com",
        "Shortened_url": f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example4.com")}", 
        "clicks": 0, 
        "created_at": None
    },{
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example5.com",
        "Shortened_url": f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example5.com")}", 
        "clicks": 0, 
        "created_at": None
    },{
        "id": None,
        "user_id": get_loggedIn_user[1].id,
        "original_url": "http://example6.com",
        "Shortened_url":f"{settings.BACKEND_URL}/r/{url_shortener.shorten_url("http://example6.com")}", 
        "clicks": 0, 
        "created_at": None
    }]
    # url mapping function
    def urls_model(urls):
        return Urls(**urls)
    
    mapped_url_data = map(urls_model, urls_data)
    url = list(mapped_url_data)
    # adds list of urls to db 
    session.add_all(url)
    session.commit()
    # query for getting url of logged in users
    urls_query = session.exec(select(Urls).where(Urls.user_id == get_loggedIn_user[1].id)).all()
    return urls_query