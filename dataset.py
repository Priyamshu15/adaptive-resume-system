# dataset.py

JOB_ROLES = {
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "sql", "statistics", "deep learning", "tensorflow", "nlp", "data visualization", "scikit-learn"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "git", "api", "typescript", "mongodb", "express"],
    "AI Engineer": ["python", "pytorch", "tensorflow", "neural networks", "machine learning", "computer vision", "nlp", "c++", "cuda", "model deployment"],
    "Data Analyst": ["sql", "excel", "tableau", "power bi", "python", "statistics", "data visualization", "dashboarding", "r", "pandas"],
    "Cloud Engineer": ["aws", "azure", "docker", "kubernetes", "linux", "terraform", "ci/cd", "networking", "security", "python"],
    "DevOps Engineer": ["linux", "bash", "docker", "kubernetes", "jenkins", "aws", "terraform", "ansible", "ci/cd", "python"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue", "angular", "typescript", "tailwind", "figma", "git"],
    "Backend Developer": ["python", "java", "node.js", "c#", "go", "sql", "mongodb", "redis", "docker", "api"],
    "Full Stack Developer": ["javascript", "react", "node.js", "python", "sql", "mongodb", "aws", "docker", "git", "typescript"],
    "Machine Learning Engineer": ["python", "pytorch", "tensorflow", "scikit-learn", "sql", "docker", "kubernetes", "aws", "nlp", "computer vision"],
    "Product Manager": ["agile", "scrum", "jira", "confluence", "sql", "python", "data analysis", "a/b testing", "roadmap", "strategy"],
    "UI/UX Designer": ["figma", "adobe xd", "sketch", "wireframing", "prototyping", "user research", "html", "css", "design systems", "usability testing"],
    "Cybersecurity Analyst": ["linux", "networking", "wireshark", "python", "siem", "firewalls", "penetration testing", "cryptography", "owasp", "incident response"],
    "Blockchain Developer": ["solidity", "ethereum", "smart contracts", "web3.js", "javascript", "go", "rust", "cryptography", "bitcoin", "dapps"],
    "Mobile App Developer": ["swift", "kotlin", "java", "react native", "flutter", "dart", "ios", "android", "git", "api"]
}

LEARNING_ROADMAPS = {
    "python": {"beginner": "Learn basics (variables, loops).", "intermediate": "Understand OOP.", "advanced": "Master async and ML pipelines."},
    "machine learning": {"beginner": "Linear Regression.", "intermediate": "Scikit-Learn.", "advanced": "Deep Learning architectures."},
    "pandas": {"beginner": "Basic DataFrames.", "intermediate": "GroupBy and merges.", "advanced": "Window functions and optimization."},
    "numpy": {"beginner": "Numpy arrays and math.", "intermediate": "Matrix multiplication.", "advanced": "Broadcasting and vectorization."},
    "sql": {"beginner": "SELECT and JOINs.", "intermediate": "Subqueries.", "advanced": "Window Functions and indexing."},
    "react": {"beginner": "JSX and props.", "intermediate": "Hooks (useState, useEffect).", "advanced": "Redux and SSR (Next.js)."},
    "node.js": {"beginner": "Event Loop.", "intermediate": "Express.js routing.", "advanced": "Microservices and streams."},
    "aws": {"beginner": "EC2 and S3.", "intermediate": "VPC and Lambda.", "advanced": "Terraform / Infrastructure as Code."}
}
DEFAULT_ROADMAP = {"beginner": "Read official docs.", "intermediate": "Build small projects.", "advanced": "Study architecture patterns."}

TRENDING_SKILLS = [
    {"skill": "Generative AI", "growth": "+120%"},
    {"skill": "Python", "growth": "+45%"},
    {"skill": "React", "growth": "+30%"},
    {"skill": "Cloud Security", "growth": "+85%"},
    {"skill": "Kubernetes", "growth": "+60%"},
    {"skill": "Data Engineering", "growth": "+75%"}
]

# PREMIUM CURATED COURSES
COURSE_LINKS = {
    "python": "https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg",
    "react": "https://www.youtube.com/playlist?list=PLC3y8-r4AaVN8z29N64u5yA8q8wBv5gZ",
    "node.js": "https://www.youtube.com/playlist?list=PLu0W_9lII9agx66oZnT6IyhcMIbUMNMdt",
    "machine learning": "https://nptel.ac.in/courses/106106139",
    "sql": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
    "aws": "https://aws.amazon.com/training/digital/",
    "deep learning": "https://nptel.ac.in/courses/106106184",
    "pandas": "https://www.youtube.com/watch?v=vmEHCJofslg"
}

