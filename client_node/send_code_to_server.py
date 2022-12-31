import logging
import os, requests, zipfile
import json
from pathlib import Path
logging.basicConfig(level=logging.INFO)

current_path = Path(__file__).parent.absolute().as_posix()

SERVER_ADDRESS = "http://34.136.57.11:80"
# Zipping student code
zipfile.ZipFile(f"extract_me.zip", mode="w").write(f"run_me.py")

try:
    # Sending student code to server
    response = requests.post(f"{SERVER_ADDRESS}/", files={"file": open(f"extract_me.zip", "rb")}, timeout=5)
    logging.info("*********  Resposta do servidor ******** \n")
    logging.info(json.dumps(response.json(), indent=4, sort_keys=True))

except Exception as e:
    logging.error(e)
finally:
    # Cleaning up
    logging.info("Cleaning up")
    os.remove(f'extract_me.zip')
