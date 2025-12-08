from app.schemas.user import Get_current_user

# test for getting the logged in user
def test_loggedin_user(get_loggedIn_user, test_user):
    assert get_loggedIn_user[0].status_code == 200
    assert get_loggedIn_user[1].email == test_user["username"]