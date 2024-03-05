from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from datetime import datetime
import json
import ast
import threading
import time
from pdf2image import convert_from_path
from conn.mongodb import (
    get_all_files,
    schedule_kyc,
    get_all_kyc_files,
    get_all_interviews,
    set_extracted,
    check_details,
    get_format_details
)
# from gpt import summary_fn
import requests


interviews_bp = Blueprint(
    "interviews", __name__, template_folder="templates", static_folder="static"
)
print(interviews_bp)


@interviews_bp.get("/schedule_interview")
def schedule_interview():
    """
    signup Screen for user to Register,
    """
    print("rendering")
    docs = get_all_kyc_files()
    print(docs)
    return render_template("schedule_interview.html", documents=docs)


@interviews_bp.get("/all_interviews")
def Interviews():
    """
    signup Screen for user to Register,
    """
    print("rendering")
    interviews = get_all_interviews()
    print(interviews)
    return render_template("interviews.html", interviews=interviews)


def get_data(doc_id):
    res=requests.get(f"http://127.0.0.1:8000/get_data/{doc_id}")
    if res.ok:
        return True
    
@interviews_bp.route("/create_interview", methods=["GET", "POST"])
def create_interview():
    doc_id = request.form["documents"]
    interview_time = request.form["interviewTime"]
    print("-------------", interview_time)

    schedule_kyc(
        kyc_details={
            "doc_id": doc_id,
            "interviewtime": datetime.strptime(interview_time, "%Y-%m-%dT%H:%M"),
            "meetingurl": "https://meet.google.com/bzr-sjyn-bkq",
        }
    )
    background_thread = threading.Thread(target=get_data, args=(doc_id,))
    background_thread.start()
    return jsonify({"status": True})
