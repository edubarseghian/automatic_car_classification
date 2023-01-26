# Source:
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os


# from app import textfile_path, file_content, textfile

import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)

#app.config['Image_Upload'] = 'static/uploads/'


@app.route("/", methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'GET':
            return render_template('testtavo.html')

        if request.method == 'POST' and request.files['file'].filename:
            filename = photos.url(request.files['file'])
            fil = request.files['file']
            return 'Text to print'
        # if request.method == 'POST':
        #     print('holaaa')
        #     image = request.files['file']
        #     print('hola2')
        #     return render_template('testtavo.html')
    except Exception as e:
        return print(e)
#     if request.method == 'POST':
#         print('possst')
#         # image = request.file['file']

#         # if image.filename == '':
#         #     print('File name is invalid')
#         #     return redirect(request.url)

#         # filename = secure_filename(image.filename)
#         return redirect(request.url)


@app.route('/about')
def about():
    return render_template('about.html')

#bootstrap = Bootstrap(app)


if __name__ == '__main__':
    app.run()
