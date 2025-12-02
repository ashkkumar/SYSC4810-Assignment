from main import remove_user, enrol_user, authenticate, check_password, password_checker

def test_login():

    print("Login & Authentication tests")
    print("---------------------------")

    # Setup - enroll test users
    test_user1 = "Alice"
    test_user2 = "Bob"
    test_user3 = "Charlie"

    # Enroll test users
    enrol_user(test_user1, "P@ssW0rd1", "Client")
    enrol_user(test_user2, "P#ssW0rd2", "Premium Client")
    enrol_user(test_user3, "P@ssW0rd3", "Financial Advisor")

    # Test 1: Correct login for user 1
    assert authenticate(test_user1, "P@ssW0rd1") is True
    print("Test 1: Correct login PASSED")

    # Test 2: Incorrect password for user 1
    assert authenticate(test_user1, "WrongP@ss") is False
    print("Test 2: Wrong password blocked PASSED")

    # Test 3: Non-existent user
    assert authenticate("NonUser", "AnyPass123!") is False
    print("Test 3: Non-existent user blocked PASSED")

    # Test 4: Correct login for user 2
    assert authenticate(test_user2, "P#ssW0rd2") is True
    print("Test 4: Correct login for Premium Client PASSED")

    # Test 5: Correct login for user 3
    assert authenticate(test_user3, "P@ssW0rd3") is True
    print("Test 5: Correct login for Financial Advisor PASSED")

    # Cleanup
    remove_user(test_user1)
    remove_user(test_user2)
    remove_user(test_user3)
    print("Cleanup of test users PASSED")

if __name__ == "__main__":
    test_login()