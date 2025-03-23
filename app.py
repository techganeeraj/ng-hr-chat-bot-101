from flask import Flask, render_template, request, jsonify
from dialogflow_client import DialogflowClient
from google import genai
from google.genai import types
import uuid

app = Flask(__name__)
dialogflow_client = DialogflowClient()
session_id = str(uuid.uuid4())

# Initialize Gemini client
client = genai.Client(
    vertexai=True,
    project="ng-project-102",
    location="us-central1",
)
model = "gemini-2.0-flash-exp"

current_question_index = 0
user_responses = []
psychometric_questions = []

def generate_psychometric_questions():
    content = types.Content(
        role="user",
        parts=[
            types.Part(text="""Generate 5 insightful psychometric questions that would help assess a person's personality, 
            work style, and emotional intelligence. The questions should be professional, open-ended, and suitable for a 
            workplace context. Return only the questions, one per line, without numbering or additional text.""")
        ]
    )
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"]
    )

    response = client.models.generate_content(
        model=model,
        contents=[content],
        config=generate_content_config,
    )
    
    questions = [q.strip() for q in response.text.split('\n') if q.strip()]
    return questions[:5]

def generate_analysis(questions_and_responses):
    content = types.Content(
        role="user",
        parts=[
            types.Part(text="""Based on these responses to a psychometric test, provide a detailed personality analysis.
            Include insights about:
            - Work style and preferences
            - Decision-making approach
            - Communication style
            - Strengths and potential growth areas

            Responses to analyze:
            """ + questions_and_responses)
        ]
    )
    
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"]
    )

    response = client.models.generate_content(
        model=model,
        contents=[content],
        config=generate_content_config,
    )
    
    return response.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = dialogflow_client.detect_intent(user_message, session_id)
    bot_response = dialogflow_client.get_response_text(response)
    return jsonify({'response': bot_response})

@app.route('/start_psych_test', methods=['POST'])
def start_psych_test():
    global current_question_index, user_responses, psychometric_questions
    current_question_index = 0
    user_responses = []
    
    try:
        psychometric_questions = generate_psychometric_questions()
        return jsonify({
            'response': "Let's begin the psychometric assessment. I'll ask you some questions to understand your personality and work style better.\n\n" + 
                       f"Question 1: {psychometric_questions[0]}"
        })
    except Exception as e:
        return jsonify({
            'response': f"Sorry, there was an error starting the test: {str(e)}"
        })

@app.route('/psych_test_response', methods=['POST'])
def psych_test_response():
    global current_question_index, user_responses
    
    user_message = request.json.get('message')
    user_responses.append(user_message)
    
    current_question_index += 1
    
    if current_question_index < len(psychometric_questions):
        return jsonify({
            'response': f"Question {current_question_index + 1}: {psychometric_questions[current_question_index]}"
        })
    else:
        try:
            # Prepare questions and responses for analysis
            qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(psychometric_questions, user_responses)])
            analysis = generate_analysis(qa_pairs)
            
            current_question_index = 0
            user_responses = []
            
            return jsonify({
                'response': f"Thank you for completing the test. Here's your personality analysis:\n\n{analysis}"
            })
        except Exception as e:
            return jsonify({
                'response': f"Sorry, there was an error generating your analysis: {str(e)}"
            })

if __name__ == '__main__':
    app.run(debug=True) 