from tests.functional.test_auth import login, signup
from flask_login import current_user
from blogapp.models import User, Blog
import re as re


def add_blog(client, title, content):
    """Provides adding a blog to be used in tests"""
    return client.post('/', data=dict(
        title=title,
        content=content
    ), follow_redirects=True)


def delete_blog(client, title):
    """Provides deleting a blog to be used in tests"""
    return client.get('/all/' + title, follow_redirects=True)


def view_blog_by_title(client, title):
    """Provides viewing a blog to be used in tests"""
    return client.get('/blogs/' + title, follow_redirects=True)


def test_index_page_without_login(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request)
    THEN a redirect response code (302) is received as it requires login
    """
    response = test_client.get('/')
    assert response.status_code == 302


def test_index_page_with_login(test_client, new_user, db):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request) and the user is logged in
    THEN a success response code (200) is received
    """
    db.session.add(new_user)
    db.session.commit()
    response = login(test_client, new_user.email, new_user.password);
    assert response.status_code == 200
    assert current_user.is_authenticated == True
    response = test_client.get('/')
    assert response.status_code == 200


def test_insert_blog_success(test_client, new_blog):
    """
    GIVEN a Flask application is running with a database created
    WHEN a new blog is inserted in the Blog table
    THEN the row count should increase by one,
        the current path is at '/all' as it will show all blogs
        a success response status code 200 is received
    """
    row_count_start = Blog.query.count()
    response = add_blog(test_client, new_blog.title, new_blog.content)
    row_count_end = Blog.query.count()

    assert response.status_code == 200
    assert response.request.path == "/all"
    assert (row_count_end - row_count_start) == 1


def test_view_blog_success(test_client, new_blog):
    """
    GIVEN a Flask application is running with a database created
    WHEN the '/blogs/<title>' is requested to view the specified blog
        and the user is logged in
    THEN a success response code (200) is received
        and the current path is at '/blogs/<title>'
    """
    response = view_blog_by_title(test_client, new_blog.title)
    assert response.status_code == 200
    assert response.request.path == "/blogs/" + new_blog.title


def test_view_blog_with_wrong_title(test_client):
    """
    GIVEN a Flask application is running with a database created
    WHEN the '/blogs/<title>' is requested to view the specified blog
        and the user is logged in, but the title is wrong
    THEN the response code is not 200 OK
    """
    response = view_blog_by_title(test_client, "wrongtitle")
    assert response.status_code == 200
    assert re.search('Error, the blog might not exist', response.get_data(as_text=True))


def test_delete_blog_non_exists(test_client):
    """
    GIVEN a Flask application is running with a database created
    WHEN the '/all/<title>' is requested to delete a blog
        and the user is logged in, but the title is non-exist
    THEN the response code is 200 OK as it redirects
        the path is '/all' now
        and proper error messages would be shown.
    """
    response = delete_blog(test_client, "wrongtitle")
    assert response.status_code == 200
    assert response.request.path == "/all"
    assert re.search('Error, the blog might not exist', response.get_data(as_text=True))


def test_delete_blog_success(test_client, new_blog):
    """
    GIVEN a Flask application is running with a database created
    WHEN the '/blogs/<title>' is requested to view the specified blog
        and the user is logged in
    THEN the response code is 200 OK
        the current path is at '/all'
        and the row count of Blog table will decrease by 1
    """
    row_count_start = Blog.query.count()
    response = delete_blog(test_client, new_blog.title)
    row_count_end = Blog.query.count()

    assert response.status_code == 200
    assert response.request.path == "/all"
    assert (row_count_start - row_count_end) == 1




