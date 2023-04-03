import flask
from flask import Flask, render_template, redirect

app = Flask(__name__)

from flight import routes