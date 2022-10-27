import json
import requests
import pandas as pd

from flask import Blueprint, request
from urllib.request import HTTPBasicAuthHandler
from io import StringIO

from utils.db import get_db_connection
from utils.message import send_message

data_ingesting = Blueprint("data-ingesting", __name__)


@data_ingesting.route("/", methods=["POST"])
def index():
    data = request.data

    try:
        job = str(json.loads(data)["job-id"])
    except:
        return "Invalid JSON", 400

    try:
        db = get_db_connection()
    except:
        return "Internal server error", 500

    collection = db["Diastema"]["DataIngesting"]
    match = collection.find_one({"job-id": job})

    if match:
        db.close()
        return "Job ID already exists", 400

    collection.insert_one({ "job-id": job, "status": "progress", "result": "" })
    db.close()

    try:
        js = json.loads(data)

        if "minio-input" in js:
            send_message("data-loading", data)
        else:
            send_message("data-ingesting", data)
    except:
        return "Failed to submit Data Ingesting job", 500

    return "Data Ingesting job submitted", 200


@data_ingesting.route("/progress", methods=["GET"])
def data_ingesting_progress():
    result = {}
    code = 200

    try:
        job = request.args.get("id")

        if not job:
            raise Exception("Missing ID argument")

        try:
            db = get_db_connection()
        except:
            raise Exception("Failed to connect to database")

        collection = db["Diastema"]["DataIngesting"]
        match = collection.find_one({"job-id": job})
        db.close()

        if not match:
            raise Exception("Job ID doesn't exist")

        status = match["status"]
        
        if status == "error":
            result = {
                "job-id": job,
                "status": status,
                "message": match["message"]
            }
            code = 400
        else:
            result = {
                "job-id": job,
                "status": status
            }
    except Exception as ex:
        result = {
            "status": "error",
            "message": str(ex)
        }
        code = 400

    return result, code


@data_ingesting.route("/<job>", methods=["GET"])
def data_ingesting_job(job):
    try:
        db = get_db_connection()
    except:
        return "Internal server error", 500

    collection = db["Diastema"]["DataIngesting"]
    match = collection.find_one({"job-id": job})

    if not match:
        return "Job ID doesn't exist", 404

    return match["result"], 200


@data_ingesting.route("/test", methods=["POST"])
def data_ingesting_test():
    data = request.data

    try:
        data = json.loads(data)
    except:
        return "Invalid JSON", 400

    url = data.get("url")
    # method = data.get("method")
    token = data.get("token")
    separator = data.get("separator")
    first_line_labels = data.get("first-line-labels")
    labels = data.get("labels")

    if token == "":
        auth = HTTPBasicAuthHandler("apikey", token)
    else:
        auth = None

    df = pd.DataFrame()

    try:
        with requests.get(url, auth=auth) as r:
            r.raise_for_status()
            file_data = r.content.decode("utf-8")
            
            if first_line_labels:
                df = pd.read_csv(StringIO(file_data), sep=separator)
            else:
                df = pd.read_csv(StringIO(file_data), sep=separator, header=None, names=labels)
    except Exception as e:
        return str(e), 400

    return df.head(10).to_html(), 200
