from flask import Flask, request, flash, redirect
from werkzeug.utils import secure_filename
import os
import zipfile
import glob
import socket
UPLOAD_FOLDER = './code'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def health_check():
    return {'message': f'Hello World from {socket.gethostname()}!'}, 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _unzip_file():
    with zipfile.ZipFile("./code/extract_me.zip", mode="r") as archive:
        archive.extractall(path="./code")

def _run_client_code():
    os.system("python3 ./code/run_me.py > ./code/output.txt")

def _delete_temp_files():
    files = glob.glob('./code/*')
    print(files)
    for f in files:
        os.remove(f)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _unzip_file()
            _run_client_code()

            response = {
                'status': 'success',
                'output': open('./code/output.txt', 'r').read(),
                'hostname': socket.gethostname()
            }

            _delete_temp_files()

            return response

    return 


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
