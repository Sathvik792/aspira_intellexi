# from flask import Blueprint,render_template,request,jsonify
# import os
# from llama_index.core import (
#     VectorStoreIndex,
#     ServiceContext,
#     StorageContext,
#     SummaryIndex,
#     # Document,
# )

# from conn.mongodb import get_all_files,get_file_by_id


# rag_bp = Blueprint(
#     "rag", __name__, template_folder="templates", static_folder="static"
# )
# print(rag_bp)


# @rag_bp.get("/query_agent")
# def Rag_agent():
#     try:
#         docs = get_all_files()
#         return render_template("queryagent.html", categories=docs)
#     except Exception as e:
#         return render_template("queryagent.html", categories=[])


# def check_multile_index(index):
#     new_index = index.split(",")
#     multiple_indices = os.listdir("multiple_indices")
#     for each in multiple_indices:
#         ids = each.split("-")
#         if len(ids) == len(new_index):
#             if all(id in new_index for id in ids):
#                 print("yess", ids)
#                 return ids
#     return None


# def create_agent_indices(documents, persist_dir_path, agent_type="simple-agent"):
#     service_context = ServiceContext.from_defaults(chunk_size=1024)
#     if agent_type == "simple-agent":
#         if not os.path.exists(os.path.join(persist_dir_path, "vector_index")):
#             print(
#                 "    Creating Vector Index  on {}".format(
#                     os.path.join(persist_dir_path, "vector_index")
#                 )
#             )
#             nodes = service_context.node_parser.get_nodes_from_documents(documents)
#             vector_index = VectorStoreIndex(nodes)
#             vector_index.storage_context.persist(
#                 persist_dir=os.path.join(persist_dir_path, "vector_index")
#             )
#     else:
#         nodes = service_context.node_parser.get_nodes_from_documents(documents)
#         storage_context = StorageContext.from_defaults()
#         storage_context.docstore.add_documents(nodes)
#         print("summary index   :", os.path.join(persist_dir_path, "summary_index"))
#         if not os.path.exists(os.path.join(persist_dir_path, "summary_index")):
#             summary_index = SummaryIndex(nodes, storage_context=storage_context)
#             summary_index.storage_context.persist(
#                 persist_dir=os.path.join(persist_dir_path, "summary_index")
#             )
#         if not os.path.exists(os.path.join(persist_dir_path, "vector_index")):
#             vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
#             vector_index.storage_context.persist(
#                 persist_dir=os.path.join(persist_dir_path, "vector_index")
#             )


# @rag_bp.get("/create_agent")
# def create_index():
#     doc_id = request.args.get("document", None)
#     agent_type = request.args.get("agent", None)
#     print("==========docid==========", doc_id, agent_type)
#     doc_ids = doc_id.split(",")
#     if len(doc_ids) == 1:
#         print("single doc")
#         single_index_path = os.path.join("indices", doc_id)

#         if not os.path.exists(single_index_path):
#             print("Create the index")
#             file = get_file_by_id(doc_id)
#             docs = []
#             data = file["extracted_text"]
#             for each in data.keys():
#                 docs.append(Document(text=str(data[each])))
#             print("documents==========", len(docs))
#             create_agent_indices(
#                 documents=docs,
#                 persist_dir_path=single_index_path,
#                 agent_type=agent_type,
#             )
#         else:
#             if agent_type == "simple-agent":
#                 indices = 1
#             else:
#                 indices = 2
#             if not len(os.listdir(single_index_path)) >= indices:
#                 file = get_file_by_id(doc_id)
#                 docs = []
#                 data = file["extracted_text"]
#                 for each in data.keys():
#                     docs.append(Document(text=str(data[each])))
#                 print("documents==========", len(docs))
#                 create_agent_indices(
#                     documents=docs,
#                     persist_dir_path=single_index_path,
#                     agent_type=agent_type,
#                 )
#             print("--------Index already exists----")
#         return jsonify({"status": True})
#     elif len(doc_ids) > 1:
#         print("multi docs")
#         docs = []
#         path = check_multile_index(doc_id)
#         print(path)
#         if path:
#             index_path = "-".join(path)
#             if agent_type == "simple-agent":
#                 indices = 1
#             else:
#                 indices = 2
#             multiple_index_path = os.path.join("multiple_indices", index_path)
#             if not len(os.listdir(multiple_index_path)) >= indices:
#                 multiple_index_path = os.path.join("multiple_indices", index_path)
#                 for each in doc_ids:
#                     file = get_file_by_id(each)
#                     docs.append(Document(text=str(file["extracted_text"])))
#                 create_agent_indices(
#                     documents=docs,
#                     persist_dir_path=multiple_index_path,
#                     agent_type=agent_type,
#                 )
#                 return jsonify({"status": True})
#         else:
#             index_path = "-".join(doc_ids)
#             multiple_index_path = os.path.join("multiple_indices", index_path)
#             for each in doc_ids:
#                 file = get_file_by_id(each)
#                 docs.append(Document(text=str(file["extracted_text"])))
#             create_agent_indices(
#                 documents=docs,
#                 persist_dir_path=multiple_index_path,
#                 agent_type=agent_type,
#             )
#             return jsonify({"status": True})
#     return jsonify({"message": "Provide a valid doc Id"})
