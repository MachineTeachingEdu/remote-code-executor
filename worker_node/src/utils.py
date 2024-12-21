import os

def is_running_in_container():
    if os.getenv("RUNNING_IN_DOCKER", "False") == "True":
        print("Estou no container!!")
        return True
    print("Não estou no container!!")
    return False