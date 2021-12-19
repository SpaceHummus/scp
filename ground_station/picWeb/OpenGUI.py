from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)
app.run(host='0.0.0.0', port=8090)
