import os
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename
from flaskr.db import get_db

ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/upcsv', methods=('GET', 'POST'))
def upcsv():
    if request.method == 'POST':
        quarter = request.form['quarter']
        year = request.form['year']
        filename = request.files['filename'] 

        # check if the post request has the file part
        if 'filename' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            return redirect(url_for('upload.showcsvs'))

    return render_template('upload/upcsv.html')

@bp.route('/showcsvs', methods=('GET', 'POST'))
def showcsvs():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    print(files)
    return render_template('upload/showcsvs.html',files=files)
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

