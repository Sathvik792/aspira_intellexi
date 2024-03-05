import pymongo
from datetime import datetime

mongo_uri = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_uri)


def add_meeting(meeting_details):
    try:
        db = client.get_database("DEMO-MEETING")
        collection = db["meetings"]
        result = collection.insert_one(meeting_details)
        print("Inserted record ID:", result.inserted_id)
        client.close()
        return result.inserted_id
    except Exception as e:
        print(f"error : {e}")


def get_upcoming_meetings_today():
    db = client.get_database("DEMO-MEETING")
    collection = db["meetings"]

    current_datetime = datetime.now()
    print("Current datetime:", current_datetime)

    query = {"meetingtime": {"$gte": current_datetime.isoformat()}}

    # Execute query
    upcoming_meetings = collection.find(query)

    return list(upcoming_meetings)
