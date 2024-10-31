# Notes-App
FlaskNotesApp is a feature-rich web-based note-taking application built with Flask and MongoDB.
It allows users to create, read, update, and delete notes effortlessly while also offering unique functionalities such as voice notes and image attachments. 
The application is fully responsive, making it accessible on any device without an internet connection.

Key Features:
  1.MongoDB Integration    : Utilizes MongoDB for data storage, enabling flexible note management and storing unstructured data.
  2.CRUD Operations        : Create, read, update, and delete notes easily.
  3.File Uploads           : Supports uploading images and voice recordings for each note.
  4.Dynamic Content        : Fetches inspirational quotes from an external API to enhance user experience.
  5.Download Notes         : Allows users to download notes as text files for offline access.
  6.User-Friendly Interface: Built with Jinja2 for powerful templating and a clean, intuitive UI.
  7.Secure File Handling   : Uses werkzeug for secure file uploads and handling.
  8.Quote Generation       : using a random quote generator api for generting quotes in homepage. 

**SCREENSHOTS**

SEE NOTES PAGE
![image](https://github.com/user-attachments/assets/918c496a-8fb8-4986-a210-769601262977)

ADD NOTES PAGE
![image](https://github.com/user-attachments/assets/76db709c-d276-4a2c-bbb3-7eeaae34b06f)

UPDATE NOTES Page
![image](https://github.com/user-attachments/assets/e987832c-66ca-4538-b5cf-eb7211c6fa51)

Files in this project:
1. app.py          - root python file for mongo db and flask integration and rendering all the html files in template folder
2. add_note_routes - handle add notes efficiently
3. see note        - displaying the saved notes
4. update note     - handle uppdate options effectively
5. base note       - for background and bootstrap based styling

Folders in the project:
1. Templates : all the html files for add notes,see note,update note are saved in this template folder for app.py
2. uploads : all the pictures uploaded in notes are saved in this folder
