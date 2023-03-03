from pathlib import Path
from flask import Flask, request,  abort
from werkzeug.utils import secure_filename
import os
import zipfile
import glob
import socket
from evaluation import evaluate_file
from exceptions import DangerException, CodeException
from flask_cors import CORS
import uuid
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
BASE_DIR = (Path(__file__).parent / "code").absolute()

app = Flask(__name__)
CORS(app)

def _valid_file(filename):
    logging.info(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

def _unzip_file(folder: Path, file_name):
    with zipfile.ZipFile(f"{folder}/{file_name}", mode="r") as archive:
        archive.extractall(path=folder.as_posix())

    return (folder / "run_me.py").as_posix()

def _run_client_code(folder: Path, file_path):
    result = subprocess.run(["python3", f"{file_path}"], capture_output=True, text=True)


    # print("Result",    result.stdout)
    if result.stderr != "":
        raise CodeException(result.stderr)
    # print("error",    result.stderr)
    return result.stdout


def _delete_temp_files(folder: Path):
    for f in glob.glob(folder.as_posix() + '/*'):
        os.remove(f)

    os.rmdir(folder.as_posix())

@app.route('/', methods=['GET'])
def health_check():
    return {'message': f'Hello World from {socket.gethostname()}!'}, 200


@app.route('/', methods=['POST'])
def upload_file():

    logging.info(request.files)
    if 'file' not in request.files:
        abort(400, 'Missing submission file')

    file = request.files['file']

    if file and _valid_file(file.filename):

        unique_id = uuid.uuid4().hex
        os.makedirs(unique_id + "/code")
    
        TEMP_DIR = (Path(__file__).parent / unique_id / "code").absolute()

        compressed_file_name = secure_filename(file.filename)
        file.save(os.path.join(TEMP_DIR, compressed_file_name))

        try:
            submitted_code_path = _unzip_file(TEMP_DIR, compressed_file_name)

            evaluate_file(submitted_code_path)            
            code_output = _run_client_code(TEMP_DIR, submitted_code_path)

            result = {
                'output': code_output,
                'hostname': socket.gethostname()
            }
            status_code = 200

        except CodeException as e:
            result = {
                'output': str(e),
                'hostname': socket.gethostname()
            }
            status_code = 400

        except DangerException as e:
            result = {
                'output': e.message,
                'hostname': socket.gethostname()
            }
            status_code = 403

        except Exception as e:
            return str(e), 500
        
        _delete_temp_files(TEMP_DIR)

        return result, status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
