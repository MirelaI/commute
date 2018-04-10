import os

from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

app = Flask("MyCommuteApp")

app.config['UPLOAD_FOLDER'] = 'static/images'

#ROUTES DEFINITION

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    # Get the file from the data form.
    file = request.files['file']

    # Redirect back home if the user does not select
    # a file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Secure store the file on disk.
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('commute', data_file=filename))

    return redirect("/")

# Here Joost to add bunch of code to do magic
# ....you can process the date using
@app.route("/commute/<data_file>")
def commute(data_file=None):

    # We need to tell our template from where to get
    # the generated image file. So this image file
    # at this point will need to point to the newly
    # generated image
    new_image_file = None
    if new_image_file:
        new_image_file = "/{}/{}".format(app.config['UPLOAD_FOLDER'], data_file)

    return render_template("data.html", image_file=new_image_file)

# UTILS
# Check to not let people upload anything else that we can process
def allowed_file(filename):
    allowed_extensions = set(['txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in allowed_extensions


app.run(debug=True)
