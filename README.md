# OrangeHRM User Management Automation 

This project automates the **User Management module** in OrangeHRM using **Playwright (Python)**.  
It covers complete CRUD operations — Add, Search, Edit, Validate, and Delete user functionality.

---

##  Features Automated
1. Login to OrangeHRM Application
2. Navigate to the PIM Module and Fetch Existing  Employee
3. Navigate to the Admin Module
4. Add a New User  
5. Search for the Newly Created User  
6. Edit User Details  
7. Validate Updated User Details  
8. Delete the User
9. Confirm User Deletion
10. Test Cleanup 

---

##  Tech Stack
- **Language:** Python  
- **Automation Tool:** Playwright  
- **Test Runner:** Pytest  
- **Playwright Version:** 1.41.1  

---

##  Project Setup

1. **Clone the Repository**
   
   git clone https://github.com/<RUTIKAKHOSE> <AccuKnox-user-management-tests>.git
   cd OrangeHRM

2. **Create and Activate Virtual Environment**

   python -m venv .venv
   .\.venv\Scripts\activate   
  
3. **Install Dependencies**

   pip install -r requirements.txt

4. **Install Playwright Browsers**

   playwright install


## How to Run the Test Cases

1. To run a test file:

   pytest QA/automation/tests/test_admin_user_flow.py
 -s
