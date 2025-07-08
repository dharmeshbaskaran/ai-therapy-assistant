from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS
from textblob import TextBlob

app = Flask(__name__)
CORS(app, origins=["http://192.168.1.6:3000"])


# Expanded keywords to allow medicine and symptom queries
THERAPY_KEYWORDS = [
    'anxiety', 'stress', 'depression', 'mental', 'therapy', 'therapist',
    'panic', 'sad', 'grief', 'anger', 'mood', 'psychologist',
    'counseling', 'emotion', 'feeling', 'fear', 'nervous', 'trauma',
    'medicine', 'medication', 'migraine', 'pain', 'headache', 'tablet', 'pill', 'relief', 'crocin', 'paracetamol', 'ibuprofen', 'aspirin', 'acetaminophen', 'treatment', 'doctor', 'prescription', 'diagnosis', 'symptom', 'health', 'wellness',
    # Greetings and thankfulness (100+)
    'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night', 'good day', 'howdy', 'yo', 'hiya', 'sup', 'wassup', 'what’s up', 'how are you', 'how are you doing', 'how do you do', 'how have you been', 'how’s it going', 'how’s everything', 'how’s life', 'how’s your day', 'how’s your morning', 'how’s your afternoon', 'how’s your evening', 'nice to meet you', 'pleased to meet you', 'good to see you', 'good to hear from you', 'glad to see you', 'glad to hear from you', 'long time no see', 'it’s been a while', 'welcome', 'welcome back', 'great to see you', 'great to hear from you', 'happy to see you', 'happy to hear from you', 'hope you are well', 'hope you are doing well', 'hope you are fine', 'hope you are okay', 'hope you are good', 'hope all is well', 'hope all is good', 'hope all is okay', 'hope all is fine', 'hope you’re having a good day', 'hope you’re having a great day', 'hope you’re having a nice day', 'hope you’re having a wonderful day', 'hope you’re having a good morning', 'hope you’re having a good afternoon', 'hope you’re having a good evening', 'hope you’re having a good night', 'hope you’re enjoying your day', 'hope you’re enjoying your morning', 'hope you’re enjoying your afternoon', 'hope you’re enjoying your evening', 'hope you’re enjoying your night', 'thank you', 'thanks', 'thanks a lot', 'thanks so much', 'thanks very much', 'thank you very much', 'thank you so much', 'thank you for your help', 'thank you for helping', 'thank you for your support', 'thank you for supporting', 'thank you for being there', 'thank you for listening', 'thank you for understanding', 'thank you for caring', 'thank you for your kindness', 'thank you for your patience', 'thank you for your time', 'thank you for your advice', 'thank you for your guidance', 'thank you for your encouragement', 'thank you for your compassion', 'thank you for your empathy', 'thank you for your concern', 'thank you for your thoughtfulness', 'thank you for your generosity', 'thank you for your consideration', 'thank you for your attention', 'thank you for your response', 'thank you for your reply', 'thank you for your message', 'thank you for your words', 'thank you for your feedback', 'thank you for your suggestion', 'thank you for your recommendation', 'thank you for your input', 'thank you for your insight', 'thank you for your perspective', 'thank you for your honesty', 'thank you for your openness', 'thank you for your sincerity', 'thank you for your trust', 'thank you for your friendship', 'thank you for your company', 'thank you for your presence', 'thank you for your smile', 'thank you for your laughter', 'thank you for your positivity', 'thank you for your optimism', 'thank you for your encouragement', 'thank you for your inspiration', 'thank you for your motivation', 'thank you for your support and encouragement', 'thank you for your help and support', 'thank you for your care and concern', 'thank you for your love and support', 'thank you for your understanding and patience', 'thank you for your kindness and generosity', 'thank you for your advice and guidance', 'thank you for your time and attention', 'thank you for your feedback and suggestion', 'thank you for your honesty and openness', 'thank you for your trust and friendship', 'thank you for your company and presence', 'thank you for your smile and laughter', 'thank you for your positivity and optimism', 'thank you for your encouragement and inspiration', 'thank you for your motivation and support', 'thank you for everything', 'thank you for all you do', 'thank you for always being there', 'thank you for always listening', 'thank you for always understanding', 'thank you for always caring', 'thank you for always supporting', 'thank you for always helping', 'thank you for always encouraging', 'thank you for always inspiring', 'thank you for always motivating', 'thank you for always being kind', 'thank you for always being patient', 'thank you for always being generous', 'thank you for always being thoughtful', 'thank you for always being considerate', 'thank you for always being honest', 'thank you for always being open', 'thank you for always being sincere', 'thank you for always being trustworthy', 'thank you for always being a good friend', 'thank you for always being a good listener', 'thank you for always being a good company', 'thank you for always being a good presence', 'thank you for always being a good support', 'thank you for always being a good encouragement', 'thank you for always being a good inspiration', 'thank you for always being a good motivation', 'thank you for always being a good help', 'thank you for always being a good care', 'thank you for always being a good concern', 'thank you for always being a good advice', 'thank you for always being a good guidance', 'thank you for always being a good suggestion', 'thank you for always being a good recommendation', 'thank you for always being a good input', 'thank you for always being a good insight', 'thank you for always being a good perspective', 'thank you for always being a good honesty', 'thank you for always being a good openness', 'thank you for always being a good sincerity', 'thank you for always being a good trust', 'thank you for always being a good friendship', 'thank you for always being a good company', 'thank you for always being a good presence', 'thank you for always being a good smile', 'thank you for always being a good laughter', 'thank you for always being a good positivity', 'thank you for always being a good optimism', 'thank you for always being a good encouragement', 'thank you for always being a good inspiration', 'thank you for always being a good motivation', 'thank you for always being a good support and encouragement', 'thank you for always being a good help and support', 'thank you for always being a good care and concern', 'thank you for always being a good love and support', 'thank you for always being a good understanding and patience', 'thank you for always being a good kindness and generosity', 'thank you for always being a good advice and guidance', 'thank you for always being a good time and attention', 'thank you for always being a good feedback and suggestion', 'thank you for always being a good honesty and openness', 'thank you for always being a good trust and friendship', 'thank you for always being a good company and presence', 'thank you for always being a good smile and laughter', 'thank you for always being a good positivity and optimism', 'thank you for always being a good encouragement and inspiration', 'thank you for always being a good motivation and support', 'thank you for always being everything', 'thank you for always being all you do',
    # Feedback and conversational context
    'satisfied', 'unsatisfied', 'dissatisfied', 'response', 'answer', 'helpful', 'not helpful', 'feedback', 'support', 'listen', 'listening', 'understand', 'understood', 'clarify', 'clarification', 'explain', 'explanation', 'continue', 'convo', 'conversation', 'talk', 'discuss', 'discussion', 'session', 'chat', 'follow up', 'follow-up', 'previous', 'before', 'earlier', 'again', 'repeat', 'more', 'less', 'better', 'worse', 'improve', 'improvement', 'problem', 'issue', 'concern', 'question', 'doubt', 'query'
]

