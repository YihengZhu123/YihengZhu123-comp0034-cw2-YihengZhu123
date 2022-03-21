from blogapp.models import User, Blog


def test_user_table_has_one_more_row(db):
    """
        GIVEN the app is created with a database
        WHEN a new user is inserted in the User table
        THEN the row count should increase by one
    """
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }

    row_count_start = User.query.count()
    new_user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                    password=user_data['password_text'])
    db.session.add(new_user)
    db.session.commit()
    row_count_end = User.query.count()
    assert row_count_end - row_count_start == 1


def test_blog_table_has_one_more_row(new_blog, db):
    """
        GIVEN the app is created with a database
        WHEN a new blog is inserted in the Blog table
        THEN the row count should increase by one
    """
    row_count_start = Blog.query.count()
    db.session.add(new_blog)
    db.session.commit()
    row_count_end = Blog.query.count()
    assert row_count_end - row_count_start == 1