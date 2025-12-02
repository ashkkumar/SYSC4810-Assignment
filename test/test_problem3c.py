import bcrypt
from main import get_user, hash_password, create_salt, enrol_user, remove_user, check_password, password_checker

def test_enrolement():

    # password creation is valid
    assert not password_checker("user", "Ab1!")  # too short
    print("Password short length validation PASSED")

    assert not password_checker("user", "Ab1!asbaiabudia")  # too kibg
    print("Password long length validation PASSED")

    assert not password_checker("user", "abc123!!")
    print("Missing uppercase validation PASSED")

    assert not password_checker("user", "ABC123!!")
    print("Missing lowercase validation PASSED")

    assert not password_checker("user", "Abcdef!!")
    print("Missing digit validation PASSED")

    assert not password_checker("user", "Abcdef12")
    print("Missing special character validation PASSED")

    assert not password_checker("user", "user")
    print("Password != username validation PASSED")

    assert not password_checker("ash", "Passw#rd1")
    print("Common password validation PASSED")

    test_user = "Ellis"
    enrol_user(test_user, "P@sSw0rD123", "Client")
    user = get_user(test_user)

    assert user is not None
    print("Successfully retrieved user from DB PASSED")

    assert user["username"] == test_user
    print("Username matches DB data PASSED")

    test_user2 = "Bryan"
    user2 = get_user(test_user2)
    assert user2 is None
    print("Non valid users are not taken from DB file PASSED")

    remove_user(test_user)


if __name__ == "__main__":
    test_enrolement()
