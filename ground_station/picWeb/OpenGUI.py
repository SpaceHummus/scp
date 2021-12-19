from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)
app.run(host='mc-avivlabs.duckdns.org', port=8090)