# INTERACTIVE SANDBOX ENVIRONMENTS
SANDBOX_LINKS = {
    "python": "https://trinket.io/embed/python3",
    "react": "https://codesandbox.io/embed/new?template=create-react-app",
    "node.js": "https://codesandbox.io/embed/node",
    "html": "https://codesandbox.io/embed/vanilla",
    "css": "https://codesandbox.io/embed/vanilla",
    "javascript": "https://codesandbox.io/embed/vanilla",
    "sql": "https://sqliteonline.com/",
    "mongodb": "https://mongoplayground.net/"
}

SALARY_IMPACT = {"react": 8000, "node.js": 7500, "python": 10000, "machine learning": 15000, "sql": 5000, "aws": 12000, "docker": 8500, "kubernetes": 14000}

# SPECIFIC SKILL QUESTIONS
INTERVIEW_QUESTIONS = {
    "react": [
        "Explain Virtual DOM.", "What are React Hooks?", "Context API vs Redux?", 
        "Controlled vs Uncontrolled components?", "What is React Fiber?"
    ],
    "python": [
        "List vs Tuple?", "How do decorators work?", "Explain the GIL.", 
        "What are generators?", "Deepcopy vs shallow copy?"
    ],
    "machine learning": [
        "Bias-variance tradeoff?", "L1 vs L2 regularization?", "Decision Trees?", 
        "Cross-validation?", "Vanishing gradient problem?"
    ],
    "pandas": [
        "How do you handle missing data in Pandas?", "Explain loc vs iloc.", 
        "How does a pandas merge differ from a join?", "What is GroupBy?", "How to optimize memory usage?"
    ],
    "sql": [
        "Inner vs Left Join?", "What is an index?", "Window functions?", 
        "Clustered vs Non-clustered index?", "How to prevent SQL injection?"
    ]
}

# ROLE SPECIFIC FALLBACK QUESTIONS
ROLE_INTERVIEW_QUESTIONS = {
    "Data Scientist": [
        "Walk me through a time you cleaned a messy dataset.",
        "How do you deploy a machine learning model to production?",
        "Explain p-value to a non-technical stakeholder.",
        "What evaluation metrics do you use for imbalanced classes?",
        "Describe a time your model didn't perform as expected."
    ],
    "AI Engineer": [
        "How do you optimize a neural network for inference speed?",
        "Explain transformer architectures.",
        "What is the difference between PyTorch and TensorFlow graphs?",
        "How do you handle GPU memory out-of-memory errors?",
        "Describe your experience with LLM fine-tuning."
    ],
    "Web Developer": [
        "Explain CORS.", "How do you optimize website load time?",
        "Describe RESTful API principles.", "What is Server-Side Rendering?",
        "How do you handle state in a complex frontend app?"
    ]
}

# GENERIC BEHAVIORAL/TECH QUESTIONS
GENERIC_INTERVIEW_QUESTIONS = [
    "Describe a challenging technical problem you solved recently.",
    "Tell me about a time you disagreed with a senior engineer on architecture.",
    "How do you keep up with new technologies?",
    "Describe a project that failed and what you learned.",
    "How do you balance technical debt with shipping features quickly?",
    "What is your debugging process for a critical production bug?",
    "Tell me about a time you had to learn a new framework in a weekend."
]

SKILL_DECAY_RATES = {
    "jquery": {"half_life_years": 1.5, "decay_rate": 0.3},
    "react": {"half_life_years": 4.5, "decay_rate": 0.1},
    "python": {"half_life_years": 8.0, "decay_rate": 0.05},
    "sql": {"half_life_years": 15.0, "decay_rate": 0.02},
    "machine learning": {"half_life_years": 6.0, "decay_rate": 0.08},
    "aws": {"half_life_years": 3.5, "decay_rate": 0.15}
}

CORPORATE_DNA = {
    "Google": {"keywords": ["scale", "distributed", "algorithms", "performance", "impact", "data-driven"], "tone": "Academic & High Scale"},
    "Stripe": {"keywords": ["developer experience", "api", "latency", "robust", "elegant", "fintech"], "tone": "Developer-First & Precise"},
    "Netflix": {"keywords": ["freedom", "responsibility", "chaos engineering", "microservices", "streaming"], "tone": "Autonomous & Resilient"}
}
