/* eslint-disable no-restricted-globals */
import "./App.css"
import "./FileUpload"
import { FileUpload } from "./FileUpload"
import { ResultViewer } from "./ResultViewer"
import putinTrumpGif from "./input/putinTrump.gif"
const queryId = new URLSearchParams(location.search).get("id")

function App() {
  return queryId !== null ? (
    <ResultViewer id={queryId} />
  ) : (
    <div className="App">
      <header>Deepfake</header>
      <body>
        <img alt="Demonstration gif" src={putinTrumpGif} />
        <p>How does it work?</p>
        <p>Upload an image of yourself and a video. The two will be merged!</p>
        <p>Upload a face picture (min 256x256) and a video (max 256x256). </p>
        <FileUpload />
      </body>
    </div>
  )
}

export default App
