import os

from flask import Flask, flash, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

import pandas as pd  # CSV reading library
import matplotlib.pyplot as plt  # plotting library
import matplotlib.dates as mdates


app = Flask("MyCommuteApp")

app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'
app.config['IMAGE_FOLDER'] = 'static/images'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['IMAGE_FOLDER']):
    os.makedirs(app.config['IMAGE_FOLDER'])

# ROUTES DEFINITION


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    # Get the file from the data form.
    uploaded_file = request.files['file']

    # Redirect back home if the user does not select
    # a file
    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Secure store the file on disk.
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('commute', data_file=filename))

    return redirect("/")


@app.route("/commute/<data_file>")
def commute(data_file=None):

    if data_file is not None and os.path.splitext(data_file)[1].lower() == '.csv':
        history = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], data_file))
    else:
        return redirect("/")

    try:
      date = pd.to_datetime(history.Date, infer_datetime_format=True)
      plt.plot(date, history.Balance)
    except AttributeError:
      print("The CSV does not follow the expected format.")
      return redirect("/")

    # Set up the plot
    plt.title("Balance")
    plt.xlabel("Date")
    plt.ylabel("GBP")

    # Tweak the axis a bit to be readable
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    image_filename = os.path.splitext(data_file)[0] + '.png'
    plt.savefig(os.path.join(app.config['IMAGE_FOLDER'], image_filename))

    new_image_file = "/{}/{}".format(app.config['IMAGE_FOLDER'], image_filename)

    return render_template("data.html", image_file=new_image_file)


# Check to not let people upload anything else that we can process
def allowed_file(filename):
    allowed_extensions = set(['.txt', '.csv', '.pdf', '.png', '.jpg', '.jpeg', '.gif'])

    if os.path.splitext(filename)[1].lower() in allowed_extensions:
        return True
    else:
        return False


app.run(debug=True)
