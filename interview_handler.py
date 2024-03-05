import sys
import os
from pdf2image import convert_from_path

import dlib
import cv2
import face_recognition
from Aspira.interview import Interview
import time
from Aspira.bot import BOT

os.makedirs("extracted_faces", exist_ok=True)
os.makedirs("loan_applications", exist_ok=True)

# Add the parent directory to the Python path

# Now you should be able to import modules from the sibling directory
from Intellexi.conn.mongodb import get_upcoming_interviews,get_file_by_id
from datetime import datetime,timedelta
import pandas as pd


class KYC:
    def __init__(self, id, file_path=None,image_path=None) -> None:
        self.id = id
        self.file_path=file_path
        self.image_path = image_path
        self.face_cascade=cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.detector=dlib.get_frontal_face_detector()
        self.all_detected_faces=[]
        os.makedirs(f"screnshots/{self.id}/detected_faces",exist_ok=True)
    
    def extractfaces(self,path=None):

        if self.file_path and self.file_path.endswith(".pdf"):
            os.makedirs(f"pdf_images/{self.id}", exist_ok=True)
            images = convert_from_path(self.file_path,  dpi=200, first_page=1, last_page=1)
            if images:
                images[0].save(f"pdf_images/{self.id}/image.png")
            print("Extarcted the image")

            path=f"pdf_images/{self.id}/image.png"
        os.makedirs(f"extracted_faces/{self.id}", exist_ok=True)
        if path:
            image = cv2.imread(path)
        else:
            image=cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        # Extract faces and save them
        for i, (x, y, w, h) in enumerate(faces):
            face = image[y : y + h, x : x + w]
            cv2.imwrite(f"extracted_faces/{self.id}/{i}.jpg", face)
            print(f"Face {i+1} extracted and saved successfully!")
            path=f"extracted_faces/{self.id}/{i}.jpg"
            self.all_detected_faces.append(path)
        return self.all_detected_faces
    
    def match_face(self,meeting_screenshot_path):
        matches=False
        each=self.all_detected_faces[0]
        print(each)
        reference_image = face_recognition.load_image_file(each)
        try:
            reference_encoding = face_recognition.face_encodings(reference_image)[0]
        except :
            pass
        image = cv2.imread(meeting_screenshot_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.detector(gray)
        print(faces)
        print("----------------")
        for face in faces:
            print(face)
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            face_image = image[y : y + h, x : x + w]
            face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            face_encoding = face_recognition.face_encodings(face_image_rgb)
            cv2.imwrite("face_image_{face}.jpg", face_image)
            if len(face_encoding) > 0:
                match = face_recognition.compare_faces(
                    [reference_encoding], face_encoding[0]
                )
                if match[0]:
                    print("Match found! This is the reference face.")
                    cv2.imshow("matched", face_image)
                    cv2.imwrite("matched_image",face_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # return True
                    matches=True
                else:
                    print("No match found.")
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("-------------matched atleat once ------------",matches)
        return matches

    def start_interview(self):
        interview=Interview(questions_excel_sheet_path="path")
        interview.start_interview()

    def extract_all_faces_from_meeting(self):
        ss_path=f"screenshots/{self.id}"
        screenshots=os.listdir(ss_path)
        for each in screenshots:
            print(each)
            self.match_face(meeting_screenshot_path=os.path.join(f"screenshots/{self.id}",each))
            
            
    def fill_answers(self,details):
            full_name=details["full_name"]
            date_of_birth=details["date_of_birth"]
            gender=details["gender"]
            print(full_name,date_of_birth,gender)
            df=pd.read_excel(io="kyc_template.xlsx")
            print(df.head())
            df["Actual Answer"]=[full_name,date_of_birth,gender]
            df.to_excel("answered.xlsx")
            
    def create_loan_application_questionaire(self):
        answered=pd.read_excel("answered.xlsx")
        answered_questions=answered["Question"]
        answered_answers=answered["Actual Answer"]
        loan_application=pd.read_excel("loan_application.xlsx")
        loan_application_questions=loan_application["Question"]
        loan_application_answers=loan_application["Answer"]

        print("-"*10)
        print(answered_questions,answered_answers)
        print(type(answered_questions),type(answered_answers))    
        concatenated_questions=pd.concat([answered_questions,loan_application_questions],ignore_index=True)
        print("-================================")
        print(type(concatenated_questions))
        
        concatenated_answers=pd.concat([answered_answers,loan_application_answers],ignore_index=True)
        print("*************************************************************88")
        print(concatenated_answers)
        print(type(concatenated_answers))
        
        df=pd.DataFrame({"Question":concatenated_questions,"Answer":concatenated_answers})
        df.to_excel(f"loan_applications/{self.id}.xlsx",index=None)
        print(df.head())

    

while True:
    current_datetime=datetime.now()
    print("True")
    interviews = get_upcoming_interviews()
    print("interview_data:  ", interviews)
    if not interviews:
        print("No interview data available")
        print("Interview data is empty. WIll fetch again in a minute...")
        time.sleep(10)
        continue
    for interview in interviews:
        interview_id=interview["_id"]
        print(interview_id)
        
        interview_time=interview["interviewtime"]
        print(type(interview_time),interview_time.day)
        if interview_time.day==current_datetime.day:
            if not os.path.exists(f"interview_questions/{interview_id}"):
                print("initiate KYC")
                document_details=get_file_by_id(id=interview["doc_id"])
                print("document details---------------",document_details)
                file_path=document_details["file_path"]
                complete_file_path=os.path.join("Intellexi",file_path)
                print("file is at================",complete_file_path)
                kyc=KYC(id=interview_id,file_path=complete_file_path)
                kyc.extractfaces()
                kyc.fill_answers(document_details["extracted_data"])
                kyc.create_loan_application_questionaire()
                print("KYC doc generated")
            if interview_time.hour==current_datetime.hour:
                print("any minute now")
                user_name=document_details["extracted_data"]["full_name"]
                print("--------------",user_name)
                meeting_link=interview["meetingurl"]
                if interview_time.minute==current_datetime.minute+1 or interview_time.minute==current_datetime.minute:
                    print("is in a minute wiating here ")
                    time.sleep(1)
                    BOT(meet_url=meeting_link, name=user_name,interview_id=interview_id)
                    print("need to start the interview")
                    # processing Meeting images
                    kyc.extract_all_faces_from_meeting()
                    print("processed the images from meeting")
        else:
            print("not today===============")
            pass
    
