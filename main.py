import bcrypt
from datetime import datetime

# Problem 1: RBAC implementation
# permissions index, each permission is mapped to a number
permissions_index = {
    1: "view_account_balance",
    2: "view_investment_portfolio",
    3: "modify_investment_portfolio",
    4: "view_financial_planner_contact",
    5: "view_financial_advisor_contact",
    6: "view_money_market_instruments",
    7: "view_private_consumer_instruments"
}

# Assign roles and permissions
roles_permissions = {
    "Client": [1, 2, 5],
    "Premium Client": [1, 2, 3, 4, 5],
    "Teller": [1, 2, "limited_access"],
    "Financial Advisor": [1, 2, 3, 7],
    "Financial Planner": [1, 2, 3, 6, 7]
}


# -----------------------------------
# Problem 2: Password choice + file
def create_salt() -> bytes:
    """Creates a 16 byte salt for passwords"""
    return bcrypt.gensalt()


def hash_password(password: str, salt: bytes):
    """Hashes a password using Bcrypt's hash function and attaches salt"""

    if not password:
        raise ValueError("Password is incorrect")

    return bcrypt.hashpw(password.encode('utf-8'), salt)


# Password file containing user info
DB_FILE = "passwd.txt"


# Problem 3: Enrollment of Users and storing data
def valid_username(username: str):
    """Checks if username is valid, we want unique usernames"""
    file = open(DB_FILE, "r")

    for line in file:
        user = line.strip().split(" ")
        if user[0] == username:
            return True
    file.close()
    return False


def password_checker(username: str, password: str):
    """Checks if the user password is valid
    or not when creating their account

    Password must:
        - must be between 8 and 12 characters in length.
         Passwords must include at least:
            – one upper-case letter
            – one lower-case letter
            – one numerical digit
            – one special character from the following: !, @, #, $, %, *, &
        • Passwords found on a list of common weak passwords must be prohibited. Note that the list
        should be flexible to allow for the addition of new exclusions over time.
        • Passwords matching the username must be prohibited.
    """

    correct_length = False
    lowercase = False
    uppercase = False
    digit = False
    special_char = False
    not_common = True
    not_username = False

    # lets check the length first
    if 8 <= len(password) <= 12:
        correct_length = True

    # check if password == username
    if password != username:
        not_username = True

    specials = ["!", "@", "#", "$", "%", "*", "&"]
    # check for specific characters like uppercase, lowercase etc
    for char in password:
        # True if char is lowercase
        if char.islower():
            lowercase = True
        # True if char is uppercase
        elif char.isupper():
            uppercase = True
        # True if char is a digit
        elif char.isdigit():
            digit = True
        # True if char is a special character
        elif char in specials:
            special_char = True

    # Check if it is a common password
    # True is the password is common, false if it is not
    common_passwords = open("common_passwords.txt")
    for line in common_passwords:
        if password.strip() == line.strip():
            not_common = False
            print("Select a different password, common passwords not allowed")
            break
    common_passwords.close()

    return correct_length and lowercase and uppercase and digit and special_char and not_common and not_username


def enrol_user(username: str, password: str, role: str):
    """Enrols a new user and adds their info to the database"""

    if valid_username(username):
        raise ValueError("Username is taken, try again")
    if not password_checker(username, password):
        raise ValueError("Password is invalid, try again")
    if role not in roles_permissions:
        raise ValueError("Role is invalid, try again")

    salt = create_salt()
    hashed_pass = hash_password(password, salt)

    file = open(DB_FILE, "a")

    file.write(f"{username} {hashed_pass.decode()} {salt.decode()} {role}\n")
    file.close()


