# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, render_template
import db_funkce



blueprint = Blueprint('zavody_bp', __name__)

# Zaregistruje funkci show_about() jako funkci, kterou má Flask zavolat, když 
# uživatel otevře v prohlížeči stránku "/about"
@blueprint.route('/zavody')
def show_zavody():
    # Zavolá funkci render_template(), která vezme template about.html a
    # vygeneruje výsledné HTML, které vrátí jako výsledek z téhle funkce zpátky
    # do Fasku, a ten ji pošle k uživateli do prohlížeče.
    zavody = db_funkce.zavody()
    return render_template('zavody.html', zavody=zavody)
