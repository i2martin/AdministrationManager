from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()




