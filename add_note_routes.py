# add_note_routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient

add_note_routes = Blueprint('add_note_routes', __name__)

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['notes_database']
collection = db['notes_collection']

@add_note_routes.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    image = request.files.get('image')
    voice = request.files.get('voice')

    # Check if title and content are provided
    if not title or not content:
        return "Title and content are mandatory", 400

    # Save image and voice files to server
    image_path = None
    voice_path = None
    if image:
        image_path = f"uploads/{image.filename}"
        image.save(image_path)
    if voice:
        voice_path = f"uploads/{voice.filename}"
        voice.save(voice_path)

    # Insert note into MongoDB
    note = {
        'title': title,
        'content': content,
        'image_path': image_path,
        'voice_path': voice_path
    }
    collection.insert_one(note)

    return redirect(url_for('see_notes'))

