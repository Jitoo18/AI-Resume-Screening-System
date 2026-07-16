"""
generate_sample_resumes.py
--------------------------
Generates sample DOCX resumes for testing the screening system.
Run this script once before testing:  python generate_sample_resumes.py
"""

import os
import docx
from docx.shared import Pt


SAMPLE_RESUMES = [
    {
        "filename": "Alice_Chen_DataScientist.docx",
        "content": """Alice Chen
alice.chen@email.com | +1-555-201-3344

SUMMARY
Experienced Data Scientist with 5 years in machine learning, deep learning, and NLP.
Passionate about turning data into actionable insights.

SKILLS
Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn,
Pandas, NumPy, SQL, PostgreSQL, Data Analysis, Data Science,
Natural Language Processing, Computer Vision, Matplotlib, Seaborn,
Docker, Git, AWS, Jupyter Notebook, Statistical Analysis

EXPERIENCE
Senior Data Scientist | TechCorp Inc.  (2021 – Present)
- Built ML models for customer churn prediction (accuracy 92%)
- Deployed NLP pipeline for sentiment analysis using BERT / Hugging Face
- Reduced ETL processing time by 40% using Spark and Airflow

Data Analyst | DataFlow Ltd.  (2019 – 2021)
- Analysed large datasets with Pandas and SQL; created Power BI dashboards

EDUCATION
M.Sc. Computer Science – Stanford University (2019)
B.Sc. Mathematics – UC Berkeley (2017)
""",
    },
    {
        "filename": "Bob_Martinez_WebDev.docx",
        "content": """Bob Martinez
bob.martinez@devmail.com | +1-555-302-4455

OBJECTIVE
Full-stack web developer with 4 years building scalable web applications.

TECHNICAL SKILLS
JavaScript, TypeScript, React, Next.js, Node.js, Express.js,
HTML, CSS, Tailwind CSS, MongoDB, PostgreSQL, REST API, GraphQL,
Docker, Git, GitHub, CI/CD, Redux, Jest, Selenium

EXPERIENCE
Full-Stack Developer | WebSolutions Agency  (2020 – Present)
- Developed e-commerce platform (React + Node.js) serving 100k+ users
- Integrated GraphQL API reducing data over-fetching by 35%
- Automated deployments with GitHub Actions (CI/CD)

Junior Developer | StartupHub  (2019 – 2020)
- Built RESTful APIs with Express.js and MongoDB

EDUCATION
B.Sc. Information Technology – Arizona State University (2019)
""",
    },
    {
        "filename": "Carol_Singh_MachineLearning.docx",
        "content": """Carol Singh
carol.singh@aiml.com | +1-555-403-5566

PROFILE
ML Engineer specializing in model development, deployment, and MLOps.

SKILLS
Python, Machine Learning, Deep Learning, TensorFlow, Keras, PyTorch,
Scikit-learn, XGBoost, LightGBM, SQL, Data Science, Feature Engineering,
MLOps, Docker, Kubernetes, AWS, GCP, Airflow, Git, CI/CD,
Pandas, NumPy, Statistical Analysis, Time Series Analysis

WORK HISTORY
ML Engineer | AI Ventures  (2021 – Present)
- Trained and productionized image classification model (PyTorch, 97% accuracy)
- Built end-to-end ML pipeline using Airflow + AWS SageMaker
- Implemented A/B testing framework reducing model deployment risk

Research Assistant | University AI Lab  (2019 – 2021)
- Developed NLP models for text summarization using Hugging Face Transformers

EDUCATION
M.Sc. Artificial Intelligence – Carnegie Mellon University (2021)
""",
    },
    {
        "filename": "David_Kim_Backend.docx",
        "content": """David Kim
david.kim@backend.io | +1-555-504-6677

SUMMARY
Backend engineer with strong Java ecosystem experience and microservices expertise.

SKILLS
Java, Spring Boot, Microservices, SQL, MySQL, PostgreSQL, Redis,
Docker, Kubernetes, REST API, Git, Maven, JUnit, Kafka,
AWS, Linux, CI/CD, Agile, Scrum, Object-Oriented Programming

EXPERIENCE
Backend Software Engineer | Enterprise Systems Co.  (2020 – Present)
- Designed microservices architecture processing 1M+ daily transactions
- Optimised MySQL queries reducing latency by 50%
- Containerised services with Docker and orchestrated via Kubernetes

Junior Java Developer | CodeFactory  (2018 – 2020)
- Developed Spring Boot REST APIs for internal tooling

EDUCATION
B.Sc. Software Engineering – Georgia Institute of Technology (2018)
""",
    },
    {
        "filename": "Eva_Patel_DataAnalyst.docx",
        "content": """Eva Patel
eva.patel@analytics.com | +1-555-605-7788

SUMMARY
Data analyst with strong SQL, visualization, and reporting skills.

CORE SKILLS
Python, SQL, MySQL, Data Analysis, Excel, Power BI, Tableau,
Pandas, Matplotlib, Statistical Analysis, Data Science, Git,
R, SPSS, Google Cloud

PROFESSIONAL EXPERIENCE
Data Analyst | RetailInsights Inc.  (2020 – Present)
- Created interactive Power BI dashboards used by C-suite
- Wrote complex SQL queries for sales trend analysis
- Automated monthly reporting with Python (Pandas + Matplotlib)

Junior Analyst | Finance Corp.  (2019 – 2020)
- Maintained Excel-based financial models and KPI trackers

EDUCATION
B.Sc. Statistics – University of Michigan (2019)
""",
    },
    {
        "filename": "Frank_Nguyen_DevOps.docx",
        "content": """Frank Nguyen
frank.nguyen@devops.net | +1-555-706-8899

SUMMARY
DevOps engineer passionate about automation, cloud infrastructure, and reliability.

SKILLS
AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Ansible,
Jenkins, GitHub Actions, CI/CD, Linux, Bash, Python, Git,
Nginx, Monitoring, Prometheus, Grafana, Kafka, Microservices

EXPERIENCE
DevOps Engineer | CloudFirst Ltd.  (2021 – Present)
- Managed AWS infrastructure for 50+ microservices using Terraform
- Reduced deployment frequency from monthly to daily via CI/CD pipelines
- Implemented Kubernetes autoscaling cutting cloud costs 30%

Systems Administrator | HostPro  (2019 – 2021)
- Maintained Linux servers and managed Nginx load balancers

EDUCATION
B.Sc. Computer Networks – University of Texas at Austin (2019)
""",
    },
    {
        "filename": "Grace_Lee_Junior.docx",
        "content": """Grace Lee
grace.lee@student.edu | +1-555-807-9900

OBJECTIVE
Recent CS graduate seeking entry-level software development role.

SKILLS
Python, Java, SQL, HTML, CSS, JavaScript, Git, Excel, Data Analysis

PROJECTS
Student Grade Predictor (Python, Scikit-learn, Pandas)
- Built a regression model predicting final grades from attendance data

Personal Portfolio Website (HTML, CSS, JavaScript)
- Designed and deployed a responsive website

EDUCATION
B.Sc. Computer Science – University of California, San Diego (2024)
GPA: 3.7 / 4.0

CERTIFICATIONS
Google Data Analytics Certificate (2024)
""",
    },
    {
        "filename": "Henry_Brown_Cybersecurity.docx",
        "content": """Henry Brown
henry.brown@secops.com | +1-555-908-0011

PROFILE
Cybersecurity specialist with 6 years in penetration testing and network security.

SKILLS
Cybersecurity, Penetration Testing, Ethical Hacking, Network Security,
Python, Bash, Linux, Cryptography, OWASP, Docker, Git, SQL,
Firewall Configuration, Vulnerability Assessment, Kali Linux, Wireshark

EXPERIENCE
Senior Security Engineer | SecureNet Corp.  (2020 – Present)
- Led red team exercises identifying 120+ vulnerabilities across client systems
- Developed custom Python scripts for automated OWASP scanning
- Hardened cloud infrastructure on AWS reducing attack surface

Penetration Tester | CyberGuard Agency  (2018 – 2020)
- Performed web application and network penetration tests

EDUCATION
B.Sc. Information Security – NYU Tandon School of Engineering (2018)
CISSP Certified  |  CEH Certified
""",
    },
]


def generate():
    out_dir = os.path.join(os.path.dirname(__file__), "sample_resumes")
    os.makedirs(out_dir, exist_ok=True)

    for resume in SAMPLE_RESUMES:
        filepath = os.path.join(out_dir, resume["filename"])
        doc = docx.Document()

        # Style the document minimally
        style = doc.styles["Normal"]
        style.font.name = "Calibri"
        style.font.size = Pt(11)

        for line in resume["content"].strip().split("\n"):
            para = doc.add_paragraph(line)
            para.paragraph_format.space_after = Pt(2)

        doc.save(filepath)
        print(f"  ✅  Created: {resume['filename']}")

    print(f"\n✨  {len(SAMPLE_RESUMES)} sample resumes saved to: {out_dir}/")


if __name__ == "__main__":
    print("Generating sample resumes…\n")
    generate()