def remove_user(username: str) -> any:
    """Removes a user from the database by username."""
    found = False

    # 1. Read all lines first
    with open(DB_FILE, "r") as file:
        lines = file.readlines()

    # 2. Filter out the user line
    new_lines = []
    for line in lines:
        if line.startswith(f"{username} "):
            found = True
            continue  # skip this user
        new_lines.append(line)

    # 3. Write back all remaining lines
    with open(DB_FILE, "w") as file:
        file.writelines(new_lines)

    # 4. Return messages based on result
    if not found:
        return f"User '{username}' not found in database."

    return None

# enrol_user("ash", "Kaijudos2#3", "Client")

# Problem 4 (here downwards)

def can_login(role: str):
    """Checks if a teller is within business hours"""
    if "limited_access" in roles_permissions[role]:
        current_hour = datetime.now().hour

        if 9 <= current_hour <= 17:
            return True
        else:
            return False
    return True

def get_user(username: str):
    """Get user from DB to see if credentials match use input"""

    file = open(DB_FILE, "r")
    for line in file:
        user = line.strip().split(" ")

        if user[0] == username:
            return {
                "username": user[0],
                "password": user[1].encode("utf-8"),
                "salt": user[2].encode("utf-8"),
                "role": " ".join(user[3:])
            }
    file.close()
    return None


def check_password(stored_pw: bytes, salt: bytes, password: str) -> bool:
    """Checks if password entered matched the password stored"""

    return stored_pw == hash_password(password, salt)

def authenticate(username: str, password: str):
    """authenticates the user, matches username + password to stored data"""

    user = get_user(username)

    if user is None:
        return False
    # here maybe
    stored_pw = user['password']
    salt = user['salt']

    return check_password(stored_pw, salt, password)


def check_access(username: str, permission: int):
    """Checks the permissions of a specific user"""
    user = get_user(username)
    print(f"Your authorized operations are: {roles_permissions[user['role']]}")


def main():
    """Main program that will be running"""

    print(
        "justInvest System \n"
        "Operations available \n"
        "------------------------------ \n"
        "1. View account balance \n"
        "2. View investment portfolio \n"
        "3. Modify investment portfolio \n"
        "4. View Financial Planner contact info \n"
        "5. View Financial Advisor Contact \n"
        "6. View money market instruments \n"
        "7. View private consumer instruments \n"
    )

    while True:

        try:
            request = input("Enter LOGIN to Login or SIGN UP to sign up: ").strip().upper()
        except Exception:
            print("Invalid try again")

        if request == "LOGIN":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if authenticate(username, password):

                user = get_user(username)
                role = user["role"]

                if not can_login(role):
                    print("Access restricted. Tellors can only log in during business hours (9am-5pm).")
                    continue

                print("Access GRANTED!\n")
                print(f"Your authorized operations are: {roles_permissions[role]}")
            else:
                print("Authentication failed")
                continue

        elif request == "SIGN UP":
            username = input("Enter username: ")
            print("""Passwords must be between 8 and 12 characters in length.
                    • Passwords must include at least:
                    – one upper-case letter
                    – one lower-case letter
                    – one numerical digit
                    – one special character from the following: !, @, #, $, %, *, &
                    • Passwords found on a list of common weak passwords must be prohibited. 
                    • Passwords matching the username must be prohibited.""")
            password = input("Enter password: ")
            role = input("Enter a role: Client, Premium Client, Teller, Financial Advisor, Financial Planner: ")

            try:
                enrol_user(username, password, role)
                print("User successfully enrolled!")
                print(f"Your authorized operations are: {roles_permissions[role]}")
                print("Please Log in")
            except ValueError as e:
                print(e)
            continue
        else:
            print("Invalid Choice. Please enter LOGIN or SIGN UP")
            continue

        user = get_user(username)
        role = user["role"]

        # choose operation
        while True:
            try:
                operation = int(input("Select an operation you would like to perform: "))
            except ValueError:
                print("Operation must be an integer")
                continue

            if operation in roles_permissions[role]:
                print("Operation Allowed!")
            else:
                print("Operation NOT allowed.")


if __name__ ==  "__main__":
    main()
