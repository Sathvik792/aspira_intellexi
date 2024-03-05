from flask import Blueprint, jsonify, render_template, request
import os
from datetime import datetime
from conn.mongodb import (
    insert_file,
    get_all_docs,
    get_all_files,
    get_cat_by_id,
    get_file_by_id,
    delete_file_by_id,
)
from dotenv import load_dotenv
load_dotenv()
 
upload_folder = os.getenv("UPLOAD_FOLDER")
os.makedirs(upload_folder,exist_ok=True)
documents_bp = Blueprint(
    "docs", __name__, template_folder="templates", static_folder="static"
)


@documents_bp.get("/uploaded_docs")
def all_uploaded_documents():
    """
    Tabular view for presenting with all uploaded docs
    """
    print_prcesses()
    try:
        docs = get_all_files()
        return render_template("uploadedDocs.html", docs=docs)
    except:
        return render_template("uploadedDocs.html", docs=[])


@documents_bp.get("/document/<id>")
def viewDocument(id):
    document = get_file_by_id(id)
    category = get_cat_by_id(document["category_id"])
    return render_template("viewDocument.html", document=document, category=category)


@documents_bp.route("/upload_document", methods=["GET", "POST"])
def upload_document_form():
    """
    Form to upload document and show the user with extracted and formatted text
    """
    if request.method == "GET":
        doc_categories = get_all_docs()
        return render_template("uploadDoc.html", categories=doc_categories)
    elif request.method == "POST":
        category_id = request.form["documentCategory"]
        file = request.files["file"]
        file.save(os.path.join(upload_folder, file.filename))
        file_path = os.path.join(upload_folder, file.filename)

        data = {
            "category_id": category_id,
            "file_path": file_path,
            "Uploaded_time": datetime.now(),
        }
        res = insert_file(data)
        return jsonify(res)


@documents_bp.get("/delete_file/<id>/")
def delete_document(id):
    delete_file_by_id(id)
    return jsonify({"status": True})


def print_prcesses():
    # for thread in ALL_THREADS:
    #     print(thread)
    pass
