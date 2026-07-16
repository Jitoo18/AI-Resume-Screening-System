"""
matcher.py
----------
Compares candidate skills against required job skills and computes
match scores. Produces a ranked list of candidates.
"""

from rapidfuzz import fuzz


class Matcher:
    """
    Scores and ranks resumes based on skill overlap with job requirements.

    Scoring formula:
        match_pct = (# matched required skills / # required skills) * 100

    A candidate skill "matches" a required skill when the fuzzy ratio
    between their lowercase forms meets or exceeds `fuzzy_threshold`.
    """

    def __init__(self, fuzzy_threshold: int = 75):
        """
        Args:
            fuzzy_threshold: Minimum fuzz.ratio score to count as a match.
        """
        self.fuzzy_threshold = fuzzy_threshold

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def match(self, candidate_skills: list, required_skills: list) -> dict:
        """
        Compute which required skills are matched / missing for a candidate.

        Args:
            candidate_skills: Skills extracted from the resume.
            required_skills:  Skills entered by the recruiter.

        Returns:
            dict with keys:
                matched_skills  – list of required skills found
                missing_skills  – list of required skills not found
                match_pct       – float 0-100
        """
        if not required_skills:
            return {"matched_skills": [], "missing_skills": [], "match_pct": 0.0}

        matched = []
        missing = []

        for req in required_skills:
            if self._is_matched(req, candidate_skills):
                matched.append(req)
            else:
                missing.append(req)

        match_pct = (len(matched) / len(required_skills)) * 100
        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_pct": round(match_pct, 2),
        }

    def rank(self, resumes: list, required_skills: list, top_k: int = None) -> list:
        """
        Score and rank all resumes, optionally returning only top K.

        Args:
            resumes:         List of dicts from ResumeParser + SkillExtractor.
                             Each dict must contain a "skills" key (list of str).
            required_skills: Skills entered by the recruiter (list of str).
            top_k:           Return only the top K candidates. None = all.

        Returns:
            Ranked list of result dicts (descending match_pct).
        """
        results = []

        for resume in resumes:
            candidate_skills = resume.get("skills", [])
            match_data = self.match(candidate_skills, required_skills)

            results.append({
                "filename":       resume.get("filename", "Unknown"),
                "name":           resume.get("name", "Unknown"),
                "email":          resume.get("email", "N/A"),
                "phone":          resume.get("phone", "N/A"),
                "skills":         candidate_skills,
                "matched_skills": match_data["matched_skills"],
                "missing_skills": match_data["missing_skills"],
                "match_pct":      match_data["match_pct"],
                "error":          resume.get("error"),
            })

        # Sort descending by match percentage
        results.sort(key=lambda r: r["match_pct"], reverse=True)

        if top_k is not None and top_k > 0:
            results = results[:top_k]

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _is_matched(self, required_skill: str, candidate_skills: list) -> bool:
        """
        Return True if `required_skill` fuzzy-matches any skill in
        `candidate_skills` above the threshold.
        """
        req_lower = required_skill.lower().strip()

        for cs in candidate_skills:
            cs_lower = cs.lower().strip()

            # Exact match
            if req_lower == cs_lower:
                return True

            # One is a substring of the other
            if req_lower in cs_lower or cs_lower in req_lower:
                return True

            # Fuzzy ratio
            if fuzz.ratio(req_lower, cs_lower) >= self.fuzzy_threshold:
                return True

            # Partial ratio (handles abbreviations within longer text)
            if fuzz.partial_ratio(req_lower, cs_lower) >= self.fuzzy_threshold:
                return True

        return False
