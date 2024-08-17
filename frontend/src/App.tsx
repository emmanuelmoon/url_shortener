import axios from "axios";
import "./App.css";
import { useState } from "react";

function App() {
  const [URL, setURL] = useState<string>("");
  const [shortenedURL, setShortenedURL] = useState<string>("");
  const [error, setError] = useState<string>("");
  function handleClick(e: { [x: string]: any; preventDefault: () => void }) {
    e.preventDefault();
    axios
      .post("api", {
        url: URL,
      })
      .then((response) => {
        setShortenedURL(`Shortened URL ${response.data.short_url}`);
        setTimeout(() => {
          setShortenedURL("");
        }, 5000);
      })
      .catch((error) => {
        setError(`Error: ${error.response.data}`);
        setTimeout(() => {
          setError("");
        }, 1800);
      });
  }

  return (
    <div>
      <form>
        <label>
          URL:{" "}
          <input
            type="text"
            value={URL}
            onChange={(e) => setURL(e.target.value)}
          />
        </label>
        <button onClick={handleClick}>Shorten</button>
      </form>
      {shortenedURL || null}
      <p style={{ color: "red" }}>{error || null}</p>
    </div>
  );
}

export default App;
