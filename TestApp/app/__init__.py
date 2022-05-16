from flask import Flask

#This file tells the Python interpreter that the app directory is a package and should be treated as such.

app = Flask(__name__)
from app import views
