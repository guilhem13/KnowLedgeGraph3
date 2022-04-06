import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
import json
import os
import shutil
import flask
from flasgger import Swagger, swag_from
from flask import Response, render_template, request, send_from_directory
from waitress import serve
from werkzeug.utils import secure_filename

import AWS.aws as aws
import webappmanager
from bdd.manager_bdd import session_creator
from bdd.paper_model_orm import PapierORM
from knowledgegraph.models.notificationmodel import Notification
from knowledgegraph.controller.treatment.processingpipeline import Textprocessed

session = session_creator()
app = flask.Flask(__name__)
swagger = Swagger(app)
app.config["UPLOAD_FOLDER"] = "."


############################### get ner entities from one pdf  ########################################
# Route where the client wants to get ner from an uploading pdf


@app.route("/getner", methods=["GET", "POST"])
@swag_from("swagger/get_ner.yml")
def upload_file():
    """Endpoint returning list of Entities based on
    AWS Comprehend service
    """
    if request.method == "POST":
        if "file" not in request.files:  # no file part
            return Response(
                Notification("1", "No file part").message(),
                status=400,
                mimetype="application/json",
            )
        else:
            file = request.files["file"]  # No selected file
            if file.filename == "":
                return Response(
                    Notification("400", "No selected file").message(),
                    status=400,
                    mimetype="application/json",
                )
            else:
                if file and webappmanager.allowed_file(
                    file.filename
                ):  # Check if the file has the correct extension
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    ners = aws.Awsner(4900).get_entities(
                        Textprocessed(None).get_data_from_file(filename)
                    )
                    os.remove(filename)
                    if ners == True: 
                        return Response(
                        Notification("400", "Problem with the AWS credentials").message(),
                        status=400,
                        mimetype="application/json",
                    )
                    else:
                        return json.dumps(ners)
                else:
                    return Response(
                        Notification("3", "File type not permitted").message(),
                        status=400,
                        mimetype="application/json",
                    )
    return render_template("index.html")


############################### manage bdd ########################################


@app.route("/arxiv/sizebdd")
@swag_from("swagger/arxiv_sizebdd.yml")
def size_of_bdd():
    nbrows = session.query(PapierORM).count()
    return Response(
        Notification("200", "number of papers " + str(nbrows)).message(),
        status=200,
        mimetype="application/json",
    )


@app.route("/arxiv/feedbdd/<nb_paper>")
@swag_from("swagger/arxiv_feedbdd.yml")
def injestpaper(nb_paper):
    webappmanager.feed_bdd(int(nb_paper), session)
    return Response(
        Notification("200", "papers had been injested in database").message(),
        status=200,
        mimetype="application/json",
    )


############################### Request directly from arxiv########################################
@app.route("/arxiv/pipeline/<nb_paper>")
@swag_from("swagger/arxiv_pipeline.yml")
def create_pipeline_from_arxiv(nb_paper):
    try:
        base_path ="knowledgegraph/owl/onto10_done.owl" 
        if os.path.isfile(base_path):
            os.remove(base_path)
            shutil.copyfile("knowledgegraph/owl/onto_template.owl","knowledgegraph/owl/onto10.owl")
        webappmanager.pipeline_from_arxiv(nb_paper) 
        os.rename("knowledgegraph/owl/onto10.owl","knowledgegraph/owl/onto10_done.owl")
        return send_from_directory(app.config['UPLOAD_FOLDER'],base_path, as_attachment=True)

    except Exception as e : 
        return Response(
            Notification(
                "400", e
            ).message(),  
            status=404,
            mimetype="application/json",
        )

############################### get_ontology ########################################

@app.route("/get/ontology")
@swag_from("swagger/get_ontology.yml")
def get_files():
    base_path ="knowledgegraph/owl/onto10_done.owl"
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'],base_path, as_attachment=True)
        
    except FileNotFoundError:
        return Response(
            Notification(
                "404", "FileNotFound"
            ).message(),  
            status=404,
            mimetype="application/json",
        )




############################### Error handler ########################################
# route for error 500
@app.errorhandler(500)
def internal_server_errors(error):
    return Response(
        Notification(
            "404",
            "error :/ Internal Server Error",
        ).message(),
        status=404,
        mimetype="application/json",
    )


# route for error 404
@app.errorhandler(404)
def internal_server_error(error):
    return Response(
        Notification(
            "404",
            "Sorry wrong endpoint.This endpoint doens't exist. Check your endpoint or your id arguments",
        ).message(),
        status=404,
        mimetype="application/json",
    )


##########################################################################################

session.close()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
