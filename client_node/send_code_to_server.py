import os, requests, zipfile
import json
SERVER_ADDRESS, SERVER_PORT = "10.105.150.56", "5000"

# Zipping student code
zipfile.ZipFile("extract_me.zip", mode="w").write("run_me.py")

# Sending student code to server
response = requests.post(f"http://{SERVER_ADDRESS}:{SERVER_PORT}/", files={"file": open("extract_me.zip", "rb")})

print("*********  Resposta do servidor ******** \n")
print(json.dumps(response.json(), indent=4, sort_keys=True))
# Cleaning up
os.remove('./extract_me.zip')