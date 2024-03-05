# Whole process of Interview should be handled from Here.
"""
-> Get the interview schedule
-> Check for the interview time and start the interview when its time
-> When Interview time is reached 
    -> Invoke the bot to join the meeting
    -> Bot Check (if any())
    -> Load the questions and start the interview
    -> When a question is asked :
        - if user responds: evaluate the response
            -   If completely answered move to next question
        - else : 
            - ask a follow up question:
                -- repeat the if block
    -> if all questions a re asked
        - End the interview     
    -> else:
        continue
"""
from bot import BOT

if __name__ == "__main__":
    BOT(meet_url="https://meet.google.com/ioh-setr-ppu", name="Sathwik")
    
    