import os
# import asyncio

import settings
import utils
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    session
)
from middleware import model_predict
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
# import requests
from os.path import exists

router = Blueprint('app_router', __name__, template_folder='templates')


@router.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # No file received, show basic UI
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # File received but no filename is provided, show basic UI
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url, filename=filename, context=context)

        # File received and it's an image, we must show it and get predictions
        if file and utils.allowed_file(file.filename):

            split_name = file.filename
            split_name = split_name.split('.')
            print(str(split_name[1]))
            # get name hashed and adding image extension to be saved
            Filenamehashed = utils.get_file_hash(file)
            saveImgPath = os.path.join(settings.UPLOAD_FOLDER, Filenamehashed)
            # Save customer image in Server
            file.save(saveImgPath)

            # call middleware
            predict, score = model_predict(Filenamehashed)
            context = {
                'prediction': predict,
                'score': score,
                'filename': Filenamehashed
            }
            filename = '/static/uploads/' + Filenamehashed
            return render_template("index.html", filename=filename, context=context)

        # File received and but it isn't an image
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)


@ router.route('/<filename>',  methods=['POST', 'GET'])
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


@ router.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        rpse = {'success': False, 'prediction': None, 'score': None}
        return jsonify(rpse), 405

    rpse = {'success': None, 'prediction': None, 'score': None}
    if 'file' not in request.files:
        rpse = {'success': False, 'prediction': None, 'score': None}
        return jsonify(rpse), 400

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        rpse = {'success': False, 'prediction': None, 'score': None}
        return jsonify(rpse), 400

    # File received and it's an image, we must show it and get predictions
    # if file and utils.allowed_file(file.filename):
    if utils.allowed_file(file.filename):
        # get name hashed and adding image extension to be saved
        Filenamehashed = utils.get_file_hash(file)
        saveImgPath = os.path.join(settings.UPLOAD_FOLDER, Filenamehashed)
        if not os.path.exists(saveImgPath):
            # Save customer image in Server
            file.save(saveImgPath)
        # call middleware
        predict, score = model_predict(Filenamehashed)
        rpse = {'success': True, 'prediction': predict, 'score': score}
        return jsonify(rpse)
    else:
        rpse = {'success': False, 'prediction': None, 'score': None}
        return jsonify(rpse), 405


@ router.route('/feedback', methods=['GET', 'POST'])
def feedback():
    report = request.form.get('report')
    # Open the file in append & read mode ('a+')
    feedback = open(settings.FEEDBACK_FILEPATH, "a+")
    # Move read cursor to the start of file.
    feedback.seek(0)
    # If file is not empty then append '\n'
    data = feedback.read(100)
    if len(data) > 0:
        feedback.write("\n")
    # Append text at the end of file
    feedback.write(str(report))
    feedback.close()
    return render_template('index.html', filename='', context='')
