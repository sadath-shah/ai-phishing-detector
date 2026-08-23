import { useState } from "react";
import UploadForm from "../components/UploadForm";
import ResultCard from "../components/ResultCard";

function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-icon">🛡️</div>

          <div>
            <h1>AI SOC Email Threat Analyzer</h1>

            <p>AI-powered phishing and threat detection</p>
          </div>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>

      <main className="dashboard-content">
        <section className="analyzer-section">
          <div className="section-heading">
            <div>
              <h2>Email Threat Analysis</h2>

              <p>
                Analyze suspicious email content using machine learning and
                SOC-based threat detection.
              </p>
            </div>
          </div>

          <UploadForm setResult={setResult} />
        </section>

        {result && (
          <section className="results-section">
            <ResultCard result={result} />
          </section>
        )}
      </main>

      <footer className="dashboard-footer">
        <span>AI SOC Email Threat Analyzer</span>

        <span>ML Detection • IOC Analysis • MITRE ATT&CK</span>
      </footer>
    </div>
  );
}

export default Home;
