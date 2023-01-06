from datetime import datetime

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import workdays as wd
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")
# Press the green button in the gutter to run the script.


@app.route("/putni")
def putni_troskovi():
    workdays = []
    year = datetime.now().year
    month = datetime.now().month
    for d in wd.get_workdays(year, month, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
        workdays.append(d.strftime("%d-%m-%Y"))
    workdays = wd.order_days(workdays)


if __name__ == '__main__':
    app.run()
