from blogapp.models import User
import re as re
from wtforms.validators import ValidationError
from flask_login import current_user


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def signup(client, first_name, last_name, email, password):
    """Provides signup to be used in tests"""
    return client.post('/signup', data=dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Provides logout to be used in tests"""
    return client.get('/logout', follow_redirects=True)


def view_without_login(test_client):
    return test_client.get('/all')


def test_user_sign_up_success(new_user, test_client):
    response = signup(test_client, first_name=new_user.first_name, last_name=new_user.last_name,
                      email=new_user.email, password=new_user.password)
    assert response.status_code == 200


def test_user_login_success(new_user, test_client, db):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    row_count_start = User.query.count()
    db.session.add(new_user)
    db.session.commit()
    row_count_end = User.query.count()
    print("row_start: ", row_count_start)
    print("row_end: ", row_count_end)

    assert row_count_end - row_count_start == 1
    response = login(test_client, new_user.email, new_user.password)
    assert response.status_code == 200
    assert current_user.is_authenticated

def test_user_logout_success(test_client):
    """
    GIVEN a User logged out
    WHEN the logout operation is successful
    THEN the response status code is 200
    AND  is not authenticated.
    """
    response = logout(test_client)
    assert response.status_code == 200
    assert current_user.is_authenticated == False

def test_user_login_with_wrong_email(new_user, test_client, db):
    """
    GIVEN a User has been created
    WHEN the user logs in with the wrong email address
    THEN then an error message should be displayed on the login form ('No account found with that email address.')
    """

    response = login(test_client, email='d', password=new_user.password)
    assert current_user.is_authenticated == False
    assert re.search('Error, no account found with that email address.', response.get_data(as_text=True))


def test_user_login_with_wrong_password(new_user, test_client, db):
    """
    GIVEN a User has been created
    WHEN the user logs in with the wrong password
    THEN then an error message should be displayed on the login form ('Incorrect password.')
    """
    response = login(test_client, email=new_user.email, password="wrongpassword")
    assert re.search('Error, incorrect password.', response.get_data(as_text=True))


def test_user_logout_redirect(test_client, new_user, db):
    """
    GIVEN a User logged out
    WHEN they access the navigation bar
    THEN there should be an option to login in
    """
    response = login(test_client, new_user.email, new_user.password);
    response = logout(test_client)
    response = view_without_login(test_client)

    assert response.status_code == 302
    assert re.search('You should be redirected automatically to target URL', response.get_data(as_text=True))