BLOCKED_KEYWORDS = [
    'payload', 'xss', 'script', '<script>', 'sql', 'inject', 'bypass', 'hack',
    'attack', 'malicious', 'exploit', 'csrf', 'xxe', 'ssrf', 'rce'
]


@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    history = request.json.get('history', [])  # List of {role, text}

    # Spell correction
    corrected_message = str(TextBlob(user_message).correct())

    if not corrected_message.strip():
        return jsonify({'reply': 'Please say something.'}), 400

    if any(bad in corrected_message for bad in BLOCKED_KEYWORDS):
        return jsonify({'reply': 'This request cannot be processed due to security concerns.'})

    if not any(keyword in corrected_message for keyword in THERAPY_KEYWORDS):
        return jsonify({'reply': 'Sorry, I can only respond to therapy or mental health-related questions.'})

    try:
        # Therapist-like system prompt for empathetic, supportive, conversational responses
        system_prompt = (
            "You are a compassionate and supportive therapist. "
            "Respond to the user as a real therapist would: listen carefully, validate their feelings, and offer gentle guidance or coping strategies. "
            "Use empathetic, conversational language. "
            "Respond warmly to greetings and thankfulness. "
            "Do not mention that you are an AI or language model. "
            "If asked about medicines, provide general information in a caring way, but do not prescribe. "
            "If the question is not about health, therapy, medicine, greetings, or thankfulness, politely decline."
        )

        # Build conversation history for prompt
        conversation = system_prompt + "\n"
        for msg in history:
            role = 'User' if msg.get('role') == 'user' else 'Assistant'
            conversation += f"{role}: {msg.get('text','').strip()}\n"
        conversation += f"User: {corrected_message}\nAssistant:"

        res = requests.post(
            'http://ollama:11434/api/generate',
            json={
                "model": "mistral",
                "prompt": conversation,
                "stream": True
            },
        )

        full_response = ''
        for line in res.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    full_response += data.get('response', '')
                except json.JSONDecodeError:
                    continue

        return jsonify({'reply': full_response.strip()})

    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)