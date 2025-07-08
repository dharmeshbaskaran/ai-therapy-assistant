import requests
from flask import request, jsonify

@api.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    try:
        response = requests.post(
            'http://ollama:11434/api/generate',
            json={
                "model": "llama3.3:70b",
                "prompt": user_input,
                "stream": True
            },
            stream=True  # <-- Important!
        )

        full_response = ''
        for line in response.iter_lines():
            if line:
                data = line.decode('utf-8')
                # Some lines may look like: {"response":"Hello"}
                try:
                    json_data = json.loads(data)
                    full_response += json_data.get('response', '')
                except json.JSONDecodeError:
                    continue

        return jsonify({'response': full_response})

    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500
