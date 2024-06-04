import replicate
import sqlite3
import openai
import json
import re
# Connect to the SQLite database and set up for full-text search
conn = sqlite3.connect('vectors.db')
cursor = conn.cursor()


def get_context_from_vector_db(user_query):
    # Connect to the SQLite database
    conn = sqlite3.connect('vectors.db')
    cursor = conn.cursor()

    # Split the user query into words and form a SQL query that can match any of these words
    words = user_query.split()
    query = "SELECT vector FROM vector_fts WHERE " + ' OR '.join(["vector LIKE ?" for _ in words])
    params = ['%' + word + '%' for word in words]  # Create parameters for SQL query
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    # Initialize an empty dictionary to aggregate results
    aggregated_dict = {}

    # Aggregate JSON data from each row fetched
    for row in results:
        vector_data = json.loads(row[0])
        for key, value in vector_data.items():
            if key in aggregated_dict:
                aggregated_dict[key] += value
            else:
                aggregated_dict[key] = value

    # Close the database connection
    cursor.close()
    conn.close()
    
    # Convert the resulting dictionary back to a JSON string if needed
    resulting_json = json.dumps(aggregated_dict)

    return resulting_json

def get_context_summary(context_data, focus_keywords, frequency_threshold=10):
    # Convert the stringified JSON back to a dictionary
    data = json.loads(context_data)
    
    # Filter data based on focus keywords and high frequency
    relevant_data = {
        key: value for key, value in data.items() if any(keyword in key.lower() for keyword in focus_keywords) or value > frequency_threshold
    }
    
    # Generate a summary from the filtered data
    summary = ", ".join(f"{key}: {value}" for key, value in relevant_data.items() if value > 0)  # Still assuming values are numeric and non-zero
    
    return summary

def extract_keywords(user_query):
    
    keywords = re.findall(r'\b\w{4,}\b', user_query.lower())
    return keywords



def query_llama_2_70b_chat(user_query):
        context = get_context_from_vector_db(user_query)
        focus_keywords = extract_keywords(user_query)
        context_summary = get_context_summary(context, focus_keywords)
        print(focus_keywords)
        print(context_summary)
        prompt = f"Based on the information: {context_summary} \nHow would you answer the user's query about: {user_query}?"
        print(f"Prompt: {prompt}")  # Check what the prompt looks like
       
        full_response = ""
       
       
        
        result =  replicate.run(
            "meta/llama-2-70b-chat",
            input={
        "top_k": 50,
        "top_p": 1,
        "prompt": prompt,
        "temperature": 0.5,
        "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        "max_new_tokens": 500,
        "min_new_tokens": -1
    },
        )
        print(result)
        full_response = ''.join(result)
        print(full_response)
        return(full_response)
       
def query_falcon(user_query):
        context = get_context_from_vector_db(user_query)
        focus_keywords = extract_keywords(user_query)
        context_summary = get_context_summary(context, focus_keywords)
        print(focus_keywords)
        print(context_summary)
        prompt = f"Based on the information: {context_summary} \nHow would you answer the user's query about: {user_query}?"
        print(f"Prompt: {prompt}")  # Check what the prompt looks like
        
        full_response = ""
       
       
        
        result =  replicate.run(
            "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173",
            input={
        "prompt": prompt,
        "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        
    },
        )
        print(result)
        full_response = ''.join(result)
        print(full_response)
        return(full_response)

def query_gpt_3_5_turbo(user_query):
    try:
        
        context = get_context_from_vector_db(user_query)
        prompt = f"Based on the information: {context} \nHow would you answer the user's query about: {user_query}?"
        openai.api_key = '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'
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        print(response.choices[0].message.content)
        result = response.choices[0].message.content
        return result
    except Exception as e:
        return {'error': str(e)}
    

def query_gpt4(user_query):
    try:

        context = get_context_from_vector_db(user_query)
        prompt = f"Based on the information: {context} \nHow would you answer the user's query about: {user_query}?"
        openai.api_key = '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'  # Ensure your API key is correctly configured
        response = openai.chat.completions.create(
            model="gpt-4",  # Confirm the model ID is correct and available to you
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
        
        )
        print(response.choices[0].message.content)
        result = response.choices[0].message.content
        return result
    except Exception as e:
        return {'error': str(e)}



