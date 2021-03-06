from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from wtforms import BooleanField, StringField, PasswordField, IntegerField, validators
from flask_wtf import FlaskForm
from flask_login import current_user
import db_functions


class RegistrationForm(FlaskForm):
    username = StringField(
        'Jméno*:', [validators.DataRequired(message='Bez jména to nepůjde.')])
    surname = StringField(
        'Příjmení*:', [validators.DataRequired(message='Bez příjmení to nepůjde.')])
    street = StringField('Ulice,č.p./č.o.:')
    city = StringField(
        'Město/Obec*:', [validators.DataRequired(message='Vyplň město, kde bydlíš.')])
    postcode = IntegerField('PSČ*:', [validators.DataRequired(message='Bez PSČ to nepůjde.'),
                                      validators.Length(min=5, max=5, message='PSČ zadej bez mezer.')])
    email = StringField('E-mail*:', [validators.DataRequired(message='Bez mailu to nepůjde.', ),
                                     validators.Email(message='Chybný tvar emailové adresy.'), validators.Length(message="Email musí mít mezi 4 a 250 znaky.", min=4, max=250)])
    phone = StringField('Telefon*:', [validators.DataRequired(message='Bez telefonního čísla to nepůjde.'), validators.Length(
        min=11, max=11, message='Telefonní číslo zadej bez předvolby a ve tvaru xxx xxx xxx.')])
    password = PasswordField('Heslo*:', [validators.DataRequired(message='Bez hesla to nepůjde.'), validators.EqualTo(
        'confirm_password', message='Hesla se musejí shodovat.'), validators.Length(min=8, message='Heslo musí být alespoň 6 znaků dlouhé.')])
    confirm_password = PasswordField(
        'Potvrzení hesla*:', [validators.DataRequired(message='Zadané heslo je třeba potvrdit.')])
    gdpr = BooleanField('Souhlasím ze zpracováním osobních údajů.*', [validators.DataRequired(
        message='Bez udělení Tvého souhlasu Tě nemůžeme zaregistrovat.')])


blueprint = Blueprint('registration_bp', __name__)


@blueprint.route('/registrace')
def show_registration():
    user = current_user
    form = RegistrationForm()

    if user.is_authenticated:
        flash('Už jsi přihlášen.', "danger")
        return redirect(url_for('races_bp.show_races'))
    return render_template('registration.html', values={}, form=form)


@blueprint.route('/registrace', methods=['POST', 'GET'])
def add_new_user():
    form = RegistrationForm()

    if form.validate_on_submit():
        already_registered = db_functions.find_user(form.email.data)
        if already_registered:
            flash('Už jsi u nás byl/a, tak se prosím přihlaš.', "danger")
            return redirect(url_for('login_bp.login'))

        if not form.password.data == form.confirm_password.data:
            flash('Hesla se neshodují.', "danger")
            return render_template("registration.html", form=form)

        id_user = db_functions.add_user(
            form.username.data,
            form.surname.data,
            form.street.data,
            form.city.data,
            form.postcode.data,
            form.email.data,
            form.phone.data,
            form.password.data,
            form.confirm_password.data
        )

        if id_user:
            flash('Vítáme Tě! Teď se prosím přihlaš.', "success")
            return redirect(url_for('login_bp.login'))
        else:
            flash(
                'Mrzí nás to, ale registrace se nepovedla. Dej nám pár minut a zkus to znovu.', "danger")
            return render_template("registration.html", form=form)
    else:
        return render_template("registration.html", form=form)
