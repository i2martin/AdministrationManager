from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, SelectField, widgets, SelectMultipleField
# from wtforms.validators import DataRequired
import workdays as wd
import honorarium_excel as he
import travel_excel as te
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    organisation = db.Column(db.String(1000))


with app.app_context():
    Bootstrap(app)
    db.create_all()
    login_manager.init_app(app)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# TODO - add validators
class PutniTroskovi(FlaskForm):
    km_arrival = StringField('arrival')  # integerfield --> ne može se korigirati size/length??
    km_return = StringField('return')  # integerfield --> ne može se korigirati size/length??
    vehicle = SelectField('vehicle', choices=["Osobni automobil", "Autobus", "Vlak"])
    submit = SubmitField(label="Preuzmi", id='submit')


# TODO - add validators
class Honorari(FlaskForm):
    subject = StringField('subject')
    class_tag = StringField('class-tag')
    hours = StringField('date')  # integerfield --> ne može se korigirati size/length??
    submit = SubmitField(label="Preuzmi", id='submit')


@app.route("/")
def home():
    flash('Logged in successfully.')
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    # TODO: Add checks (i.e. existing username) so that it doesn't crash
    if request.method == "POST":
        new_user = User(
            username=request.form.get('username'),
            password= generate_password_hash(password=request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
            organisation=request.form.get('organisation')
        )
        print(new_user.username)
        print(new_user.password)
        print(new_user.organisation)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("putni_troskovi"))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: Add checks (i.e. existing username) so that it doesn't crash
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Find user by username entered.
        user = User.query.filter_by(username=username).first()
        # Check stored password hash against entered password hashed.
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('putni_troskovi'))
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/putni", methods=["GET", "POST"])
@login_required
def putni_troskovi():
    workdays = []
    year = datetime.now().year
    month = datetime.now().month
    for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
        workdays.append(d.strftime("%d.%m.%Y"))
    workdays = wd.order_days(workdays)
    number_of_workdays = len(workdays)
    if request.method == "POST":
        te.travel(request.form.to_dict(flat=False), workdays)
        return send_from_directory(directory='static', path='files/temp_files/tablica-prijevoz.xlsx')
    else:
        form = PutniTroskovi()
        return render_template("putni.html", form=form, workdays=workdays, number_of_workdays=number_of_workdays)


@app.route("/honorari", methods=["GET", "POST"])
@login_required
def honorari():
    workdays = []
    year = datetime.now().year
    month = datetime.now().month
    for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
        workdays.append(d.strftime("%d.%m.%Y"))
    workdays = wd.order_days(workdays)
    workdays = wd.only_date(workdays)
    number_of_workdays = len(workdays)
    if request.method == "POST":
        he.honorarium(request.form.to_dict(flat=False), workdays)
        return send_from_directory(directory='static', path='files/temp_files/tablica-honorari.xlsx')
    else:
        forms = []
        for i in range(0, 5):
            form = Honorari()
            forms.append(form)
        return render_template("honorari.html", forms=forms, workdays=workdays, number_of_workdays=number_of_workdays)


if __name__ == '__main__':
    app.run(debug=True)
