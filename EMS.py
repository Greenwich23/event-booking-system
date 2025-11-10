from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3
import re
from Controllers.LoginController import LoginWindow
from database.database import initialize_database


def main():
    app = QApplication(sys.argv)
    # initialize_database()
    # Launch the login window first
    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
