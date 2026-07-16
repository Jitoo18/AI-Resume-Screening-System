"""
Automated Resume Screening System using NLP
============================================
A web application for recruiters to analyze and rank resumes.
"""

from app import app


def main():
    """Entry point for the Resume Screening System."""
    print("Starting the Resume Screening Web Application...")
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
