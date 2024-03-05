from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from datetime import datetime
import json
import ast

from conn.mongodb import (
    get_cat_by_id,
    get_all_categories,
    update_document,
    delete_category_by_id,
    get_files_by_category,
    insert_document
)


categories_bp = Blueprint(
    "cats", __name__, template_folder="templates", static_folder="static"
)
print(categories_bp)


@categories_bp.get("/all-categories")
def documentCategories():
    """
    Render Home Page
    """
    categories = get_all_categories()
    return render_template("documentCategories.html", categories=categories)


@categories_bp.get("/add-category")
def addCategory():
    """
    Render Home Page
    """
    return render_template("addCategory.html")


@categories_bp.get("/category/<id>/")
def viewCategory(id):
    """
    Render Home Page
    """
    category = get_cat_by_id(id)
    print(category)
    return render_template("viewCategory.html", category=category)


@categories_bp.get("/delete-category/<id>/")
def deleteCategory(id):
    """
    Render Home Page
    """
    if get_files_by_category(id):
        delete_category_by_id(id)
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})


@categories_bp.route("/edit-category/<id>", methods=["GET", "POST"])
def editCategoryForm(id):
    """
    Render Home Page
    """
    if request.method == "GET":
        category = get_cat_by_id(id)
        file_type = category["file_type"]
        category_name = category["doc_category_name"]
        conversion_ontology = json.dumps(category.get("conversion_ontology"))
        extraction_ontology = json.dumps(category.get("extraction_ontology"))
        prompt = category.get("prompt_instructions")
        return render_template(
            "editCategory.html",
            id=id,
            category_name=category_name,
            extraction_ontology=extraction_ontology,
            conversion_ontology=conversion_ontology,
            prompt=prompt,
            file_type=file_type,
        )

    elif request.method == "POST":
        doc_category_name = request.form["documentCategory"]
        extraction_ontology = request.form.get("extractionOntology")
        conversion_ontology = request.form.get("conversionOntology")
        prompt_instructions = request.form["promptInstructions"]
        try:
            cleaned_prompt_string = prompt_instructions.strip()
            if conversion_ontology and extraction_ontology:
                cleaned_extraction_string = (
                    extraction_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_conversion_string = (
                    conversion_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_extraction_json_string = ast.literal_eval(
                    cleaned_extraction_string
                )
                cleaned_conversion_json_string = ast.literal_eval(
                    cleaned_conversion_string
                )
                data = {
                    "doc_category_name": doc_category_name,
                    "extraction_ontology": cleaned_extraction_json_string,
                    "conversion_ontology": cleaned_conversion_json_string,
                    "prompt_instructions": cleaned_prompt_string,
                    "Last_Updated": datetime.isoformat(datetime.now()),
                }
            else:
                data = {
                    "doc_category_name": doc_category_name,
                    "prompt_instructions": cleaned_prompt_string,
                    "Uploaded_time": datetime.isoformat(datetime.now()),
                }
            res = update_document(id, data)
            if res:
                return jsonify({"status": True})
            else:
                return jsonify(res)
        except SyntaxError:
            return jsonify({"status": False})
    else:
        return redirect(url_for("doc_category_management"))


# //////////////////////////////////////  FORM SUBMISSIONS  //////////////////////////////////////////////#
@categories_bp.route("/create-doc-category/", methods=["GET", "POST"])
def create_doc_category():
    """
    Get the data from doc_category_management form
    - Document Catgeory Name
    - Extraction Ontology
    - Conversion Ontology
    - Prompt Instructions
    stor in Db and provide ack to user and return to upload page
    """
    if request.method == "POST":
        file_type = request.form.get("fileType")

        if file_type == "pdf":
            doc_category_name = request.form.get("documentCategory")
            extraction_ontology = request.form.get("extractionOntology")
            conversion_ontology = request.form.get("conversionOntology")
            prompt_instructions = request.form.get("promptInstructions")

            try:
                cleaned_extraction_string = (
                    extraction_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_conversion_string = (
                    conversion_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_prompt_string = prompt_instructions.strip()

                cleaned_extraction_json_string = ast.literal_eval(
                    cleaned_extraction_string
                )
                cleaned_conversion_json_string = ast.literal_eval(
                    cleaned_conversion_string
                )

                data = {
                    "doc_category_name": doc_category_name,
                    "extraction_ontology": cleaned_extraction_json_string,
                    "conversion_ontology": cleaned_conversion_json_string,
                    "prompt_instructions": cleaned_prompt_string,
                    "Uploaded_time": datetime.now(),
                    "file_type": file_type,
                }
                res = insert_document(data)
                if res["status"]:
                    return jsonify({"status": True})
                else:
                    return jsonify(res)
            except (SyntaxError, ValueError):
                return jsonify({"status": False})

        elif file_type == "xlsx":
            doc_category_name = request.form.get("documentCategory")
            prompt_instructions = request.form.get("promptInstructions")
            conversion_ontology = request.form.get("conversionOntology")
            try:
                cleaned_conversion_string = (
                    conversion_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_prompt_string = prompt_instructions.strip()
                cleaned_conversion_json_string = ast.literal_eval(
                    cleaned_conversion_string
                )
                data = {
                    "file_type": file_type,
                    "doc_category_name": doc_category_name,
                    "conversion_ontology": cleaned_conversion_json_string,
                    "prompt_instructions": cleaned_prompt_string,
                    "Uploaded_time": datetime.now(),
                }

                res = insert_document(data)
                if res["status"]:
                    return jsonify({"status": True})
                else:
                    return jsonify(res)
            except (SyntaxError, ValueError):
                return jsonify({"status": False})
        elif file_type=="kyc":
            doc_category_name = request.form.get("documentCategory")
            prompt_instructions = request.form.get("promptInstructions")
            conversion_ontology = request.form.get("conversionOntology")
            try:
                cleaned_conversion_string = (
                    conversion_ontology.strip()
                    .replace("\r\n", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                cleaned_prompt_string = prompt_instructions.strip()
                cleaned_conversion_json_string = ast.literal_eval(
                    cleaned_conversion_string
                )
                data = {
                    "file_type": file_type,
                    "doc_category_name": doc_category_name,
                    "conversion_ontology": cleaned_conversion_json_string,
                    "prompt_instructions": cleaned_prompt_string,
                    "Uploaded_time": datetime.now(),
                }

                res = insert_document(data)
                if res["status"]:
                    return jsonify({"status": True})
                else:
                    return jsonify(res)
            except (SyntaxError, ValueError):
                return jsonify({"status": False})
    else:
        return redirect(url_for("doc_category_management"))
