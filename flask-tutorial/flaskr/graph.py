import base64
from io import BytesIO

from matplotlib.figure import Figure

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('graph', __name__, url_prefix='/graph')

@bp.route('/showInstance')
def showInstance():
    file = request.args.get('filename')
    fig = Figure()
    fig.suptitle(file)
    ax = fig.subplots()
    ax.plot([1,2])
    buf = BytesIO()
    fig.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return render_template('graph/showInstance.html', data=data)


