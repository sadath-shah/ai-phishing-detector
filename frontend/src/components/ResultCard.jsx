const toClassName = (value) =>
  String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-");

const normalizeList = (value) => (Array.isArray(value) ? value : []);

const getConfidenceWidth = (value) => {
  const parsedValue =
    typeof value === "number" ? value : Number.parseFloat(String(value || ""));

  if (Number.isNaN(parsedValue)) {
    return "0%";
  }

  return `${Math.min(Math.max(parsedValue, 0), 100)}%`;
};

const getRiskNumber = (riskScore) => {
  const parsedValue = Number.parseInt(
    String(riskScore || "0").split("/")[0],
    10,
  );

  if (Number.isNaN(parsedValue)) {
    return 0;
  }

  return Math.min(Math.max(parsedValue, 0), 10);
};

const getRiskPercentage = (riskScore) => {
  const score = getRiskNumber(riskScore);

  return (score / 10) * 100;
};

const getRiskLevel = (riskScore) => {
  const score = getRiskNumber(riskScore);

  if (score >= 7) {
    return "HIGH RISK";
  }

  if (score >= 4) {
    return "MEDIUM RISK";
  }

  return "LOW RISK";
};

const getRiskClass = (riskScore) => {
  const score = getRiskNumber(riskScore);

  if (score >= 7) {
    return "high";
  }

  if (score >= 4) {
    return "medium";
  }

  return "low";
};

function ResultCard({ result = {} }) {
  const classification = result.classification || "Unknown";

  const severity = result.severity || "Unknown";

  const riskScore = result.riskScore || result.risk_score || "0/10";

  const confidence = result.confidence || "0%";

  const reasons = normalizeList(result.reasons);

  const urls = normalizeList(result.urls);

  const emails = normalizeList(result.emails || result.emailAddresses);

  const ips = normalizeList(result.ips || result.ipAddresses);

  const mlPrediction =
    result.mlPrediction || result.ml_prediction || "Not available";

  const mlConfidence =
    result.mlConfidence || result.ml_confidence || "Not available";

  const mitre = result.mitre || "None";

  const totalIocs = urls.length + emails.length + ips.length;

  return (
    <div className="result-card">
      <div className="result-header">
        <div>
          <h2>Security Analysis</h2>

          <p>AI and SOC-based email threat analysis</p>
        </div>

        <span className="analysis-status">Analysis Complete</span>
      </div>

      <div className="result-summary">
        <div className="result-item">
          <span className="result-label">Final Classification</span>

          <span className={`classification ${toClassName(classification)}`}>
            {classification}
          </span>
        </div>

        <div className="result-item">
          <span className="result-label">Severity</span>

          <span className={`severity ${toClassName(severity)}`}>
            {severity}
          </span>
        </div>

        <div className="result-item risk-item">
          <span className="result-label">Risk Score</span>

          <div className="risk-score-display">
            <span className="risk-score">{riskScore}</span>

            <span className={`risk-level ${getRiskClass(riskScore)}`}>
              {getRiskLevel(riskScore)}
            </span>
          </div>

          <div className="risk-meter">
            <div
              className={`risk-meter-fill ${getRiskClass(riskScore)}`}
              style={{
                width: `${getRiskPercentage(riskScore)}%`,
              }}
            />
          </div>
        </div>
      </div>

      <div className="analysis-section">
        <h3>🤖 Machine Learning Analysis</h3>

        <div className="ml-grid">
          <div className="ml-item">
            <span>ML Prediction</span>

            <strong
              className={
                mlPrediction === "Phishing"
                  ? "ml-phishing"
                  : mlPrediction === "Legitimate"
                    ? "ml-legitimate"
                    : ""
              }
            >
              {mlPrediction}
            </strong>
          </div>

          <div className="ml-item">
            <span>ML Confidence</span>

            <strong>{mlConfidence}</strong>
          </div>
        </div>
      </div>

      <div className="analysis-section">
        <h3>Final Confidence</h3>

        <div className="confidence-container">
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{
                width: getConfidenceWidth(confidence),
              }}
            />
          </div>

          <span className="confidence-value">{confidence}</span>
        </div>
      </div>

      <div className="analysis-section">
        <h3>🔍 Detection Reasons</h3>

        {reasons.length > 0 ? (
          <ul className="reason-list">
            {reasons.map((reason, index) => (
              <li key={index}>
                <span className="reason-icon">⚠</span>

                <span>{reason}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p>No suspicious indicators detected.</p>
        )}
      </div>

      <div className="analysis-section">
        <h3>🎯 MITRE ATT&CK</h3>

        <div className="mitre-box">
          <span className="mitre-label">Detected Techniques</span>

          {Array.isArray(mitre) && mitre.length > 0 ? (
            <ul className="mitre-list">
              {mitre.map((technique, index) => (
                <li key={index}>{technique}</li>
              ))}
            </ul>
          ) : (
            <strong>None</strong>
          )}
        </div>
      </div>

      <div className="ioc-section">
        <div className="ioc-header">
          <div>
            <h3>🚨 Indicators of Compromise</h3>

            <p>Potential indicators identified during analysis</p>
          </div>

          <span className="ioc-count">
            {totalIocs} {totalIocs === 1 ? "Indicator" : "Indicators"}
          </span>
        </div>

        <div className="ioc-grid">
          <div className="ioc-card">
            <div className="ioc-card-header">
              <span className="ioc-icon">🔗</span>

              <div>
                <h4>URLs</h4>

                <span>{urls.length} detected</span>
              </div>
            </div>

            {urls.length > 0 ? (
              <ul className="ioc-list">
                {urls.map((url, index) => (
                  <li key={index}>
                    <span className="ioc-indicator">⚠</span>

                    <span className="ioc-value">{url}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="ioc-empty">No URLs detected</p>
            )}
          </div>

          <div className="ioc-card">
            <div className="ioc-card-header">
              <span className="ioc-icon">📧</span>

              <div>
                <h4>Email Addresses</h4>

                <span>{emails.length} detected</span>
              </div>
            </div>

            {emails.length > 0 ? (
              <ul className="ioc-list">
                {emails.map((email, index) => (
                  <li key={index}>
                    <span className="ioc-indicator">⚠</span>

                    <span className="ioc-value">{email}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="ioc-empty">No email addresses detected</p>
            )}
          </div>

          <div className="ioc-card">
            <div className="ioc-card-header">
              <span className="ioc-icon">🌐</span>

              <div>
                <h4>IP Addresses</h4>

                <span>{ips.length} detected</span>
              </div>
            </div>

            {ips.length > 0 ? (
              <ul className="ioc-list">
                {ips.map((ip, index) => (
                  <li key={index}>
                    <span className="ioc-indicator">⚠</span>

                    <span className="ioc-value">{ip}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="ioc-empty">No IP addresses detected</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
