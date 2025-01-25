import google.generativeai as genai
import numpy as np
from keras.models import load_model
from keras.utils import pad_sequences
import re
import pickle
import pandas as pd
import os
import csv
from SimilarText import load_qa_data, TextSimilarity

# Configure Gemini AI
GOOGLE_API_KEY = 'AIzaSyAtjJK865GQRbuAZAYiltGEwZC5-TZor_0'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize ML components with error handling
try:
    # Load MBTI classifier
    with open('model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)

    # Load learning style classifier
    with open('tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    with open('labelEncoder.pickle', 'rb') as f:
        le = pickle.load(f)
    model = load_model('LearningStyleClassifier.h5')
    
    ML_ENABLED = True
except Exception as e:
    print(f"Warning: ML models not loaded ({str(e)}). Using default classification.")
    ML_ENABLED = False

def classify_personality(response):
    """Classify MBTI personality type"""
    try:
        if ML_ENABLED:
            X_test = loaded_vectorizer.transform([response])
            prediction = loaded_model.predict(X_test)[0]
            return prediction
        return "INFJ"  # Default type if ML is not available
    except Exception as e:
        print(f"Personality classification error: {str(e)}")
        return "INFJ"

def clean(text):
    """Clean text for processing"""
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text.lower()

def classify_learning_type(sentence):
    """Classify learning style"""
    try:
        if ML_ENABLED:
            sentence = clean(sentence)
            sentence = tokenizer.texts_to_sequences([sentence])
            sentence = pad_sequences(sentence, maxlen=48, truncating='pre')
            result = le.inverse_transform(np.argmax(model.predict(sentence), axis=-1))[0]
            return result
        return "visual"  # Default learning style if ML is not available
    except Exception as e:
        print(f"Learning style classification error: {str(e)}")
        return "visual"

# Initialize QA database
try:
    qa_dict = load_qa_data('question_answer.csv')
    text_similarity = TextSimilarity()
    vectorstore = text_similarity.update_embeddings(qa_dict)
except Exception as e:
    print(f"Warning: QA database initialization error ({str(e)})")
    qa_dict = {}
    vectorstore = None

def generate_gemini_response(prompt, mbti, learning, temperature):
    """Generate response using Gemini AI"""
    try:
        generation_config = {
            "temperature": temperature,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config
        )
        
        system_prompt = f"""As an advanced educational AI tutor, create a comprehensive learning experience for a {mbti} 
        personality type with a {learning} learning style. Structure your response exactly as follows:

        🎯 **Learning Objectives:**
        • List 2-3 clear learning goals
        • What the student will understand after this lesson

        📚 **Core Concept:**
        Provide a clear, engaging introduction that captures interest and sets the context.
        Break down the main concept into easily digestible parts.

        🔑 **Key Principles:**
        1. [First principle with definition]
        2. [Second principle with explanation]
        3. [Third principle with importance]

        💡 **Detailed Explanation:**
        • Use {learning}-focused explanations
        • Include relevant analogies and examples
        • Break complex ideas into simple steps

        🌟 **Real-World Applications:**
        1. [Practical example with explanation]
        2. [Industry application]
        3. [Daily life connection]

        ✍️ **Interactive Practice:**
        [Provide an engaging exercise that matches the student's learning style]
        
        💭 **Critical Thinking:**
        • [Thought-provoking question]
        • [Analysis prompt]
        • [Problem-solving scenario]

        📌 **Key Takeaways:**
        • [Main point 1]
        • [Main point 2]
        • [Main point 3]

        🔄 **Next Steps:**
        • [Related topics to explore]
        • [Recommended resources]
        • [Practice suggestions]

        Use a friendly, encouraging tone and adapt examples to match both MBTI preferences and learning style.
        """
        
        full_prompt = f"{system_prompt}\n\nStudent's question: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def format_response(response_text, score_message, mbti, learning_style):
    """Format the response with enhanced HTML structure"""
    return f"""
    <div class="response-container">
        <div class="response-header">
            <div class="response-title">
                <h2>Personalized Learning Guide</h2>
                <div class="response-meta">
                    <span class="meta-item"><i class="fas fa-brain"></i> {mbti}</span>
                    <span class="meta-item"><i class="fas fa-book"></i> {learning_style} Learner</span>
                    <span class="meta-item"><i class="fas fa-search"></i> Match: {score_message}</span>
                </div>
            </div>
        </div>

        <div class="content-section">
            <div class="learning-content">
                {response_text}
            </div>
        </div>

        <div class="practice-section">
            <div class="section-title">
                <i class="fas fa-pencil-alt"></i>
                <span>Practice & Application</span>
            </div>
            <div class="practice-content">
                <!-- Dynamic practice content -->
            </div>
        </div>

        <div class="resource-section">
            <div class="section-title">
                <i class="fas fa-book-open"></i>
                <span>Additional Resources</span>
            </div>
            <div class="resource-grid">
                <!-- Dynamic resource content -->
            </div>
        </div>
    </div>
    """

def send_gptnew(prompt, tem, vecstore=vectorstore):
    """Main function to handle responses"""
    try:
        # Check database for existing response
        similarity_score = 0
        if vectorstore is not None:
            try:
                similarity_score = text_similarity.top_similar_prompts(prompt, vecstore)[0][1]
            except Exception:
                pass
        
        score_message = f"Similarity Score: {similarity_score:.2f}"
        
        # Return cached response if available
        if prompt in qa_dict and qa_dict[prompt]['temperature'] == tem:
            return f"{score_message}\n[Cached Response]\n{qa_dict[prompt]['returnstring']}"
            
        # Return similar response if found
        if similarity_score > 0.2 and vectorstore is not None:
            similar_response = text_similarity.top_similar_docs(prompt, vecstore, qa_dict)
            summary = text_similarity.extractive_summary(prompt, similar_response)
            return f"{score_message}\n[Similar Response Found]\n{summary}"
        
        # Generate new response
        mbti = classify_personality(prompt)
        learning_style = classify_learning_type(prompt)
        
        response = generate_gemini_response(prompt, mbti, learning_style, tem)
        
        formatted_response = format_response(response, score_message, mbti, learning_style)
        
        # Cache the response
        if vectorstore is not None:
            try:
                qa_dict[prompt] = {
                    'returnstring': formatted_response,
                    'mbti': mbti,
                    'learning': learning_style,
                    'temperature': tem
                }
                text_similarity.update_embeddings(qa_dict)
                
                # Update CSV
                row = {
                    'prompt': prompt,
                    'returnstring': formatted_response,
                    'mbti': mbti,
                    'learning': learning_style,
                    'temperature': tem
                }
                with open('question_answer.csv', mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=row.keys())
                    writer.writerow(row)
            except Exception as e:
                print(f"Error updating QA database: {str(e)}")
        
        return f"{score_message}\n[Generated Response]\n{formatted_response}"
    except Exception as e:
        return f"Error processing request: {str(e)}"
