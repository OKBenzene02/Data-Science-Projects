# Home page
from pages import app
from flask import render_template, url_for, request, redirect, flash
import os
from werkzeug.utils import secure_filename

app.secret_key = "random_secret_key"

app.config['UPLOAD_FOLDER'] = 'C:\\Python Learning\\Python Learning\\Current Python learning\\image content recognizer\\pages\\static\\uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_html():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded')
            return render_template('home.html', image_name=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)


    return render_template("home.html", image_name=None)

@app.route('/about')
def about_html():
    return render_template('about.html')

@app.route('/contributors')
def contributors_html():
    return render_template('contributors.html')