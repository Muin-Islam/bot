from flask import Flask, render_template, request, jsonify
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (only needed once)
nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

# Google Custom Search API credentials
GOOGLE_API_KEY = "AIzaSyAxJj5wcmsJayQgH06JMA3VbLsYF2y6a8I"  # Replace with your API key
GOOGLE_CSE_ID = "3359a636478a342e5"  # Replace with your CSE ID

def search_google(query):
    """
    Searches Google using the Custom Search JSON API and returns the first result snippet.
    """
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract the first result snippet
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['snippet']
        else:
            return "No results found."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google search results: {e}")
        return "Sorry, I couldn't fetch the information from Google."

def process_query(query):
    """
    Processes the user's query by removing stop words and tokenizing.
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    filtered_query = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_query)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    print(f"User input: {user_input}")  # Debug: Print user input
    try:
        processed_query = process_query(user_input)
        print(f"Processed query: {processed_query}")  # Debug: Print processed query
        response = search_google(processed_query)
        print(f"Bot response: {response}")  # Debug: Print bot response
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")  # Debug: Print any errors
        return jsonify({'response': "Sorry, something went wrong!"})

if __name__ == '__main__':
    app.run(debug=True)