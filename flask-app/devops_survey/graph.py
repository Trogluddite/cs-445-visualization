import base64
from io import BytesIO

import matplotlib.pyplot as plt

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from devops_survey.db import get_db

bp = Blueprint('graph', __name__, url_prefix='/graph')
plt.switch_backend('Agg') #don't draw GUI windows that won't be seen

Q_HEADINGS = [
    "will_complete",
    "fail_learn_opportunity",
    "responsibility_shared",
    "collab_rewarded",
    "ideas_welcomed",
    "info_sought",
    "failures_shame_free",
    "scm_works",
    "task_runners_work",
    "artifact_managment_works",
    "integration_is_simple",
    "changes_simple_safe",
    "changes_distinct",
    "changes_clear",
    "releases_simple",
    "env_cfg_easy",
    "env_startup_easy",
    "resources_available",
    "safe_experimental_envs",
    "easy_experimental_envs",
    "policies_clear",
    "policies_usable",
    "policies_discoverable",
    "policies_meaningful",
]

@bp.route('/showInstance')
def showInstance():
    file = request.args.get('filename')
    instance_name = file.split('.')[0]
    averages = get_averages(instance_name)

    fig = plt.figure(figsize=(9,7))
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.3)
    bars = plt.bar( averages.keys(), averages.values(), color="blue", width=0.7)

    # set red/yellow/green based on arbitrary thresholds
    for b in bars:
        if b.get_height() >= 3.8:
            b.set_color('darkgreen')
        elif b.get_height() < 3.8 and b.get_height() > 2.8:
            b.set_color('khaki')
        else:
           b.set_color('crimson')

    plt.xlabel(xlabel='Question Shortname', fontsize='x-large')
    plt.ylabel(ylabel='Average Response Score', fontsize='x-large')
    plt.xticks(rotation=45,ha='right')
    plt.title(instance_name)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    plt.close()
    return render_template('graph/showInstance.html', data=data)

def get_averages(survey_instance_name):
    db = get_db()
    row_count = db.execute(
        f"""
        SELECT COUNT(*) as count FROM survey_datapoints AS sd
        LEFT JOIN survey_instances AS si
        ON sd.quarter = si.quarter AND sd.year = si.year
        WHERE si.instance_name = '{survey_instance_name}'
        """
    ).fetchone()['count']

    counts_dict = {}
    for k in Q_HEADINGS:
        counts_dict[k] = 0

    survey_rows = db.execute(
        f"""
        SELECT * FROM survey_datapoints AS sd
        LEFT JOIN survey_instances AS si
        ON sd.quarter = si.quarter AND sd.year = si.year
        WHERE si.instance_name = '{survey_instance_name}'
        """
    )

    for r in survey_rows:
        for h in Q_HEADINGS:
            counts_dict[h] += int(r[h])
    # convert counts to averages
    for h in Q_HEADINGS:
        counts_dict[h] = counts_dict[h] / row_count;

    return counts_dict

