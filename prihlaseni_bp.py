from flask import Blueprint, current_app, request, render_template, redirect, url_for, flash, abort
# from myapp.models import User
from hashlib import sha512
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from wtforms import Form, TextField, PasswordField, validators, HiddenField
# https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/
# pip install flask-wtf flask-login
from db_funkce import najdi_uzivatele

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


class LoginForm(Form):
    email = TextField('email', [validators.Required(), validators.Length(min=4, max=25)])
    password = PasswordField('heslo', [validators.Required(), validators.Length(min=6, max=200)])


blueprint = Blueprint('prihlaseni_bp', __name__)

@blueprint.route('/prihlaseni', methods=['GET', 'POST'])
def login():
    next = get_redirect_target()
    #print(next)
    form = LoginForm(request.form)

    if request.method == 'POST':
        # TODO: validace poli formulare??

        email = request.form["email"]
        heslo = request.form["heslo"]
        uzivatel = najdi_uzivatele(email)
        # uspesne_prihlasen = False
        if uzivatel:
            if sha512(heslo.encode()).hexdigest() != uzivatel.password_hash:
                flash ('Špatně zadané heslo.', "danger")
            elif sha512(heslo.encode()).hexdigest() == uzivatel.password_hash:
                if login_user(uzivatel, force=True):
                    flash ('Uživatel byl úspěšně přihlášen.', "success")
                    if next.endswith('prihlaseni') or next.endswith('registrace') or 'noveheslo' in next:
                        return redirect(url_for('zavody_bp.show_zavody'))
                    return redirect(next)
        if not uzivatel:
            flash ("Zadaný e-mail není v naší databázi. Nejprve se, prosím, zaregistruj.", "danger")
        

    # TODO: při neúspěšném pokusu o přihlášení zachovat ve formuláři zadaný email??
    return render_template('prihlaseni.html', form=form)

@blueprint.route('/odhlaseni')
def logout():
    logout_user()
    return redirect(url_for('main.show_index'))
