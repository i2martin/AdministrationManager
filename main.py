import os
import time
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, widgets, SelectMultipleField, HiddenField, FieldList
from wtforms.validators import DataRequired
import workdays as wd
import honorarium_excel as he
import travel_excel as te

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# TODO - add validators
class PutniTroskovi(FlaskForm):
    km_arrival = StringField('arrival')  # integerfield --> ne može se korigirati size/length??
    km_return = StringField('return')  # integerfield --> ne može se korigirati size/length??
    vehicle = SelectField('vehicle', choices=["Osobni automobil", "Autobus", "Vlak"])
    #checkbox = MultiCheckboxField('checkbox', choices=[''], render_kw={"onclick": "change(this)"})
    #checkbox_tag = HiddenField('checkbox')
    submit = SubmitField(label="Preuzmi", id='submit')

# TODO - add validators
class Honorari(FlaskForm):
    subject = StringField('subject')
    class_tag = StringField('class-tag')
    hours = StringField('date')  # integerfield --> ne može se korigirati size/length??
    submit = SubmitField(label="Preuzmi", id='submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/putni", methods=["GET", "POST"])
def putni_troskovi():
    if request.method == "POST":
        print(request.form)
        print(request.data)
        te.travel(request.form.to_dict(flat=False))
        return "<h1> Done! </h1>"
    else:
        workdays = []
        year = datetime.now().year
        month = datetime.now().month
        for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
            workdays.append(d.strftime("%d.%m.%Y"))
        workdays = wd.order_days(workdays)
        number_of_workdays = len(workdays)
        form = PutniTroskovi()
        return render_template("putni.html", form=form, workdays=workdays, number_of_workdays=number_of_workdays)


@app.route("/honorari", methods=["GET", "POST"])
def honorari():
    if request.method == "POST":
        he.honorarium(request.form.to_dict(flat=False))
        return send_from_directory(directory='static', path='files/temp_files/tablica-honorari.xlsx')
    else:
        workdays = []
        year = datetime.now().year
        month = datetime.now().month
        for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
            workdays.append(d.strftime("%d.%m.%Y"))
        workdays = wd.order_days(workdays)
        workdays = wd.only_date(workdays)
        number_of_workdays = len(workdays)
        forms = []
        for i in range(0, 5):
            form = Honorari()
            forms.append(form)
        return render_template("honorari.html", forms=forms, workdays=workdays, number_of_workdays=number_of_workdays)


if __name__ == '__main__':
    app.run(debug=True)
