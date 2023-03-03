import React from "react";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-funky.css"; // Example style, you can use another
import "prismjs/components/prism-python.js";
import LoadingSpinner from "./components/Spinner";
import {
  CheckCircleTwoTone,
  ExclamationCircleTwoTone,
} from "@ant-design/icons";

const ResultCard = ({
  server,
  resultado,
  submissionIndex,
  success,
  timeTaken,
}) => {
  return (
    <div
      style={{
        width: "100%",
        color: "#000",
        textAlign: "left",
        backgroundColor: "#fff",
        borderRadius: 10,
        fontSize: 15,
        padding: 10,
      }}
    >
      <p style={{ display: "flex", width: "100%", alignItems: "center" }}>
        {success ? (
          <CheckCircleTwoTone
            style={{ fontSize: "26px" }}
            twoToneColor="#00ff00"
          />
        ) : (
          <ExclamationCircleTwoTone
            style={{ fontSize: "26px" }}
            twoToneColor="#ff0000"
          />
        )}
        <b style={{ marginLeft: 14 }}>Submissão {submissionIndex}</b>
      </p>
      <p>{resultado}</p>
      <p>
        <b>Server:</b> {server}
      </p>
      <p>
        <b>Tempo total:</b> {timeTaken} ms
      </p>
    </div>
  );
};

function Results({ executionResults, loading }) {
  // const [code, setCode] = React.useState(exampleCode);

  // if (loading) {
  // return <>Carregando...</>;
  // }

  return (
    <div style={{ width: "100%", maxHeight: 500, overflowY: "auto" }}>
      {loading ? (
        <div style={{ display: "flex", justifyContent: "center", padding: 30 }}>
          <LoadingSpinner />
        </div>
      ) : null}
      {executionResults
        .map((item) => item)
        .reverse()
        .map((result, index) => (
          <div style={{ padding: 10 }}>
            <ResultCard
              success={result.success}
              resultado={result.output}
              server={result.hostname}
              timeTaken={result.timeTaken}
              submissionIndex={executionResults.length - index}
            />
          </div>
        ))}
    </div>
  );
}

export default Results;
