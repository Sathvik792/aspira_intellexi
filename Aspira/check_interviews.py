from conn.mongodb import *
import datetime
import time
from bot import BOT
from bson import ObjectId
import os
import schedule
import time

# os.makedirs("Interview_Questions", exist_ok=True)


while True:
    print("True")
    interview_data = get_upcoming_meetings_today()
    print("interview_data:  ", interview_data)

    if not interview_data:
        print("No interview data available")
        print("Interview data is empty. WIll fetch again in a minute...")
        time.sleep(10)
        continue

    for item in interview_data:
        name = item.get("name", "No Name")
        meetingTime = item.get("meetingtime", None)
        meeting_link = item.get("meetingurl", "No Meeting Link")
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        datetime_obj = datetime.datetime.strptime(meetingTime, "%Y-%m-%dT%H:%M")
        formatted_meettime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")

        print(current_time, formatted_meettime_str)
        if current_time == formatted_meettime_str:
            print("yes")
            BOT(meet_url=meeting_link,name=name)
        else:
            print("not the time")
        print(
            "next--------------------------------------------------------------------------------"
        )

    schedule.run_pending()
