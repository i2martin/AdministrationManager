from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
import workdays as wd
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
class PutniTroskovi(FlaskForm):
    km_arrival = IntegerField('arrival')
    km_return = IntegerField('return')
    vehicle = SelectField('vehicle', choices=["Osobni automobil", "Autobus", "Vlak"])
    signature = StringField('signature')
    submit = SubmitField('submit')

@app.route("/")
def home():
    return render_template("index.html")
# Press the green button in the gutter to run the script.

forms = []

@app.route("/putni", methods=["GET", "POST"])
def putni_troskovi():
    if request.method == "POST":
        print(request.form)
        return "<h1> Done! </h1>"
    else:
        workdays = []
        year = datetime.now().year
        month = datetime.now().month
        for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
            workdays.append(d.strftime("%d.%m.%Y"))
        workdays = wd.order_days(workdays)
        number_of_workdays = len(workdays)
        forms = []
        for i in range(0, number_of_workdays):
            form = PutniTroskovi()
            forms.append([form, workdays[i]])
        return render_template("putni.html", forms=forms, workdays=workdays)


if __name__ == '__main__':
    app.run()
