import csv
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename
from flaskr.db import get_db

ALLOWED_EXTENSIONS = {'csv'}

# map headings from CSV to column names in the survey_datapoints table
HEADING_MAP = {
    "Timestamp" : "response_timestamp",
    "I will probably complete the survey" : "will_complete",
    "Failures are treated as learning opportunities" : "fail_learn_opportunity",
    "Responsibilities are shared" : "responsibility_shared",
    "Cross-functional collaboration is encouraged and rewarded" : "collab_rewarded",
    "New ideas are welcomed" : "ideas_welcomed",
    "Unbiased information is actively sought" : "info_sought",
    "Failures lead to inquiry rather than punishment or shame" : "failures_shame_free",
    "Our Source Control Management tools easily support my work" : "scm_works",
    "Our build and task-running tools easily support my work" : "task_runners_work",
    "Our package and artifact management tools easily support my work" : "artifact_managment_works",
    "Integrating my work with other components or services is simple" : "integration_is_simple",
    "I can easily make the changes I care about without unintended side effects" : "changes_simple_safe",
    "Changes made by others rarely cause problems for my work" : "changes_distinct",
    "It is easy for me to discover information about what has changed in the environments services or components I depend on" : "changes_clear",
    "It is easy for me to understand how to release my changes" : "releases_simple",
    "It is easy for me to specify the details of the environment in which my service will operate" : "env_cfg_easy",
    "It is easy for me to create the necessary environment(s) for developing and operating my service" : "env_startup_easy",
    "I have access to the compute storage or network resources I need for developing or operating my service" : "resources_available",
    "I can easily access environments that allow me to experiment safely" : "safe_experimental_envs",
    "My experimental environments are easy to use" : "easy_experimental_envs",
    "I understand or can easily reference policies standards and common procedures" : "policies_clear",
    "I usually apply policies standards and common procedures to my work" : "policies_usable",
    "It is easy for me to find information about how builds and operates our product and its supporting systems" : "policies_discoverable",
    "I understand the intent of policies standards and common procedures" : "policies_meaningful",
}
# map Likert scale responses to numbers
LIKERT_MAP = {
    "Strongly Agree" : 5,
    "Agree" : 4,
    "Neither Agree nor Disagree" : 3,
    "Disagree" : 2,
    "Strongly Disagree" : 1
}

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/upcsv', methods=('GET', 'POST'))
def upcsv():
    if request.method == 'POST':
        # TODO: check these by regex
        quarter = request.form['quarter']
        year = request.form['year']
        file_obj = request.files['filename']

        survey_instance_name = (file_obj.filename).split('.')[0] #drop the extension

        db = get_db()
        has_instance = db.execute(
           f'SELECT COUNT(*) as count FROM survey_instances WHERE quarter="{quarter}" AND year="{year}"'
            ).fetchone()['count']
        if not has_instance:
            db.execute(
                f'INSERT INTO survey_instances(instance_name, quarter, year) VALUES("{survey_instance_name}", "{quarter}", "{year}")'
            )
            db.commit()
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
            insert_csv(os.path.join(upload_folder, filename), quarter, year)
            return redirect(url_for('upload.showcsvs'))

    return render_template('upload/upcsv.html')

def insert_csv(file_path, quarter, year):
    fieldnames = list(HEADING_MAP.values())
    db = get_db()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            # original survey made the practice question optional;
            # assume non-answers are 'Strongly Disagree'
            if(row['will_complete'] ==''):
                row['will_complete'] = 'Strongly Disagree'
            resp_values = [LIKERT_MAP[row[x]] if x != "response_timestamp" else str(row[x]) for x in fieldnames]
            resp_values[0] = f"'{resp_values[0]}'"

            insert = f"""
                INSERT INTO survey_datapoints ({",".join(fieldnames)},quarter,year)
                VALUES ({",".join([str(x) for x in resp_values])},"{quarter}","{year}")"""
            db.execute(insert)
        db.commit()


@bp.route('/showcsvs', methods=('GET', 'POST'))
def showcsvs():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('upload/showcsvs.html',files=files)
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

