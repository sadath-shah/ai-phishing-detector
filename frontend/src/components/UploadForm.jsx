import { useState } from "react";
import axios from "axios";

function UploadForm({ setResult }) {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!email.trim()) {
      setError("Please paste an email before analyzing.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/analyze`,
        {
          email: email.trim(),
        },
      );

      setResult(response.data);
    } catch (error) {
      console.error("Analysis error:", error);

      if (error.response) {
        const statusCode = error.response.status;
        const responseData = error.response.data;

        if (statusCode === 422) {
          setError(
            "Invalid email data. Please check the email content and try again.",
          );
        } else if (statusCode === 500) {
          setError(
            "The analysis server encountered an error. Please try again.",
          );
        } else {
          setError(
            responseData?.message ||
              responseData?.detail ||
              "The backend returned an error.",
          );
        }
      } else if (error.request) {
        setError(
          "Unable to connect to the analysis server. Please make sure the backend is running.",
        );
      } else {
        setError(
          "Something went wrong while analyzing the email. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-box">
      <div className="upload-header">
        <div>
          <h2>Paste Email Content</h2>

          <p>
            Paste the complete email content below for AI-powered threat
            analysis.
          </p>
        </div>

        <span className="input-status">Secure Analysis</span>
      </div>

      <textarea
        rows="10"
        placeholder="Paste suspicious email content here..."
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);

          if (error) {
            setError("");
          }
        }}
        disabled={loading}
      />

      <div className="upload-footer">
        <span className="character-count">{email.length} characters</span>

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? (
            <>
              <span className="loading"></span>
              Analyzing...
            </>
          ) : (
            <>🔍 Analyze Email</>
          )}
        </button>
      </div>

      {error && <div className="error-message">❌ {error}</div>}
    </div>
  );
}

export default UploadForm;
