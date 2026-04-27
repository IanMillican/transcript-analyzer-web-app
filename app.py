from flask import Flask, render_template, request, redirect, url_for, jsonify
import tempfile
import os
import json

from domain.service.transcript_service import parse_transcript
from exceptions.parsing_exception import ParsingException
from exceptions.invalid_argument import InvalidArgumentException
from exceptions.degree_writer_error import DegreeWriterException
from domain.service.degree_service import get_degree, get_degree_list, pretty_print_degree
from domain.service.evaluator_service import evaluate_transcript
from data_access.repository.degree_writer import write_degree

def createApp():
    app = Flask(__name__, template_folder="template", static_folder="static")
    return app

app = createApp()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload/", methods=["POST"])
def upload():
    file = request.files.get("transcript")
    path = None
    if file is None or file.filename == "":
        return render_template("index.html", error="No file selected")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            file.save(temp.name)
            path = temp.name
        transcript = parse_transcript(path)
        degree = get_degree("data_access/config/requirements/bsc.json")
        result = evaluate_transcript(transcript, degree)
    except (ParsingException, InvalidArgumentException) as e:
        return render_template("index.html", error=str(e))
    finally:
        if path and os.path.exists(path):
            os.remove(path)

    return render_template("transcript_preview.html", result=result)

@app.route("/create-degree/", methods=["GET", "POST"])
def create_degree():
    if request.method == "POST":
        new_degree = request.get_json()
        overwrite = new_degree.pop('overwrite', False)
        try:
            write_degree(new_degree, allow_overwrite=overwrite)
            return jsonify({"redirect": "/"}), 200
        except DegreeWriterException as e:
            return jsonify({"error": str(e)}), 400
    else:
        return render_template("create_degree.html")

@app.route("/create-section/", methods=["GET"])
def create_section():
    return render_template("create_section.html")

@app.route("/edit-degree/", methods=["GET"])
def edit_degree():
    filename = request.args.get('file_path')
    if filename:
        with open(f"data_access/config/requirements/{filename}") as f:
            degree = json.load(f)
        return render_template("edit_degree_form.html", degree=degree, filename=filename)
    else:
        degree_list = get_degree_list()
        return render_template("edit_degree.html", degree_list=degree_list)

@app.route("/edit-degree-form/", methods=["GET"])
def edit_degree_form():
    filename = request.args.get('file_path')
    if filename:
        with open(f"data_access/config/requirements/{filename}") as f:
            degree = json.load(f)
        return render_template("edit_degree_form.html", degree=degree, filename=filename)
    return redirect(url_for('edit_degree'))

@app.route("/export/", methods=["POST","GET"])
def export():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5001)