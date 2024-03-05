from flask import Flask, render_template,send_file
from categories import categories_bp
from uploadedDocs import documents_bp
# from rag import rag_bp
from interviews import interviews_bp

# utils
import os
from flask_cors import CORS
from zipfile import ZipFile
import json
import ast



# DB based data (Intellexi)
from conn.mongodb import (
    dashboard_data,
    get_cat_by_id,
    get_file_by_id,
    delete_file_by_id,

)  
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

app.register_blueprint(categories_bp)
app.register_blueprint(documents_bp)
# app.register_blueprint(rag_bp)
app.register_blueprint(interviews_bp)

os.makedirs("indices",exist_ok=True)

os.makedirs("multiple_indices", exist_ok=True)

@app.get("/")
def index():
    """
    Render Dashboard Page
    """
    print("yes")
    total_documents, processed, inprogress, not_processed = dashboard_data()
    simple_agents = len(os.listdir("indices"))
    query_agents = len(os.listdir("multiple_indices"))
    total_agents = simple_agents + query_agents
    # categories = get_all_categories()
    return render_template(
        "dashboard.html",
        total_documents=total_documents,
        processed=processed,
        error=not_processed,
        inprogress=inprogress,
        total_agents=total_agents,
    )


# Download category
@app.get("/download_category/<id>/")
def download_category(id):
    """
    download the category data
    -> if file_type : PDF [ ontologies and prompts]
    -> if file_type : xlsx [prompt]

    => new method
            Write the whole data into the json irrespective of filetype
    """
    temp_dir = "temp_download"
    os.makedirs(temp_dir, exist_ok=True)

    file_paths = []
    data = get_cat_by_id(id)

    file_path = os.path.join(temp_dir, "category.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2, default=str)
    file_paths.append(file_path)

    zip_file_path = "downloaded_files.zip"
    with ZipFile(zip_file_path, "w") as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))

    for file_path in file_paths:
        os.remove(file_path)

    os.rmdir(temp_dir)
    return send_file(zip_file_path, as_attachment=True)


# sending multiple files
@app.get("/download_multiple_files/<id>/")
def download_multiple_files(id):
    temp_dir = "temp_download"
    os.makedirs(temp_dir, exist_ok=True)

    file_paths = []
    data = get_file_by_id(id)

    file_path = os.path.join(temp_dir, "extracted_data.json")
    with open(file_path, "w") as file:
        json.dump(data.get("extracted_text"), file, indent=2, default=str)
    file_paths.append(file_path)

    file_path = os.path.join(temp_dir, "formatted_data.json")
    try:
        with open(file_path, "w") as file:
            if isinstance(data.get("formatted_data"), dict):
                json.dump(data.get("formatted_data"), file, indent=2, default=str)
            elif isinstance(data.get("formatted_data"), str):
                formatted_text = ast.literal_eval(data.get("formatted_data"))
                json.dump(formatted_text, file, indent=2)
    except:
        pass

    file_paths.append(file_path)

    zip_file_path = "downloaded_files.zip"
    with ZipFile(zip_file_path, "w") as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))

    for file_path in file_paths:
        os.remove(file_path)

    os.rmdir(temp_dir)
    return send_file(zip_file_path, as_attachment=True)


@app.get("/delete_file/<id>/")
def delete_document(id):
    delete_file_by_id(id)
    return jsonify({"status": True})


if __name__=="__main__":
    app.run(debug=True)
