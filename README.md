# AI SOC Email Threat Analyzer

An AI-assisted phishing email analysis application that combines machine learning classification with rule-based threat indicators to help identify suspicious email content.

The application uses a React frontend and a FastAPI backend to analyse email text and present a structured security assessment.

**Repository:** [ai-phishing-detector](https://github.com/sadath-shah/ai-phishing-detector)

## Features

- **Machine learning classification:** Uses TF-IDF text features and a scikit-learn Logistic Regression classifier to distinguish legitimate emails from potential phishing emails.
- **Rule-based threat analysis:** Examines email content for suspicious keywords, urgency patterns, impersonation indicators and credential-harvesting language.
- **Risk assessment:** Presents a classification, risk score, severity level and confidence information based on the implemented analysis logic.
- **IOC extraction:** Identifies supported indicators such as URLs, email addresses and IP addresses in the submitted content.
- **MITRE ATT&CK mapping:** Associates relevant detection findings with applicable phishing-related techniques where supported by the implemented rules.
- **Web interface:** Provides a React-based interface for submitting email content and reviewing analysis results.
- **API integration:** Uses FastAPI to expose the analysis functionality to the frontend.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Machine Learning | scikit-learn, TF-IDF, Logistic Regression |
| Data Processing | pandas |
| Model Persistence | joblib |
| API Communication | REST API, Axios |

## Architecture

1. **Input:** The user submits email content through the React interface.
2. **API:** The frontend sends the content to the FastAPI backend for analysis.
3. **ML analysis:** The trained model and TF-IDF vectorizer process the email and generate a classification.
4. **Rule-based analysis:** The implemented detection rules examine suspicious patterns and extract supported indicators.
5. **Results:** The application returns the available analysis findings for display in the frontend.

## Project Structure

The repository contains separate backend, frontend, data and model directories.

- `backend/` — API and analysis logic
- `frontend/` — React user interface
- `data/` — Dataset files used by the project
- `models/` — Saved machine learning artefacts

Consult the actual repository files for the complete structure.

## Getting Started

### Prerequisites

- Python 3.9 or a compatible version supported by the backend dependencies
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/sadath-shah/ai-phishing-detector.git
cd ai-phishing-detector
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

If the saved model artefacts need to be regenerated, follow the repository's model-training instructions and run the training script:

```bash
python train_model.py
```

Start the API:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend should be available at `http://127.0.0.1:8000`.

FastAPI's interactive API documentation is normally available at `http://127.0.0.1:8000/docs` when enabled.

### 3. Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
```

Configure the frontend API URL in a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Open the local development URL printed by Vite.

**Note:** Verify the actual environment-variable name and backend configuration in the repository before following these commands. The saved model files and required dependencies must be available for analysis to work.

## Model Evaluation

The project includes a machine learning classification pipeline. Model quality should be evaluated on a held-out test dataset that is separate from the training data.

Useful evaluation measures include:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Evaluation results should be added here only after running and documenting a reproducible test.

## Limitations

- The application provides automated analysis to support investigation; its output is not proof that an email is malicious or safe.
- Machine learning predictions and rule-based findings can produce false positives and false negatives.
- MITRE ATT&CK mappings describe relevant techniques and do not independently confirm an attack.
- Evaluation performance depends on the dataset, preprocessing and evaluation methodology.

## Future Improvements

Potential areas for further development include:

- Reproducible model evaluation and comparison
- Expanded test coverage
- Additional analysis and reporting features
- API rate limiting and stronger deployment controls
- Further improvements to the analysis interface

These are proposed improvements, not claims of existing functionality.

## Author

**Mohammed Sadath Shah**

- GitHub: [sadath-shah](https://github.com/sadath-shah)
- Project: [AI SOC Email Threat Analyzer](https://github.com/sadath-shah/ai-phishing-detector)
