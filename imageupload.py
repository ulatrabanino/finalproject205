#Reference: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


#Restrictions for file uploads
app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

#render html file and also display uploaded images 
@app.route('/')
def imageuploadtest():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('imageuploadtest.html', files=files)

#checks if it is a valid file type. If it is, save to uploads. If not, display error
@app.route('/', methods=['POST'])
def image_upload():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('imageuploadtest'))

#reroutes uploads onto the html page for display
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)