"""
Provides an interface for the MongoDB database
"""

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime

load_dotenv()

connection = os.getenv("MONGODB_CONN")
client = MongoClient(connection)
db = client.get_database("Intellexi")
collection_docs = db.doc_category
collection_files = db.files
collection_interviews = db.interviews

collection_docs.create_index([("doc_category_name", 1)], unique=True)


def insert_document(data):
    """
    create a new document category
    """
    try:
        inserted_id = collection_docs.insert_one(data).inserted_id
        return {"status": True, "inserted_id": inserted_id}
    except DuplicateKeyError:
        return {"status": False, "message": "Document with the name already exists"}


def get_cat_by_id(id):
    """
    Return a document category with id
    """
    return collection_docs.find_one({"_id": ObjectId(id)})


def get_all_docs():
    """
    Return the doc_category_name of all the document categories
    """
    docs = collection_docs.find({}, {"doc_category_name": 1})
    return docs


def get_all_categories():
    """
    return all the categories
    """
    docs = list(collection_docs.find())
    return docs


def update_document(id, data):
    """
    Update a document category with data
    """
    doc = collection_docs.update_one({"_id": ObjectId(id)}, {"$set": data})
    return True


def get_files_by_category(category_id):
    """
    return True if there are no files dependent on the category_id else return False
    """
    files = list(collection_files.find({"category_id": category_id}))
    if len(files) > 0:
        return False
    else:
        return True


def insert_file(data):
    """
    insert a new file
    """
    try:
        inserted_id = collection_files.insert_one(data).inserted_id
        return {"status": True, "id": str(inserted_id)}
    except DuplicateKeyError:
        return {"status": False, "message": "Document with the name already exists"}


def delete_category_by_id(id):
    """
    delete category with id
    """
    category = collection_docs.delete_one({"_id": ObjectId(id)})
    return True


def get_file_by_id(id):
    """
    Return a File with id
    """
    file = collection_files.find_one({"_id": ObjectId(id)})
    category_doc = collection_docs.find_one({"_id": ObjectId(file["_id"])})
    if category_doc:
        file["category_name"] = category_doc.get("doc_category_name")
    return file


def get_all_files():
    """
    Return all the files with there associated document category names
    """
    docs = list(collection_files.find({}))
    docs_list = []
    for file_doc in docs:
        category_id = file_doc["category_id"]
        id = ObjectId(category_id)
        category_doc = collection_docs.find_one({"_id": id})
        if category_doc:
            file_doc["category_name"] = category_doc.get("doc_category_name")
            file_doc["docCategory"] = category_doc
            file_doc["file_name"] = os.path.split(file_doc["file_path"])[1]
            docs_list.append(file_doc)
    # print(docs_list[0].keys())
    return docs_list


def add_extracted_formatted_data(id, data: dict):
    """
    add the extracted and the formatted text that is returned by OpenAI API in the DB Collection
    """
    record = collection_files.update_one({"_id": ObjectId(id)}, {"$set": data})
    if record.modified_count > 0:
        return True
    else:
        return False


def delete_file_by_id(id):
    """
    delete the file with id
    """
    file = collection_files.delete_one({"_id": ObjectId(id)})
    return True


def dashboard_data():
    files = list(collection_files.find({}))
    not_processed = []
    processed = []
    error = []

    for file in files:
        formatted_data = file.get("formatted_data", None)
        if formatted_data:
            formatted_data = str(formatted_data).lower()

            if "error" in formatted_data:
                error.append(file)
            elif len(formatted_data) > 2:
                processed.append(file)
        else:
            not_processed.append(file)
            print("=========", not_processed, len(not_processed))
    print(len(files), len(processed), len(not_processed), len(error))
    return len(files), len(processed), len(not_processed), len(error)


def schedule_kyc(kyc_details: dict):
    try:
        inserted_id = collection_interviews.insert_one(kyc_details).inserted_id
        return {"status": True, "id": inserted_id}
    except Exception as e:
        print("Error {}".format(e))




def get_upcoming_interviews():
    current_datetime = datetime.now()
    query = {"interviewtime": {"$gte": current_datetime}}
    upcoming_interviews = collection_interviews.find(query)
    return list(upcoming_interviews)


def get_all_kyc_files():
    kyc_categories = list(collection_docs.find({"file_type": "kyc"}))
    print(kyc_categories)
    print("*" * 20)
    all_kyc_documents = []
    for each in kyc_categories:
        category_id = str(each["_id"])
        kyc_documents = collection_files.find({"category_id": category_id})
        for doc in kyc_documents:
            all_kyc_documents.append(doc)
    print(all_kyc_documents)
    return all_kyc_documents


def get_all_interviews():
    interviews_list = collection_interviews.find()
    interviews = []
    try:
        for interview in interviews_list:
            print(interview)
            file = collection_files.find_one({"_id": ObjectId(interview["doc_id"])})
            print(file)
            interview["file_name"] = file["file_path"]
            interview["extracted_data"] = file.get("extracted_data", None)
            interviews.append(interview)
        print(interviews_list)
        return list(interviews)
    except Exception as e:
        print("Error is ", e)
        return []


def set_extracted(doc_id, json_data):
    collection_files.update_one(
        {"_id": ObjectId(doc_id)}, {"$set": {"extracted_data": json_data}}
    )
    print("updated doc extarcted status")


def check_details(doc_id):
    file = collection_files.find_one({"_id": ObjectId(doc_id)})
    print("---------file is -       %%%%%%%%%%%%%5          ", file)
    return file.get("extracted_data", None), file.get("file_path", None)


def get_format_details(doc_id):
    category_id = collection_files.find_one({"_id": ObjectId(doc_id)})["category_id"]
    print(category_id)
    category = collection_docs.find_one({"_id": ObjectId(category_id)})
    print(category)
    return category
