from flask import Flask, request, render_template, redirect, url_for

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZ724'

# Flask-Bootstrap requires this line
Bootstrap(app)

class ConfForm(FlaskForm):
    name = StringField('Which actor is your favorite?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def main():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = ConfForm()
    if request.method == 'GET':
        form.name.data = "123"
        return render_template('test_form.html', form=form, message = "")
    else:
        print(form.name.data)
        return render_template('test_form.html', form=form, message = "Data saved!")

@app.route('/template')
def form():
    return render_template('test_template.html', name="Avi")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)