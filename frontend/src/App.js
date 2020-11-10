import './App.css';
import './FileUpload';
import { FileUpload } from './FileUpload';
import demo from './input/putinTrump.gif';
function App() {

  
  return (
    <div className="App">
      <header>Deepfake</header>
      <body>
        <img src={demo} />
        <p>How does it work?</p>
        <p>Upload an image of yourself and a video. The two will be merged!</p>
        <p>Upload a face picture (min 256x256) and a video (max 256x256). </p>
        <FileUpload />
      </body>
    </div>
  );
}

export default App;
