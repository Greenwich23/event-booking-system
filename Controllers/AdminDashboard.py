from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3
import re

class AdminDashboard(QMainWindow) :
    def __init__(self, parent=None):
        super(AdminDashboard, self).__init__(parent)
        loadUi("SIMLoginScene.ui", self)
