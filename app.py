from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import fetch_data
import json
app = Flask(__name__)
CORS(app)

def stream_responses(user_query):
   
    try:
        response_gpt4 = fetch_data.query_gpt4(user_query)
        yield f"data: {json.dumps({'gpt4': response_gpt4})}\n\n"
        
        response_gpt35 = fetch_data.query_gpt_3_5_turbo(user_query)
        yield f"data: {json.dumps({'gpt-3.5-turbo': response_gpt35})}\n\n"
        
        response_llama = fetch_data.query_llama_2_70b_chat(user_query)
        yield f"data: {json.dumps({'Llama-2-70b-chat': response_llama})}\n\n"

        response_falcon = fetch_data.query_falcon(user_query)
        yield f"data: {json.dumps({'Falcon-40b-instruct': response_falcon})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.route('/api/query', methods=['GET'])
def handle_query():
    user_query = request.args.get('query', type=str)
    try:
        return Response(stream_with_context(stream_responses(user_query)), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

