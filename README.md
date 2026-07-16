# 🤖 AI Resume Screening System

An AI-powered resume screening system that automatically analyzes resumes, extracts candidate information, and ranks applicants based on how well they match a given job's required skills.

Built using Python, Flask, and Natural Language Processing (NLP), the system helps streamline the recruitment process by reducing manual resume screening and providing recruiters with ranked candidate insights.

---

## 🚀 Features

- 📄 Upload multiple resumes (PDF & DOCX)
- 🧠 AI-based resume parsing using NLP
- 🔍 Automatic extraction of:
  - Candidate Name
  - Email Address
  - Phone Number
  - Technical Skills
- ⚡ Skill normalization (handles abbreviations & synonyms)
- 🎯 Intelligent skill matching with fuzzy matching
- 📊 Candidate ranking based on match percentage
- 📈 Interactive charts and visual analytics
- 📥 Export screening results as CSV

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### NLP & Processing
- PyPDF2
- python-docx
- RapidFuzz

### Frontend
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```
AI-Resume-Screening-System/
│
├── app.py
├── resume_parser.py
├── skill_extractor.py
├── matcher.py
├── templates/
├── static/
├── uploads/
├── exports/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Resume-Screening-System.git

cd AI-Resume-Screening-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## 💡 How It Works

1. Upload one or more resumes.
2. Enter the required job skills.
3. The system extracts text from each resume.
4. Skills are identified and normalized.
5. Candidates are matched against the required skills.
6. Applicants are ranked by their match percentage.
7. View detailed results and export them if needed.

---

## 📊 Example Workflow

Resume Upload
        ↓
Text Extraction
        ↓
Information Parsing
        ↓
Skill Extraction
        ↓
Skill Matching
        ↓
Candidate Ranking
        ↓
Visualization & Export

---

## 🎯 Use Cases

- HR Recruitment
- Resume Shortlisting
- Internship Hiring
- Campus Recruitment
- Technical Hiring
- Initial Candidate Screening

---

## 🔮 Future Improvements

- OCR support for scanned resumes
- Job Description parsing
- Experience detection
- Education extraction
- AI-based semantic matching using BERT
- User authentication
- PDF & Excel export
- Advanced analytics dashboard

---

## 🤝 Contributors

- Harsh Kumar
- Sahil Kumar
- Jitesh Kumar

---

## 📜 License

This project was developed for educational purposes as part of an Artificial Intelligence course.

---

⭐ If you found this project useful, consider giving it a star!
