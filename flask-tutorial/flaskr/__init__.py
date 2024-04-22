import os
import base64

from io import BytesIO

from flask import Flask

from matplotlib.figure import Figure


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/graph')
    def graph():
    	# Generate the figure **without using pyplot**.
    	fig = Figure()
    	ax = fig.subplots()
    	ax.plot([1, 2])
    	# Save it to a temporary buffer.
    	buf = BytesIO()
    	fig.savefig(buf, format="png")
    	# Embed the result in the html output.
    	data = base64.b64encode(buf.getbuffer()).decode("ascii")
    	return f"<img src='data:image/png;base64,{data}'/>"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

