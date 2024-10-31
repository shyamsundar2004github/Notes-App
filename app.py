from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
import requests
import os
import nltk 
from nltk.corpus import wordnet

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['notes_database']
collection = db['notes_collection']

QUOTE_API_URL = 'https://api.quotable.io/random'

def get_quote_from_api():
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data['content'] + ' - ' + data['author']
        else:
            return 'Failed to fetch quote from API'
    except Exception as e:
        return str(e)

# Create upload folder if not exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set upload folder for Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for serving static files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def login():
    quote = get_quote_from_api()
    return render_template('login.html',quote=quote)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
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
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        if voice:
            filename = secure_filename(voice.filename)
            voice_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
    else:
        return render_template('add_note.html')

@app.route('/see_notes')
def see_notes():
    notes = collection.find()
    return render_template('see_notes.html', notes=notes)

@app.route('/delete_note/<note_id>')
def delete_note(note_id):
    collection.delete_one({'_id': ObjectId(note_id)})
    return redirect(url_for('see_notes'))

@app.route('/update_note/<title>', methods=['GET', 'POST'])
def update_note(title):
    print("Received title:", title)  # Add this line for debugging
    # Fetch the note from the database based on the title
    note = collection.find_one({'title': title})
    print("Found note:", note)  # Add this line for debugging
    if not note:
        return "Note not found", 404

    if request.method == 'POST':
        # Update the note with the new data from the form
        updated_title = request.form['title']
        updated_content = request.form['content']
        updated_image = request.files.get('image')
        updated_voice = request.files.get('voice')

        # Check if updated title and content are provided
        if not updated_title or not updated_content:
            return "Updated title and content are mandatory", 400

        # Update image if provided
        if updated_image:
            filename = secure_filename(updated_image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            updated_image.save(image_path)
            collection.update_one({'title': title}, {'$set': {'image_path': image_path}})

        # Update voice if provided
        if updated_voice:
            filename = secure_filename(updated_voice.filename)
            voice_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            updated_voice.save(voice_path)
            collection.update_one({'title': title}, {'$set': {'voice_path': voice_path}})

        # Update the title and content
        collection.update_one({'title': title}, {'$set': {'title': updated_title, 'content': updated_content}})

        # Redirect back to the see_notes page
        return redirect(url_for('see_notes'))

    return render_template('update_note.html', note=note)

@app.route('/word_lookup', methods=['POST'])
def word_lookup():
    word = request.form['word']
    synsets = wordnet.synsets(word)
    if synsets:
        word_info = []
        for synset in synsets:
            word_info.append({
                'definition': synset.definition(),
                'synonyms': synset.lemma_names(),
                'antonyms': [lemma.antonyms()[0].name() for lemma in synset.lemmas() if lemma.antonyms()]
            })
        return render_template('word_lookup_result.html', word_info=word_info)
    else:
        return render_template('word_lookup_result.html', error='Word not found in WordNet')

@app.route('/word_lookup_form')
def word_lookup_form():
    return render_template('word_lookup_form.html')

@app.route('/share_as_txt/<title>')
def share_as_txt(title):
    note = collection.find_one({'title': title})
    if not note:
        return "Note not found", 404

    # Create a response with the note content as a text file
    response = make_response(note['content'])
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename="{title}.txt"'

    return response

if __name__ == '__main__':
    app.run(debug=True)