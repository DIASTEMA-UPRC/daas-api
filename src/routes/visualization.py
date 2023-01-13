import json

from flask import Blueprint, request

from utils.db import get_db_connection
from utils.message import send_message

visualization = Blueprint("visualization", __name__)


@visualization.route("/", methods=["POST"])
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

    collection = db["Diastema"]["Visualization"]
    match = collection.find_one({"job-id": job})

    if match:
        db.close()
        return "Job ID already exists", 400

    collection.insert_one({ "job-id": job, "status": "progress", "result": "completed" })
    db.close()

    try:
        send_message("visualization", data)
    except:
        return "Failed to submit Visualization job", 500

    return "JoVisualizationin job submitted", 200


@visualization.route("/progress", methods=["GET"])
def visualization_progress():
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

        collection = db["Diastema"]["Visualization"]
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


@visualization.route("/<job>", methods=["GET"])
def visualization_job(job):
    try:
        db = get_db_connection()
    except:
        return "Internal server error", 500

    collection = db["Diastema"]["Visualization"]
    match = collection.find_one({"job-id": job})

    if not match:
        return "Job ID doesn't exist", 404

    return "completed", 200
