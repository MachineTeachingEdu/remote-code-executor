import CodeEditor from "./CodeEditor";
import Results from "./Results";
import "./App.css";
import "antd/dist/antd.min.css";
import { useState } from "react";

function App() {
  const [executionResults, setExecutionResults] = useState([]);
  const [loading, setLoading] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <h1
          style={{
            fontSize: window.innerWidth > 1000 ? "3rem" : "2rem",
            fontWeight: 700,
            lineHeight: 0.8,
            margin: 0,
            color: "#fff",
          }}
        >
          Machine Teaching
        </h1>
        <p style={{ margin: "0 0 3rem 0" }}>Beta</p>
      </header>
      <div className="App-body">
        <div
          style={{
            width: window.innerWidth < 800 ? "100%" : "60%",
            padding: "10px",
          }}
        >
          <CodeEditor
            loading={(v) => setLoading(v)}
            addResult={(result) =>
              setExecutionResults([...executionResults, result])
            }
          />
        </div>
        <div
          style={{
            width: window.innerWidth < 800 ? "100%" : "40%",
            padding: "10px",
          }}
        >
          <Results executionResults={executionResults} loading={loading} />
        </div>
      </div>
    </div>
  );
}

export default App;
