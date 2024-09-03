import asyncio 
import time 
import os 
from groq import Groq 

def call_llm_groq(user_input):

    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "you are an ai_receptionist who is commited to respond in emergency situation for, EMERGENCY:" + str(user_input) + "do not respond which is not medical emergency responding I'm not aware of that please resuggest"
            }
        ], 
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    return response 

async def emergency_or_message():
    user_input = input("Are you in an emergency or would you like to leave a message?")
    if user_input == "message": 
        input("Please leave a message: ")
        print("Thank you for the message, we will forward it to the Dr. Adrin")
    else: 
        emergency = input("Please tell me, what's happening?: ")
        return emergency
    return None 

async def call_llm(emergency):
    print("Calling to Database")
    await asyncio.sleep(10) 
    response = call_llm_groq(emergency) 
    print(response)

async def hold_for_second(): 
    await asyncio.sleep(0.1)
    print("Please hold for a second........")

async def making_conversation(): 
    user_area = input("I'm checking what you should do immediately, meanwhile can you tell me which area are you located right now?")
    print(f"Dr. Adrin will be coming {user_area} immediately, in 10 minutes")

async def main(): 
    # node 1: confirm if the user is in an emergency or would like to leave a message
    response = await emergency_or_message()
    
    # node 2: if the user is in an emergency, call the emergency services
    if response is not None:
        task1 = asyncio.create_task(call_llm(response)) 
        task2 = asyncio.create_task(making_conversation())
        await task2 
        user_status = input("arrival be too late?")
        if user_status == "yes":
            task3 = asyncio.create_task(hold_for_second())
            await task1
        else: 
            print("Dr. Adrin will be coming immediately")


if __name__ == "__main__": 
    asyncio.run(main())