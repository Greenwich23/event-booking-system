# login_controller.py
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import re
import sys
import sqlite3
from Controllers.UserDashboard import UserDashboard
from Controllers.AdminDashboard import AdminDashboard
from database.database import get_db_connection

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        loadUi("GUIs/EMSLoginPage.ui", self)
        self.loginButton = self.findChild(QPushButton, "logInBtn")
        self.signUpButton = self.findChild(QPushButton, "signUpBtn")
        self.email = self.findChild(QLineEdit, "emailField")
        self.password = self.findChild(QLineEdit, "passwordField")
        self.errorLabel = self.findChild(QLabel, "errorLabel")
        # self.firstwindow = UserDashboard()
        # self.secondwindow = AdminDashboard()
        # self.secondwindow.hide()

        self.loginButton.clicked.connect(self.handle_login)
        self.signUpButton.clicked.connect(self.gotosignuppage)
        self.open()
        print("ran the log in page")

    def handle_login(self):
        emailField = self.email.text().strip().lower()
        passwordField = self.password.text().strip()

        email_regex = r"\S+@\S+\.[a-zA-Z]{2,}"
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_]).{8,}$"

        if not emailField or not passwordField:
            self.errorLabel.setText("Please fill in all fields.")
            return

        if not re.match(email_regex, emailField):
            self.errorLabel.setText("Invalid email format.")
            return

        if not re.match(password_regex, passwordField):
            self.errorLabel.setText("Password must contain \n letters, \n numbers, and symbols.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT fullname, role FROM Users
                WHERE email = ? AND password = ?
            """, (emailField, passwordField))

            user = cursor.fetchone()


            if user:
                fullname, role = user
                print(f"✅ Logged in: {fullname} ({role})")

                if role == "admin":
                    self.hide()
                    AdminPage = AdminDashboard()
                    AdminPage.exec_()
                    AdminPage.show()
                else:
                    self.hide()
                    UsersPage = UserDashboard()
                    UsersPage.exec_()
                    UsersPage.show()

            else:
                self.errorLabel.setText("User does not exist.")

        except Exception as e:
            print("❌ Database error:", e)
            self.errorLabel.setText("Something went wrong. Try again later.")
        finally:
            conn.close()

    def gotosignuppage(self):
        from Controllers.SignUpController import SignUpWindow
        self.hide()
        signUpPage = SignUpWindow()
        signUpPage.exec_()
        signUpPage.show()



