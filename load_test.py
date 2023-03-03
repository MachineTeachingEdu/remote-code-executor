
import io
import zipfile
from locust import HttpUser, task, between
import zlib
import textwrap

class LoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        code = textwrap.dedent("""\
        def multiples_of_3_or_5():
            for number in range(1000):
                if not number % 3 or not number % 5:
                    yield number

        print("Result:")
        print(sum(multiples_of_3_or_5()))
        """)

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a",
                            zipfile.ZIP_DEFLATED, False) as zip_file:

            zip_file.writestr('run_me.py', io.BytesIO(code.encode('utf-8')).getvalue())

        with open('extract-me.zip', 'wb') as f:
            f.write(zip_buffer.getvalue())

        response = self.client.post("/", 
        headers={
            "accept": "application/json, text/plain, */*",
        },
        files={"file": ("extract-me.zip", open("extract-me.zip", "rb"))}
        );

        print(response.text)



