from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import csv
from datetime import datetime
from flask import render_template

from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from matcher import Matcher

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

parser = ResumeParser()
extractor = SkillExtractor()
matcher = Matcher()


# ─────────────────────────────────────────────
# ANALYZE ROUTE
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        skills_raw = request.form.get("skills", "")
        top_k = int(request.form.get("top_k", 5))

        files = request.files.getlist("files")

        file_paths = []

        # save uploaded files temporarily
        for f in files:
            save_path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(save_path)
            file_paths.append(save_path)

        # 1. Parse resumes
        resumes = parser.parse_multiple(file_paths)

        # 2. Extract skills
        for r in resumes:
            r["skills"] = extractor.extract(r.get("raw_text", ""))

        # 3. Required skills
        required = [s.strip() for s in skills_raw.split(",") if s.strip()]
        required = extractor.normalize_list(required)

        # 4. Match + rank
        results = matcher.rank(resumes, required, top_k)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# EXPORT CSV ROUTE
# ─────────────────────────────────────────────
@app.route("/export_csv", methods=["POST"])
def export_csv():
    try:
        results = request.get_json()

        if not results:
            return jsonify({"error": "No data"}), 400

        filename = f"resume_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        fields = [
            "Rank", "Name", "Email", "Phone", "Match %",
            "Matched Skills", "Missing Skills", "All Skills", "Filename"
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for i, r in enumerate(results, 1):
                writer.writerow({
                    "Rank": i,
                    "Name": r.get("name", ""),
                    "Email": r.get("email", ""),
                    "Phone": r.get("phone", ""),
                    "Match %": r.get("match_pct", ""),
                    "Matched Skills": "; ".join(r.get("matched_skills", [])),
                    "Missing Skills": "; ".join(r.get("missing_skills", [])),
                    "All Skills": "; ".join(r.get("skills", [])),
                    "Filename": r.get("filename", "")
                })

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────
# RUN SERVER
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)