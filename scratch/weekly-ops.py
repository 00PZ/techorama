from flask import Flask, jsonify
import requests
from bs4 import BeautifulSouxp
import openai
import os

app = Flask(__name__)


def get_latest_version(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = soup.get_text()

    # Use environment variable for OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = f"Extract the latest software version from the following text:\n\n{text_content}\n\nVersion:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10
    )

    latest_version = response.choices[0].text.strip()
    return latest_version if latest_version else None


def check_for_update(current_version, latest_version):
    return current_version != latest_version


@app.route('/check-update/<current_version>', methods=['GET'])
def check_update(current_version):
    url = 'https://example.com/software-release-page'  # Replace with the actual URL
    latest_version = get_latest_version(url)
    if latest_version:
        needs_update = check_for_update(current_version, latest_version)
        return jsonify({
            'current_version': current_version,
            'latest_version': latest_version,
            'needs_update': needs_update
        })
    else:
        return jsonify({'error': 'Could not retrieve the latest version'}), 500


if __name__ == '__main__':
    app.run(debug=True)
