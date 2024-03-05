from Intellexi.conn.mongodb import get_upcoming_interviews
import datetime
import time

upcoming_interviews = get_upcoming_interviews()
print("           MAIN DB CALL ")
while True:
    Break=False
    time.sleep(1)
    if not upcoming_interviews:
        time.sleep(3)
        print("            DB CALL because no inetrviews    ")
        upcoming_interviews=get_upcoming_interviews()

    current_date=datetime.datetime.now()

    for interview in upcoming_interviews:
        meetingTime=interview["interviewtime"]
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M")
        # print("current--------------           ",current_time)
        datetime.datetime.strptime
        formatted_meettime_str = meetingTime.strftime("%Y-%m-%d %H:%M")
        print(current_time," --------------           ",formatted_meettime_str)
        if current_time == formatted_meettime_str:
            print("yes")
            print("will fetch again after this")
            Break=True
            break
            
            upcoming_interviews = get_upcoming_interviews()

            # BOT(meet_url=meeting_link,name=name)
        else:
            print("not the time")
    if Break:
        break