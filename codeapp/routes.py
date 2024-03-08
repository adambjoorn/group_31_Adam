# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

from codeapp.models import EuropeSalesRecords

# internal imports
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")
def home() -> Response:
    dataset: list[EuropeSalesRecords] = get_data_list()
    priority_count: dict[str, int] = calculate_statistics(dataset)
    return render_template("home.html", priority_count=priority_count)


@bp.get("/image")
def image() -> Response:
    dataset: list[EuropeSalesRecords] = get_data_list()
    priority_count: dict[str, int] = calculate_statistics(dataset)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(
        list(priority_count.values()),
        labels=[str(label) for label in priority_count],
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.axis("equal")
    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:
    dataset: list[EuropeSalesRecords] = get_data_list()
    return jsonify(dataset)


@bp.get("/json-stats")
def get_json_stats() -> Response:
    dataset: list[EuropeSalesRecords] = get_data_list()
    stats: dict[str, int] = calculate_statistics(dataset)
    return jsonify(stats)
