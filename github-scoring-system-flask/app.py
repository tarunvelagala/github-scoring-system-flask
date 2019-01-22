from ssl import CertificateError
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
app.static_folder = 'static'


class Searchform(FlaskForm):
    url = URLField(
        validators=[DataRequired(message='Please enter a URL')])


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', )
def hello_world():
    form = Searchform()
    return render_template('index.html', form=form)


def process(url):
    gh_score = 0
    forked_commits = 0
    url_name = requests.get(url + '?tab=repositories')
    bsObj = BeautifulSoup(url_name.content, 'lxml')
    url_parse_obj = urlparse(url)
    if url_parse_obj:
        gh_score += 10
    url_rel = url_parse_obj.scheme + '://' + url_parse_obj.netloc + url_parse_obj.path
    repo_list = bsObj.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public fork"})
    for rl in repo_list:
        url_commits = url_rel + '/' + rl.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'lxml')
        c = soup_commits.find('span', {"class": 'num text-emphasized'})
        cc = c.get_text().strip()
        cc = cc.replace(",", "")
        forked_commits += int(cc)
        if forked_commits > 5:
            gh_score += 20
            break
    original_commits = 0
    for rl in bsObj.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public source"}):
        url_commits = url_rel + '/' + rl.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'html.parser')
        c = soup_commits.find('span', {"class": 'num text-emphasized'})
        cc = c.get_text().strip()
        cc = cc.replace(",", "")
        original_commits += int(cc)
        if original_commits > 10:
            gh_score += 20
            break
    return gh_score


@app.route('/success', methods=['POST'])
def success():
    form = Searchform()
    if request.method == 'POST':
        url = request.form.get('url')
        if form.validate_on_submit():
            try:
                gh_score = process(url)
            except (URLError, CertificateError, HTTPError) as e:
                flash(str(e.__class__.__name__) + '.Please enter a valid URL', 'info')
                return redirect(url_for('hello_world'))
            # process(url)
            return render_template('success.html', gh_score=gh_score)


if __name__ == '__main__':
    app.run()
