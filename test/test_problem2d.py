# Test for the password file
import bcrypt
from main import get_user, hash_password, create_salt, enrol_user, remove_user, check_password, password_checker

def test_passwords():

    print("Password File tests")
    print("------------")

    print("Verifying salt")
    salt = create_salt()

    # 29 is the length of the encoded salt string returned by bcrypt.gensalt()
    assert len(salt) == 29
    print("Salt length: " + str(len(salt)) + " Expected length: 29")

    # salts are unique
    salt2 = create_salt()
    assert salt != salt2
    print("Salt2 is different than Salt PASSED")

    # Password hashing
    password1 = "P@ssW3rd"
    password2 = "P#ssW2rd"

    hashed_pw1 = hash_password(password1, salt)
    hashed_pw2 = hash_password(password2, salt2)
    assert hashed_pw1 != hashed_pw2
    print("hashed passwords are unique PASSED")

    hashed_pw3 = hash_password(password1, salt)

    assert hashed_pw3 == hashed_pw1
    print("Identical password + salt results in identical hashes PASSED")

    # Correct password check
    assert check_password(hashed_pw1, salt, password1)
    print("Correct password verification PASSED")


if __name__ == "__main__":
    test_passwords()
