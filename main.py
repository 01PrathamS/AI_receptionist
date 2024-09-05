import os 
from groq import Groq 
import chromadb

def search_vector(user_input): 

    client = chromadb.PersistentClient("emergency_vector_data")

    collection = client.get_collection(name="emergency_ai")

    results = collection.query(
        query_texts=[user_input],
        n_results=1
    )

    # check if the distance is less than 0.5 then return the document
    if results['distances'][0][0] > 0.5: 
        return results['documents'][0]
    
    return None 

def call_llm_groq(user_input, context):

    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"you're an ai receptionist,don't add anything your self and answer user_question based only on context, don't add anything your self.USER_QUESTION: {user_input},CONTEXT: {context}"
        }], 
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    return response 

def classify_emergency(user_input):

    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY')
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"check if the given text is medical emergency or not: {user_input}, Answer strictly in 'yes' or 'no'"
        }], 
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    return response 