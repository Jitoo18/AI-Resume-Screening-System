"""
resume_parser.py
----------------
Handles extraction of text and metadata from PDF and DOCX resume files.
"""

import re
import os
import PyPDF2
import docx


class ResumeParser:
    """
    Parses PDF and DOCX resume files to extract raw text and
    candidate information (name, email, phone).
    """

    def __init__(self):
        # Regex patterns for contact info extraction
        self.email_pattern = re.compile(
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
        )
        self.phone_pattern = re.compile(
            r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}'
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self, filepath: str) -> dict:
        """
        Parse a single resume file.

        Args:
            filepath: Absolute path to the PDF or DOCX file.

        Returns:
            dict with keys: filename, raw_text, name, email, phone
        """
        ext = os.path.splitext(filepath)[1].lower()

        if ext == ".pdf":
            raw_text = self._extract_pdf(filepath)
        elif ext in (".docx", ".doc"):
            raw_text = self._extract_docx(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        filename = os.path.basename(filepath)

        return {
            "filename": filename,
            "raw_text": raw_text,
            "name": self._extract_name(raw_text, filename),
            "email": self._extract_email(raw_text),
            "phone": self._extract_phone(raw_text),
        }

    def parse_multiple(self, filepaths: list, progress_callback=None) -> list:
        """
        Parse multiple resume files with optional progress reporting.

        Args:
            filepaths: List of file paths.
            progress_callback: Optional callable(current, total) for progress bar.

        Returns:
            List of parsed resume dicts.
        """
        results = []
        total = len(filepaths)

        for i, path in enumerate(filepaths):
            try:
                parsed = self.parse(path)
                results.append(parsed)
            except Exception as e:
                # Skip unreadable files and attach error info
                results.append({
                    "filename": os.path.basename(path),
                    "raw_text": "",
                    "name": "Unknown",
                    "email": "N/A",
                    "phone": "N/A",
                    "error": str(e),
                })

            if progress_callback:
                progress_callback(i + 1, total)

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _extract_pdf(self, filepath: str) -> str:
        """Extract text from a PDF file using PyPDF2."""
        text_parts = []
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    def _extract_docx(self, filepath: str) -> str:
        """Extract text from a DOCX file using python-docx."""
        doc = docx.Document(filepath)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)

    def _extract_name(self, text: str, filename: str) -> str:
        """
        Heuristic: the candidate name is usually the first non-empty line
        of the resume that looks like a real name (no numbers/emails).
        Falls back to filename stem.
        """
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        for line in lines[:8]:
            # Skip lines that look like headers, emails, or phone numbers
            if (
                len(line.split()) >= 2
                and len(line) < 60
                and not re.search(r'[\d@]', line)
                and not any(
                    kw in line.lower()
                    for kw in ("resume", "curriculum", "vitae", "cv", "profile",
                               "summary", "objective", "address", "linkedin")
                )
            ):
                return line.title()

        # Fallback: use filename without extension
        stem = os.path.splitext(filename)[0]
        return stem.replace("_", " ").replace("-", " ").title()

    def _extract_email(self, text: str) -> str:
        """Extract first email address found in text."""
        match = self.email_pattern.search(text)
        return match.group(0) if match else "N/A"

    def _extract_phone(self, text: str) -> str:
        """Extract first phone number found in text."""
        match = self.phone_pattern.search(text)
        return match.group(0).strip() if match else "N/A"
