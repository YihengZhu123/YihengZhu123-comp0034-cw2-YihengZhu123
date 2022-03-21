from blogapp.models import User, Blog


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email, and password fields are defined correctly
    """
    user_data = {
        'first_name': 'Meat',
        'last_name': 'Loaf',
        'password_text': 'BatOutOfHell',
        'email': 'meat@bat.org',
    }

    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password=user_data['password_text'])

    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password == 'BatOutOfHell'


def test_new_blog_details_correct():
    blog_data = {
        'title': 'CS3001 Introduction',
        'content': "content"
    }

    blog = Blog(title=blog_data['title'], content=blog_data['content'])
    assert blog.title == 'CS3001 Introduction'
    assert blog.content == 'content'
