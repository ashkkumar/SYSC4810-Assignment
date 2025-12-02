# Overview
This project implements a simple user authentication and role-based access control (RBAC) system using Python.
The system supports:
User sign-up with password policy enforcement
Secure password hashing using bcrypt
Login authentication
Time-restricted login for specific roles (e.g., Teller: 9am–5pm)
Role-based authorized operations
Test scripts validating the access control policies
The program is designed to run in a terminal environment on Ubuntu 24.04.3 LTS using Python 3.12.3.

# Prerequisites
The machine used for grading is guaranteed to have:
Python 3.12.3
pip (preinstalled in Ubuntu)
Required libraries:
bcrypt

# Installation Instructions
Run the following command to install required packages:
### IMPORTANT  
bcrypt must be installed for program to run  
```
pip install bcrypt
```
The program uses only:  
Python Standard Library  
bcrypt (for hashing)  

# How to Run the Program
Run main program
From the project root directory:  
```
python3 -m main
```
OR 
```
python -m main.py (depending on your specific system)
```
This will start the interactive prompt:  
Enter LOGIN to Login or SIGN UP to sign up:  

# Program Flow
SIGN UP  
The program will:  
Ask for username  
Ask for password  
Validate the password using the assignment’s constraints  
Hash and store the password + salt in passwd.txt  
Store the role and authorized operations  

LOGIN  
The program will:  
Verify the username exists  
Retrieve the stored salt and hash  
Verify the password using bcrypt  
Check time-restricted access rules (e.g., Teller)  
Show the user’s authorized operations  

# Running the Tests
All tests are located inside the /test/ folder.  
To run a test file:  
```
python3 -m test.<filename>
```
Example:  
```
python3 -m test.test_problem1c
```
