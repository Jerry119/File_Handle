import os
from flask import Flask, request, render_template, flash, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/samliu/Desktop/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jepg', 'gif'])

app = Flask(__name__)
app.secret_key = 'random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if 'file' not in request.files:
        flash("no selected file")
        return redirect('/')
    f = request.files['file']
    if not allowed_file(f.filename):
        flash('the extension format is not allowed')
        return redirect('/')
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('file is uploaded successfully')
    return redirect('/')

@app.route('/download', methods=["GET", "POST"])
def download_file():
    try:
        filename = request.form['filename']
    except:
        filename = None

    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except:
        flash('can not find the file')
        return redirect('/')

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

@app.route('/display', methods=["GET", "POST"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    file_info = []
    for file in files:
        file_info.append(file + " -- " + convert_bytes(os.path.getsize(app.config['UPLOAD_FOLDER'] + '/' + file)))
    return render_template("display.html", file_info=file_info)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    try:
        filename = request.form['filename']
    except:
        filename = None

    path = app.config['UPLOAD_FOLDER'] + "/" + filename

    if os.path.exists(path):
        os.remove(path)
    else:
        flash("can not find the file")
    return redirect('/')

