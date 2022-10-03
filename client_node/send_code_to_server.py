import logging
import os, requests, zipfile
import json

logging.basicConfig(level=logging.INFO)

SERVER_ADDRESS, SERVER_PORT = "10.105.150.56", "5000"

# Zipping student code
zipfile.ZipFile("extract_me.zip", mode="w").write("run_me.py")

try:
    # Sending student code to server
    response = requests.post(f"http://{SERVER_ADDRESS}:{SERVER_PORT}/", files={"file": open("extract_me.zip", "rb")})
    logging.info("*********  Resposta do servidor ******** \n")
    logging.info(json.dumps(response.json(), indent=4, sort_keys=True))

except Exception as e:
    logging.error(e)
finally:
    # Cleaning up
    logging.info("Cleaning up")
    os.remove('./extract_me.zip')
