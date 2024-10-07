import os
from flask import Flask, render_template, jsonify
from helpers import *

app = Flask(__name__)

# Paths to media directories
IMAGE_DIR = 'static/slides'
AUDIO_DIR = 'static/audio'

# Ensure that the audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Get a sorted list of images from the slides directory
images = sorted(
    [file for file in os.listdir(IMAGE_DIR) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
)

# Home page
@app.route('/')
def index():
    # pptx_path = '/static/powerpoint/Sprint_review_ROB_18-06-2024.pptx'
    # output_dir = '/static/slides'
    # pptx_to_images(pptx_path, output_dir)
    return render_template('index.html')

# Function to fetch the slide count
@app.route('/get_slide_count')
def get_slide_count():
    return jsonify({ 'count': f'{len(images)}'})

# Function to fetch a slide
@app.route('/get_slide/<int:index>')
def get_slide(index):
    if index >= 0 and index < len(images):
        image_name = images[index]
        image_url = f'{IMAGE_DIR}/{image_name}'

        root, _ = os.path.splitext(image_name)
        audio_name = root + '.mp3'
        audio_url = f'{AUDIO_DIR}/{audio_name}'

        if not os.path.exists(audio_url):
            audio_url = ''

        return jsonify({
            'image_url': image_url,
            'audio_url': audio_url    
        })

    return jsonify({
        'image_url': '',
        'audio_url': ''
    })
    
@app.route('/get_audio/<int:index>')
def get_audio(index):
    if index >= 0 and index < len(images):
        image_name = images[index]
        root, _ = os.path.splitext(image_name)
        audio_name = root + '.mp3'
        audio_url = f'{AUDIO_DIR}/{audio_name}'

        # Return the URL if the audio file exists
        if os.path.exists(audio_url):
            return jsonify({'audio_url': audio_url})

        # Use GPT-4o to generate a narration for the image
        image_url = f'{IMAGE_DIR}/{image_name}'
        text = generate_narration(image_url)

        # Use TTS to generate audio
        generate_audio(text, audio_url)
			
        # Return the audio URL
        return jsonify({'audio_url': audio_url})
	
    return jsonify({'audio_url': ''})