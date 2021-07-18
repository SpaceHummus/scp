"""test Flask with this"""

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello World!'

@app.route('/template')
def form():
    return render_template('test_template.html', name="Avi")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)