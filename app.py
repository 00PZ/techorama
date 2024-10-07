from flask import Flask, jsonify
from openai import AsyncOpenAI

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello, World!")

@app.route('/test')
def test():
    client = AsyncOpenAI(api_key='')
    messages = []
    

if __name__ == '__main__':
    app.run(debug=True)

