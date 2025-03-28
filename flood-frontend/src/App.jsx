import FloodForm from "./components/FloodForm";
import './App.css';

function App() {
  return (
    <div className="app-container">
      <h1 className="app-title">AI Flood Prediction System</h1>
      <div className="content-wrapper">
        <FloodForm />
      </div>
    </div>
  );
}

export default App;