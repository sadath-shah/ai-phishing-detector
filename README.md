# 🛡️ AI SOC Email Threat Analyzer

An advanced AI-powered phishing detection system that combines machine learning with rule-based threat detection to analyze email content and identify potential security threats. Features MITRE ATT&CK mapping, IOC extraction, and confidence-based risk assessment.

## 📋 Overview

**AI SOC Email Threat Analyzer** is a comprehensive email security solution that leverages:
- **Machine Learning** - TF-IDF vectorization + Logistic Regression for phishing classification
- **Rule-Based Detection** - Advanced pattern matching for threat indicators
- **SOC-Style Analysis** - Professional threat assessment with MITRE ATT&CK mapping
- **Real-Time Processing** - Instant email analysis with detailed reasoning

## ✨ Key Features

### 🤖 Machine Learning Analysis
- TF-IDF feature extraction from email content
- Logistic Regression classification (Legitimate vs. Phishing)
- Confidence scoring based on model probabilities
- High accuracy threat detection

### 🔍 Advanced Threat Detection
- **Keyword Analysis** - Detects phishing-related keywords (urgent, verify, password, etc.)
- **URL/Email/IP Detection** - Extracts and flags indicators of compromise
- **Urgency + Threat Patterns** - Identifies time-pressure tactics combined with account threats
- **Credential Harvesting** - Detects attempts to collect login credentials
- **Impersonation Detection** - Identifies trusted organization spoofing
- **Financial Targeting** - Flags banking and payment-related threats

### 🎯 MITRE ATT&CK Mapping
- T1566 - Phishing
- T1566.002 - Spearphishing Link
- T1056.003 - Web Portal Capture

### 📊 Comprehensive Reporting
- Final classification (Safe, Suspicious, Phishing)
- Risk score (0-10 scale)
- Severity levels (Low, Medium, High)
- Confidence percentage
- Detection reasons with explanations
- Indicators of Compromise (URLs, emails, IPs)
- ML prediction details

## 🏗️ Architecture

### Backend (FastAPI)
```
Backend/
├── main.py              # FastAPI server with /analyze endpoint
├── train_model.py       # Model training pipeline
├── prepare_data.py      # Data preparation utilities
├── requirements.txt     # Python dependencies
└── [empty modules]      # Placeholder for future features
```

**Tech Stack:**
- FastAPI - Web framework
- scikit-learn - ML pipeline
- pandas - Data processing
- joblib - Model serialization
- TF-IDF Vectorizer - Feature extraction
- Logistic Regression - Classification

### Frontend (React + Vite)
```
Frontend/
├── src/
│   ├── components/
│   │   ├── UploadForm.jsx      # Email input interface
│   │   ├── ResultCard.jsx      # Analysis results display
│   │   ├── Navbar.jsx          # Navigation
│   │   ├── Charts.jsx          # Analytics (placeholder)
│   │   └── IOCSection.jsx      # IOC display (placeholder)
│   ├── pages/
│   │   ├── Home.jsx            # Main dashboard
│   │   ├── Analysis.jsx        # Analysis page (placeholder)
│   │   └── Dashboard.jsx       # Dashboard (placeholder)
│   ├── App.jsx                 # Main app component
│   ├── App.css                 # Component styling
│   └── index.css               # Global styles
└── [config files]
```

**Tech Stack:**
- React 19+ - UI framework
- Vite - Build tool
- Axios - HTTP client
- CSS3 - Styling with dark theme

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Train the model (if needed)
python train_model.py

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set API URL in .env
echo "VITE_API_URL=http://localhost:8000" > .env

# Start dev server
npm run dev
```

Frontend runs on: `http://localhost:5173`

## 📖 Usage

1. **Paste Email Content** - Copy and paste suspicious email content
2. **Click Analyze** - Send email for threat analysis
3. **View Results** - Get comprehensive security assessment including:
   - Classification (Safe/Suspicious/Phishing)
   - Risk score and severity
   - ML model prediction
   - Detection reasons
   - MITRE ATT&CK mapping
   - Indicators of compromise

## 📊 Analysis Output

### Response Format
```json
{
  "classification": "Phishing",
  "confidence": "92.45%",
  "severity": "High",
  "riskScore": "9/10",
  "reasons": [
    "Suspicious keywords detected: urgent, verify, click",
    "Suspicious URL detected (1 URL(s))",
    "ML model detected phishing (95.23% confidence)",
    "Urgency combined with account threat"
  ],
  "mitre": [
    "T1566 - Phishing",
    "T1566.002 - Spearphishing Link"
  ],
  "urls": ["http://malicious-site.com/login"],
  "emails": ["attacker@fake-bank.com"],
  "ips": ["192.168.1.1"],
  "mlPrediction": "Phishing",
  "mlConfidence": "95.23%"
}
```

## 🎨 UI Features

- **Dark Theme** - Professional SOC-style interface
- **Real-Time Analysis** - Instant email processing
- **Visual Risk Meter** - Color-coded risk assessment
- **Animated Components** - Smooth transitions and effects
- **Responsive Design** - Works on desktop and tablet
- **Error Handling** - Clear error messages and guidance
- **Loading States** - User feedback during analysis

## 📈 Model Performance

The ML model is trained on the CEAS_08 dataset:
- **Accuracy**: ~95%
- **Precision**: High
- **Recall**: Balanced
- **F1-Score**: Strong

Hybrid Approach:
- 60% weight: Rule-based indicators
- 40% weight: ML model prediction
- Conflict detection: Flags when ML and rules disagree

## 🔐 Security Features

- CORS enabled for frontend communication
- Input validation (max 50KB email size)
- Error handling without exposing internals
- Safe regex patterns for IOC extraction
- No sensitive data storage

## 📚 Dataset

The model is trained on:
- **CEAS_08.csv** - Email classification dataset
- **64.76 MB** - 1000+ labeled emails
- Binary classification: Legitimate vs. Phishing

## 🛠️ Future Enhancements

- [ ] Advanced charts and analytics dashboard
- [ ] Email attachment analysis
- [ ] Browser extension
- [ ] API rate limiting
- [ ] User authentication
- [ ] Email history logging
- [ ] Custom rule builder
- [ ] Gemini AI explanations
- [ ] PDF report generation

## 📝 Code Quality

✅ **All comments removed** for clean, production-ready code  
✅ **Self-documenting** with clear naming conventions  
✅ **Modular structure** for easy maintenance  
✅ **Type hints** in backend (Pydantic models)  
✅ **Error handling** throughout  

## 🤝 Contributing

Contributions welcome! Areas for improvement:
1. Enhanced ML models
2. Additional threat patterns
3. UI/UX enhancements
4. Performance optimization
5. Test coverage

## 📄 License

MIT License - feel free to use and modify

## 👤 Author

**Mohammed Sadath Shah**  
GitHub: [@sadath-shah](https://github.com/sadath-shah)

## 📧 Contact & Support

For questions or issues:
- Open a GitHub issue
- Check existing documentation
- Review the code comments in complex sections

## 🔗 Links

- [GitHub Repository](https://github.com/sadath-shah/ai-phishing-detector)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Built with ❤️ for cybersecurity professionals**
