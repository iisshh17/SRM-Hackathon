from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import ssl
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure Gemini AI
GOOGLE_API_KEY = 'AIzaSyAtjJK865GQRbuAZAYiltGEwZC5-TZor_0'
genai.configure(api_key=GOOGLE_API_KEY)

# Add these configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_credentials(username, password):
    with open('credentials.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == username and row[1] == password:
                return True
    return False

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        # Format the response text
        formatted_response = response.text.replace('```', '<pre><code>').replace('```', '</code></pre>')
        return formatted_response
    except Exception as e:
        return f"Error: {str(e)}"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('content.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('signin.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/content')
def content():
    return render_template('content.html')

@app.route('/chat_2', methods=['GET', 'POST'])
def get_request_json():
    # Define topic_icons at the start of the function so it's available for both GET and POST
    topic_icons = {
        'physics': 'atom',
        'mathematics': 'calculator',
        'biology': 'dna',
        'chemistry': 'flask'
    }

    if request.method == 'POST':
        if len(request.form['question']) < 1:
            return render_template(
                'chat_2.html', 
                question="NULL", 
                res="Question can't be empty!", 
                temperature="NULL",
                topic_icons=topic_icons)  # Add topic_icons here
        
        question = request.form['question']
        temperature = float(request.form['temperature'])
        
        try:
            res = ask_gemini(question)
        except Exception as e:
            res = f"Error: {str(e)}"
            
        print("Q: \n", question)
        print("A: \n", res)
        
        return render_template('chat_2.html', 
                             question=question, 
                             res=str(res), 
                             temperature=temperature,
                             topic_icons=topic_icons)
    
    # For GET requests, pass topic_icons
    return render_template('chat_2.html', question=0, topic_icons=topic_icons)

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            
        try:
            prompt = r.recognize_google(audio)
            print("You said:", prompt)
            
            if prompt.lower() == "bye":
                response = "Goodbye! Have a great day!"
            else:
                response = ask_gemini(prompt)
                
                # Text to speech
                engine = pyttsx3.init()
                engine.say(response)
                engine.runAndWait()
            
            return jsonify({
                'user_message': prompt,
                'bot_response': response
            })
            
        except sr.UnknownValueError:
            return jsonify({
                'error': "Could not understand audio"
            })
        except sr.RequestError as e:
            return jsonify({
                'error': f"Could not request results; {str(e)}"
            })
    
    return render_template('voice.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    text = request.json.get('text')
    try:
        response = ask_gemini(text)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/stop_voice', methods=['POST'])
def stop_voice():
    # Add logic to stop recording
    return jsonify({'success': True})

@app.route('/games/sudoku')
def sudoku_game():
    return render_template('games/sudoku.html')

@app.route('/games/memory')
def memory_game():
    return render_template('games/memory.html')

@app.route('/games/word-scramble')
def word_scramble():
    return render_template('games/word_scramble.html')

@app.route('/games/math-quiz')
def math_quiz():
    return render_template('games/math_quiz.html')

@app.route('/games/pattern-match')
def pattern_match():
    return render_template('games/pattern_match.html')

@app.route('/games/speed-typing')
def speed_typing():
    return render_template('games/speed_typing.html')

@app.route('/games/color-memory')
def color_memory():
    return render_template('games/color_memory.html')

@app.route('/games/number-sequence')
def number_sequence():
    return render_template('games/number_sequence.html')

@app.route('/games/word-association')
def word_association():
    return render_template('games/word_association.html')

@app.route('/art')
def art_index():
    return render_template('art/index.html')

@app.route('/art/shapes')
def art_shapes():
    return render_template('art/shapes.html')

@app.route('/art/heroes')
def art_heroes():
    return render_template('art/heroes.html')

@app.route('/art/flowers')
def art_flowers():
    return render_template('art/flowers.html')

@app.route('/art/ironman')
def art_ironman():
    return render_template('art/ironman.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)