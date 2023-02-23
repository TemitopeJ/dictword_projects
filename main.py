from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
Bootstrap(app)


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Go')


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    result = None
    header = None
    if form.validate_on_submit():
        search_term = form.search.data
        # Perform search using search_term
        print(search_term)
        url = os.getenv('URL')
        key = os.getenv('X-RapidAPI-Key')
        Host = os.getenv('X-RapidAPI-Host')

        querystring = {
            "term": search_term
        }

        header = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": Host
        }
        responses = requests.get(url, headers=header, params=querystring)

        data = responses.json()
        results = data['list'][0]['definition']
        result = results.get('definition', 'Definition not found')

        header = f"Your word is: {search_term}"
    return render_template("index.html", form=form, result=result, header=header)


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)



