from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3
from Controllers.UserDashboard import UserDashboard
from Controllers.AdminDashboard import AdminDashboard
import re
from database.database import get_db_connection

class SignUpWindow(QDialog):
    def __init__(self, parent=None):
        super(SignUpWindow, self).__init__(parent)
        loadUi("GUIs/EMSSignUpPage.ui", self)
        self.loginButton = self.findChild(QPushButton, "login_btn")
        self.signUpButton = self.findChild(QPushButton, "signup_btn")
        self.fullname = self.findChild(QLineEdit, "fullnameField")
        self.email = self.findChild(QLineEdit, "emailField")
        self.password = self.findChild(QLineEdit, "passwordField")
        self.errorLabel = self.findChild(QLabel, "errorLabel")

        self.signUpButton.clicked.connect(self.handleSignUp)
        self.loginButton.clicked.connect(self.gotologinpage)

    def handleSignUp(self):
        fullnameField = self.fullname.text().strip()
        emailField = self.email.text().strip().lower()
        passwordField = self.password.text().strip()

        email_regex = r"\S+@\S+\.[a-zA-Z]{2,}"
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[\W_]).{8,}$"

        conn = get_db_connection()
        cursor = conn.cursor()

        if not fullnameField or not emailField or not passwordField:
            self.errorLabel.setText("All fields are required!")
            return

        if not re.match(email_regex, emailField):
            self.errorLabel.setText("Invalid email format.")
            return

        if not re.match(password_regex, passwordField):
            self.errorLabel.setText("Password must contain letters, numbers, and \n symbols.")
            return

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (emailField,))
        existing_user = cursor.fetchone()

        if existing_user:
            QMessageBox.warning(self, "Error", "Email already registered!")
            conn.close()
            return

        # Insert new user
        cursor.execute(
            "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)",
            (fullnameField, emailField, passwordField, "user")
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Account created successfully!")
        self.gotologinpage()  # Optionally redirect to login page



    def gotologinpage(self):
        from Controllers.LoginController import LoginWindow
        self.hide()
        loginPage = LoginWindow()
        loginPage.exec_()
        loginPage.show()
