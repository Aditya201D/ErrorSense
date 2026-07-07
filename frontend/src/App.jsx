import { useEffect, useState } from "react";
import axios from "axios";

import "./App.css";
import ResultCard from "./components/ResultCard";
import Sidebar from "./components/Sidebar";
import ThemeToggle from "./components/ThemeToggle";
import { useTheme } from "./hooks/useTheme";

const HISTORY_KEY = "rrc-history";
const SIDEBAR_KEY = "rrc-sidebar-collapsed";
const MAX_HISTORY = 25;

function loadHistory() {
  try {
    const raw = window.localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    return [];
  }
}

function App() {
  const [requestText, setRequestText] = useState("");
  const [responseText, setResponseText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [history, setHistory] = useState(loadHistory);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    try {
      return window.localStorage.getItem(SIDEBAR_KEY) === "true";
    } catch (e) {
      return false;
    }
  });

  const { theme, toggleTheme } = useTheme();

  // Persist sidebar state
  useEffect(() => {
    try {
      window.localStorage.setItem(SIDEBAR_KEY, String(sidebarCollapsed));
    } catch (e) {
      // ignore
    }
  }, [sidebarCollapsed]);

  // Persist history
  useEffect(() => {
    try {
      window.localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch (e) {
      // ignore
    }
  }, [history]);

  const addToHistory = (entry) => {
    setHistory((prev) => {
      // De-dupe by request+response combination
      const filtered = prev.filter(
        (h) => h.request !== entry.request || h.response !== entry.response
      );
      return [entry, ...filtered].slice(0, MAX_HISTORY);
    });
  };

  const analyse = async () => {
    if (!requestText.trim() && !responseText.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        {
          request: requestText,
          response: responseText,
        }
      );

      setResult(response.data);

      addToHistory({
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        request: requestText,
        response: responseText,
        category: response.data.category,
        confidence: response.data.confidence,
        resolution: response.data.resolution,
        timestamp: Date.now(),
      });
    } catch (error) {
      console.error(error);

      setResult({
        category: "Connection Error",
        resolution: "Unable to connect to backend service.",
        alternatives: [],
      });
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setRequestText("");
    setResponseText("");
    setResult(null);
  };

  const handleSelectHistory = (item) => {
    setRequestText(item.request || "");
    setResponseText(item.response || "");
    if (item.category || item.resolution) {
      setResult({
        category: item.category,
        resolution: item.resolution,
        confidence: item.confidence,
        alternatives: [],
      });
    }
  };

  const handleDeleteHistory = (id) => {
    setHistory((prev) => prev.filter((h) => h.id !== id));
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="app">
      <Sidebar
        history={history}
        onSelect={handleSelectHistory}
        onDelete={handleDeleteHistory}
        onClear={handleClearHistory}
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((c) => !c)}
      />

      <div
        className={`app-main ${
          sidebarCollapsed ? "sidebar-collapsed" : "sidebar-expanded"
        }`}
      >
        <header className="topbar">
          <div className="topbar-left">
            <h1>Request Response Categoriser</h1>
            <p>Intelligent Error Analysis Assistant</p>
          </div>
          <div className="topbar-right">
            <ThemeToggle theme={theme} onToggle={toggleTheme} />
          </div>
        </header>

        <main className="dashboard">
          <section className="panel input-panel">
            <h2>Input Data</h2>

            <div className="field">
              <label>Request Payload</label>
              <textarea
                value={requestText}
                onChange={(e) => setRequestText(e.target.value)}
                placeholder="Paste request payload..."
              />
            </div>

            <div className="field">
              <label>Response Message</label>
              <textarea
                value={responseText}
                onChange={(e) => setResponseText(e.target.value)}
                placeholder="Paste response message..."
              />
            </div>

            <div className="actions">
              <button className="analyse-btn" onClick={analyse}>
                Analyse
              </button>
              <button className="clear-btn" onClick={clearAll}>
                Clear
              </button>
            </div>
          </section>

          <section className="panel results-panel">
            <div className="results-header">
              <h2>Analysis Results</h2>
              {loading && <span className="loader">Analysing...</span>}
            </div>

            {!loading && <ResultCard result={result} />}
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;
