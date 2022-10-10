import CodeEditor from "./CodeEditor";
import "./App.css";
import "antd/dist/antd.min.css";

function App() {
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
        <CodeEditor />
      </header>
    </div>
  );
}

export default App;
