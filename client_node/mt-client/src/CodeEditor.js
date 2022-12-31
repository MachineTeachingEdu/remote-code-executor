import React from "react";
import Editor from "react-simple-code-editor";
import { highlight, languages } from "prismjs/components/prism-core";
import axios from "axios";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-funky.css"; // Example style, you can use another
import "prismjs/components/prism-python.js";
import { notification } from "antd";

const exampleCode = `# Escreva o código a ser processado pelo servidor

num1 = 10
num2 = 14
num3 = 12

maior = None

if (num1 >= num2) and (num1 >= num3):
    maior = num1
elif (num2 >= num1) and (num2 >= num3):
    maior = num2
else:
    maior = num3

print("O maior número é ", maior)`;

function CodeEditor() {
  const [code, setCode] = React.useState(exampleCode);

  const openNotificationWithIcon = (type, title, message) => {
    notification[type]({
      message: title,
      description: message,
    });
  };

  const sendCodeToServer = async () => {
    const zip = require("jszip")();
    zip.file("run_me.py", code);

    var formData = new FormData();
    const willSendthis = await zip.generateAsync({ type: "blob" });
    formData.append("file", willSendthis, "extract-me.zip");

    try {
      const response = await axios.post("http://34.136.57.11:80/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      openNotificationWithIcon(
        "success",
        "Código executado com sucesso",
        response.data.output
      );
    } catch (error) {
      openNotificationWithIcon("error", "Erro", error.response.data);
    }
  };

  return (
    <>
      <div
        style={{
          width: window.innerWidth > 1000 ? "50vw" : "90vw",
          height: "500px",
          overflow: "auto",
        }}
      >
        <Editor
          value={code}
          onValueChange={(code) => setCode(code)}
          highlight={(code) => highlight(code, languages.python)}
          tabSize={4}
          padding={20}
          style={{
            fontFamily: '"Fira code", "Fira Mono", monospace',
            fontSize: window.innerWidth > 800 ? 20 : 12,
            backgroundColor: "#111",
          }}
        />
      </div>
      <button className="mtButton" onClick={sendCodeToServer}>
        Executar
      </button>
    </>
  );
}

export default CodeEditor;
