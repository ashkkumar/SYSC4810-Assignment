# Tests for the acceess control mechanism RBAC

from main import roles_permissions, enrol_user, get_user, remove_user

def is_allowed(username: str, operation: int):
    """helper function for testing RBAC"""

    user = get_user(username)
    role = user["role"]
    if operation in roles_permissions[role]:
        return True
    else:
        raise PermissionError("Operation NOT allowed")

def test_rbac():

    print("RBAC Tests")
    print("------------")

    enrol_user("t_client", "Test@1234", "Client")
    enrol_user("t_premium_client", "Test@5326", "Premium Client")
    enrol_user("t_teller", "Test@2643", "Teller")
    enrol_user("t_advisor", "Test@5678", "Financial Advisor")
    enrol_user("t_planner", "Test@9012", "Financial Planner")

    print("Testing Client role")
    assert is_allowed("t_client", 1) == True
    print("Client Test 1 PASSED (View Balance)")

    assert is_allowed("t_client", 2) == True
    print("Client Test 2 PASSED (View Portfolio)")

    assert is_allowed("t_client", 5) == True
    print("Client Test 3 PASSED (view Advisor contact)")

    try:
        is_allowed("t_client", 3)
        assert False, "Client should NOT have access to modify portfolio"
    except PermissionError:
        print("Client Test 4 PASSED (blocked modify portfolio)")

    print("\nTesting Premium Client")
    assert is_allowed("t_premium_client", 1)
    print("Premium Client Test 1 PASSED (View Balance)")

    assert is_allowed("t_premium_client", 2)
    print("Premium Client Test 2 PASSED (View Balance)")

    assert is_allowed("t_premium_client", 3)
    print("Premium Client Test 3 PASSED (Modify Investment Portfolio)")

    assert is_allowed("t_premium_client", 4)
    print("Premium Client Test 4 PASSED (View Financial Planner Info)")

    assert is_allowed("t_premium_client", 5)
    print("Premium Client Test 5 PASSED (View Financial Advisor Info)")

    try:
        is_allowed("t_premium_client", 6)
        assert False, "Premium Client should NOT have access to Money Market Instruments"
    except PermissionError:
        print("Premium Client Test 6 PASSED (blocked Money Market Instruments)")

    print("\nTesting Teler")
    assert is_allowed("t_teller", 1)
    print("Teller Test 1 PASSED (View Balance)")

    assert is_allowed("t_teller", 2)
    print("Teller Test 2 PASSED (View Balance)")

    try:
        is_allowed("t_teller", 3)
        assert False, "Teller should NOT have access to modify portfolio"
    except PermissionError:
        print("Teller Test 3 PASSED (blocked modify portfolio)")

    print("\nTesting Financial Advisor")
    assert is_allowed("t_advisor", 1)
    print("Financial Advisor Test 1 PASSED (View Balance)")

    assert is_allowed("t_advisor", 2)
    print("Financial Advisor Test 2 PASSED (View Balance)")

    assert is_allowed("t_advisor", 3)
    print("Financial Advisor Test 3 PASSED (Modify Investment Portfolio)")

    assert is_allowed("t_advisor", 7)
    print("Financial Advisor Test 4 PASSED (View Private Consumer Instruments)")

    try:
        is_allowed("t_advisor", 6)
        assert False, "Financial Advisor should NOT have access to Money Market Instruments"
    except PermissionError:
        print("Financial Advisor Test 5 PASSED (blocked Money Market Instruments)")

    print("\nTesting Financial Planner")
    assert is_allowed("t_planner", 1)
    print("Financial Planner Test 1 PASSED (View Balance)")

    assert is_allowed("t_planner", 2)
    print("Financial Planner Test 2 PASSED (View Balance)")

    assert is_allowed("t_planner", 3)
    print("Financial Planner Test 3 PASSED (Modify Investment Portfolio)")

    assert is_allowed("t_planner", 6)
    print("Financial Planner Test 4 PASSED (View Private Consumer Instruments)")

    assert is_allowed("t_planner", 7)
    print("Financial Planner Test 5 PASSED (View Private Consumer Instruments)")

    try:
        is_allowed("t_advisor", 4)
        assert False, "Financial Planner should NOT have access to View Planner Info"
    except PermissionError:
        print("Financial Planner Test 6 PASSED (blocked Money Market Instruments)")

    remove_user("t_client")
    remove_user("t_premium_client")
    remove_user("t_teller")
    remove_user("t_advisor")
    remove_user("t_planner")




if __name__ == "__main__":
    test_rbac()