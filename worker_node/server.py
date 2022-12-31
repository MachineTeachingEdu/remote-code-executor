from pathlib import Path
from flask import Flask, request,  abort
from werkzeug.utils import secure_filename
import os
import zipfile
import glob
import socket
from evaluation import evaluate_file
from exceptions import DangerException
from flask_cors import CORS

BASE_DIR = (Path(__file__).parent / "code").absolute()

app = Flask(__name__)
CORS(app)

def _valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

def _unzip_file(file_name):
    with zipfile.ZipFile(f"{BASE_DIR}/{file_name}", mode="r") as archive:
        archive.extractall(path=BASE_DIR.as_posix())

    return (BASE_DIR / "run_me.py").as_posix()

def _run_client_code(file_path):
    os.system(f'python3 "{file_path}" > "{BASE_DIR.as_posix()}/output.txt"')

def _delete_temp_files():
    for f in glob.glob(BASE_DIR.as_posix() + '/*'):
        os.remove(f)

@app.route('/', methods=['GET'])
def health_check():
    return {'message': f'Hello World from {socket.gethostname()}!'}, 200


@app.route('/', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        abort(400, 'Missing submission file')

    file = request.files['file']

    if file and _valid_file(file.filename):
        compressed_file_name = secure_filename(file.filename)
        file.save(os.path.join(BASE_DIR, compressed_file_name))

        try:
            submitted_code_path = _unzip_file(compressed_file_name)

            evaluate_file(submitted_code_path)            
            _run_client_code(submitted_code_path)

        except DangerException:
            return 'Potential malicious code', 403

        except Exception as e:
            return str(e), 500
        
        _delete_temp_files()

        return {
                'status': 'success',
                'output': open((BASE_DIR / 'output.txt').as_posix(), 'r').read(),
                'hostname': socket.gethostname()
            }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
