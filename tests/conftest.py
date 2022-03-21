import pytest
from blogapp import create_app, config, init_db, db as _db
from blogapp.models import User, Blog


@pytest.fixture(scope='session')
def app():
    """Create a Flask app for the testing"""
    app = create_app(config_class_name=config.TestingConfig)
    yield app


@pytest.fixture(scope='session')
def test_client(app):
    """Create a Flask test client using the Flask app."""
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def db(app):
    """
    Return a session wide database using a Flask-SQLAlchemy database connection.
    """
    with app.app_context():
        _db.app = app
        _db.create_all()
        init_db(_db)
    yield _db
    _db.drop_all()


# https://docs.pytest.org/en/latest/how-to/fixtures.html#autouse-fixtures-fixtures-you-don-t-have-to-request
@pytest.fixture(scope='module', autouse=True)
def session(db, app):
    """ Roll back database changes at the end of each test """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=options)
        db.session = sess
        yield sess
        sess.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope='module')
def user_data():
    """ Data to create a new user"""
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'alice',
        'email': 'alice@gmail.com'
    }
    yield user_data

@pytest.fixture(scope='module')
def blog_data():
    blog_data = {
        'title': 'volcano 2009',
        'content': 'In 2009'
    }
    yield blog_data

@pytest.fixture(scope='module')
def new_user(user_data):
    """ Create a user without a profile and add them to the database. Allow the user object to be used in tests. """
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password=user_data['password_text'])
    yield user

@pytest.fixture(scope='module')
def new_blog(blog_data):
    blog = Blog(title=blog_data['title'], content=blog_data['content'])
    yield blog

