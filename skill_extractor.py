"""
skill_extractor.py
------------------
Identifies and normalizes technical skills from raw resume text.
Uses a curated skill database plus synonym / abbreviation mapping.
"""

import re
from rapidfuzz import fuzz


class SkillExtractor:
    """
    Extracts skills from resume text using:
      1. Exact keyword matching against the skill database.
      2. Synonym / abbreviation normalization.
      3. Fuzzy matching for near-matches.
    """

    # ------------------------------------------------------------------
    # Master skill database (canonical forms)
    # ------------------------------------------------------------------
    SKILL_DATABASE = [
        # Programming Languages
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "R", "Go", "Rust", "Swift", "Kotlin", "PHP", "Ruby", "Scala",
        "MATLAB", "Perl", "Shell", "Bash", "PowerShell", "Dart", "Lua",

        # Web / Frontend
        "HTML", "CSS", "React", "Angular", "Vue", "Next.js", "Nuxt",
        "Bootstrap", "Tailwind CSS", "jQuery", "Sass", "LESS",
        "Redux", "GraphQL", "REST API", "WebSocket",

        # Backend / Frameworks
        "Node.js", "Django", "Flask", "FastAPI", "Spring Boot",
        "Express.js", "Ruby on Rails", "ASP.NET", "Laravel",

        # Databases
        "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis",
        "Cassandra", "DynamoDB", "Oracle", "Firebase", "Elasticsearch",
        "MariaDB", "Neo4j", "CouchDB",

        # Data Science / ML / AI
        "Machine Learning", "Deep Learning", "Neural Networks",
        "Natural Language Processing", "Computer Vision",
        "Data Science", "Data Analysis", "Data Engineering",
        "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
        "XGBoost", "LightGBM", "Hugging Face", "OpenCV",
        "Reinforcement Learning", "Feature Engineering",
        "Statistical Analysis", "Time Series Analysis",

        # Cloud / DevOps
        "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes",
        "Terraform", "Ansible", "Jenkins", "GitHub Actions",
        "CI/CD", "Linux", "Unix", "Nginx", "Apache",

        # Version Control / Collaboration
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",

        # Big Data
        "Spark", "Hadoop", "Kafka", "Hive", "Pig", "Airflow",
        "Databricks", "Snowflake", "dbt",

        # Security
        "Cybersecurity", "Penetration Testing", "Ethical Hacking",
        "Network Security", "Cryptography", "OWASP",

        # Mobile
        "Android", "iOS", "React Native", "Flutter", "Xamarin",

        # Tools & Misc
        "Excel", "Power BI", "Tableau", "Looker", "SPSS",
        "Agile", "Scrum", "Kanban", "DevOps", "MLOps",
        "Object-Oriented Programming", "Functional Programming",
        "Microservices", "Serverless", "Unit Testing",
        "Selenium", "Pytest", "JUnit",
    ]

    # ------------------------------------------------------------------
    # Synonym / abbreviation map  →  canonical form
    # ------------------------------------------------------------------
    SYNONYMS = {
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "nlp": "Natural Language Processing",
        "cv": "Computer Vision",
        "ai": "Artificial Intelligence",
        "ds": "Data Science",
        "da": "Data Analysis",
        "de": "Data Engineering",
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "tf": "TensorFlow",
        "sk-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",
        "scikit learn": "Scikit-learn",
        "pytorch": "PyTorch",
        "torch": "PyTorch",
        "node": "Node.js",
        "nodejs": "Node.js",
        "react js": "React",
        "reactjs": "React",
        "vue js": "Vue",
        "vuejs": "Vue",
        "angular js": "Angular",
        "angularjs": "Angular",
        "next js": "Next.js",
        "nextjs": "Next.js",
        "postgres": "PostgreSQL",
        "mongo": "MongoDB",
        "elastic": "Elasticsearch",
        "k8s": "Kubernetes",
        "gcp": "Google Cloud",
        "aws lambda": "AWS",
        "amazon web services": "AWS",
        "microsoft azure": "Azure",
        "google cloud platform": "Google Cloud",
        "oop": "Object-Oriented Programming",
        "fp": "Functional Programming",
        "ci cd": "CI/CD",
        "cicd": "CI/CD",
        "ms excel": "Excel",
        "microsoft excel": "Excel",
        "power bi": "Power BI",
        "powerbi": "Power BI",
        "spring": "Spring Boot",
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "xgb": "XGBoost",
        "lgbm": "LightGBM",
        "hf": "Hugging Face",
        "transformers": "Hugging Face",
        "bert": "Hugging Face",
        "gpt": "Hugging Face",
    }

    def __init__(self, fuzzy_threshold: int = 80):
        """
        Args:
            fuzzy_threshold: Minimum fuzzy ratio (0-100) to accept a match.
        """
        self.fuzzy_threshold = fuzzy_threshold
        # Build lowercase lookup for fast exact matching
        self._db_lower = {s.lower(): s for s in self.SKILL_DATABASE}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> list:
        """
        Extract and return a deduplicated list of canonical skill names
        found in the given text.

        Args:
            text: Raw resume text.

        Returns:
            Sorted list of unique canonical skill strings.
        """
        text_lower = text.lower()
        found = set()

        # 1. Check synonyms first (they're often abbreviations)
        for alias, canonical in self.SYNONYMS.items():
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found.add(canonical)

        # 2. Exact match against skill database
        for skill_lower, canonical in self._db_lower.items():
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found.add(canonical)

        # 3. Fuzzy matching on individual words/tokens (catches typos)
        tokens = self._tokenize(text)
        for token in tokens:
            if len(token) < 3:
                continue
            for skill_lower, canonical in self._db_lower.items():
                if canonical in found:
                    continue
                score = fuzz.ratio(token, skill_lower)
                if score >= self.fuzzy_threshold:
                    found.add(canonical)

        return sorted(found)

    def normalize(self, skill: str) -> str:
        """
        Normalize a single skill string to its canonical form.

        Args:
            skill: Raw skill text (e.g. "ML", "pytorch").

        Returns:
            Canonical skill name or the original (title-cased) if not found.
        """
        key = skill.strip().lower()
        if key in self.SYNONYMS:
            return self.SYNONYMS[key]
        if key in self._db_lower:
            return self._db_lower[key]
        return skill.title()

    def normalize_list(self, skills: list) -> list:
        """Normalize a list of skill strings."""
        seen = set()
        result = []
        for s in skills:
            norm = self.normalize(s)
            if norm not in seen:
                seen.add(norm)
                result.append(norm)
        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> list:
        """Split text into lowercase tokens for fuzzy matching."""
        # Keep multi-word skill tokens (up to 3 words)
        tokens = set()
        words = re.findall(r'[a-zA-Z0-9\+\#\.]+', text.lower())

        for w in words:
            tokens.add(w)

        # Bigrams
        for i in range(len(words) - 1):
            tokens.add(f"{words[i]} {words[i+1]}")

        # Trigrams
        for i in range(len(words) - 2):
            tokens.add(f"{words[i]} {words[i+1]} {words[i+2]}")

        return list(tokens)
