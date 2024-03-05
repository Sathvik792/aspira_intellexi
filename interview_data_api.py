from fastapi import FastAPI
app = FastAPI()
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import os
from PIL import Image
from Intellexi.conn.mongodb import (
    get_all_files,
    schedule_kyc,
    get_all_kyc_files,
    get_all_interviews,
    set_extracted,
    check_details,
    get_format_details
)
from GPT.gpt import summary_fn
import json


def convert_pdf_to_image(pdf_path, page=1, dpi=200):
    # Convert the specified page of the PDF to an image
    print("------------------------",pdf_path)
    images = convert_from_path(pdf_path, dpi=dpi, first_page=page, last_page=page)

    # Return the image
    return images[0] if images else None


def extract_text_from_file(file_path):
    image=convert_pdf_to_image(pdf_path=file_path)
    image.save("image.png")
    ocr=PaddleOCR(use_angle_cls=True)
    res=ocr.ocr("image.png",cls=True)
    extracted_text=""
    print("             res                  ",res)
    for idx in range(len(res)):
        line = res[idx]
        print(type(res))
        for each in line:
            print(type(each), each[-1][0])
            extracted_text+="\n"+each[-1][0]
    print(extracted_text)
    return extracted_text


def extract_user_details(doc_id):
    print("extarcted the sier details---------------------------------", doc_id)
    is_extracted,file_path = check_details(doc_id)
    complete_file_path=os.path.join("Intellexi",file_path)
    print("----------extarcted or not------------", is_extracted,file_path,complete_file_path)
    if is_extracted:
        print("is already extarcted ---------")
    #     pass
    else:
        print("extarct now ----------------")
        category=get_format_details(doc_id)
        format = category["conversion_ontology"]
        prompt = category["prompt_instructions"]
        text = extract_text_from_file(complete_file_path)
        print(" ----------------          text    ----------------")
        formatted_text=summary_fn(input_text=text,prompt=prompt,format_string=format)
        # do the extarction
        print("formatted text is --------------",formatted_text)
        result=formatted_text["result"]
        try:
            json_result=json.loads(result)
            set_extracted(doc_id,json_data=json_result)
            print("------------added data to db-------")
        except json.JSONDecodeError:
            print("json error is caught")
            valid_json=result.replace("'", '"')
            json_result=json.loads(valid_json)
            print("     valid     jsonified ",json_result)
            set_extracted(doc_id,json_data=json_result)
        finally:
            return {"status":True}



@app.get("/get_data/{doc_id}")
async def read_root(doc_id):
    res=extract_user_details(doc_id)
    print("returning---------------",res)
    return {"message": res}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
