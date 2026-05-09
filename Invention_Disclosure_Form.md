# INVENTION DISCLOSURE FORM

## 1. TITLE
**Adaptive Resume Intelligence Engine with Multimodal Biometric Authenticity and Zero-Knowledge Proof Verification**

## 2. INTERNAL INVENTOR(S)/ STUDENT(S)
*   **Name:** [Please enter your name here]
*   **Registration Number / Employee ID:** [Please enter your ID here]
*   **Department/School:** [Please enter your Department here]
*   **Contact Info:** [Please enter your Email/Phone here]

*(No external inventors)*

## 3. DESCRIPTION OF THE INVENTION
This invention is an enterprise-grade "Super App" for recruitment that fundamentally transforms how candidate resumes are parsed, verified, and scored. It replaces static keyword-matching Applicant Tracking Systems (ATS) with an interactive, multimodal cognitive engine that actively tests candidates, mathematically verifies their skills without exposing demographic data, and embeds live learning sandboxes to upskill rejected candidates.

### PROBLEM ADDRESSED BY THE INVENTION
1.  **AI-Generated Fraud:** Candidates use Generative AI to heavily optimize resumes, making it impossible for standard ATS software to determine if the candidate actually possesses the technical skills listed on paper.
2.  **Unconscious Hiring Bias:** Standard resume screening exposes a candidate's name, gender, and ethnicity, which inherently invites human bias into the selection process.
3.  **Lack of Actionable Candidate Feedback:** Traditional systems reject candidates without offering any targeted, technical pathway for them to acquire the exact skills they were missing.

### OBJECTIVE OF THE INVENTION
1.  To accurately detect fraudulent skill claims by forcing candidates into a live browser-based interview that measures cognitive load (Words-Per-Minute and hesitation pauses) against technical questions.
2.  To eliminate unconscious demographic bias in the hiring pipeline by cryptographically hashing verified skills into a "Zero-Knowledge Proof" token that employers evaluate before ever seeing the candidate's personal identity.
3.  To predict the obsolescence (career decay) of a candidate's specific technology stack using actuarial forecasting models over a 5-year timeline.

### C. STATE OF THE ART / RESEARCH GAP / NOVELTY
**Research Gap:** Existing solutions (like Workday or Taleo) rely strictly on static Natural Language Processing to extract keywords. They do not test human authenticity, nor do they natively integrate cryptographic blind hiring protocols into the parsing stage.
**Novelty:** 
*   **Multimodal Biometric & Cognitive Authenticity Engine:** This system transitions from static text to behavioral biometrics, analyzing *how* a candidate speaks about their skills in real-time.
*   **Reverse-Engineered Corporate DNA Matching:** It evaluates the semantic tone of the resume (e.g., highly analytical vs. disruptive startup) to match specific corporate cultures.
*   **Stealth Learning Sandbox Integration:** Upon detecting a missing skill (e.g., Python), the system dynamically injects a live interactive coding terminal (via iframe) directly into the candidate's dashboard for immediate learning.

### D. DETAILED DESCRIPTION
The system is architected as a web application utilizing a Python (Flask) backend and an HTML/JS Glassmorphism frontend. 
1.  **Ingestion:** The system parses uploaded PDF/DOCX files using SpaCy NLP, specifically targeting named entities, quantifiable business metrics (e.g., "improved efficiency by X%"), and technical keywords.
2.  **Processing:** A context-aware algorithm maps extracted skills against specific job role requirements, outputting an "Enterprise Impact Score".
3.  **Authentication:** The candidate engages with the "Biometric Interview". The Web Speech API captures audio transcriptions, while an internal algorithm calculates WPM and pause frequency to generate an "Authenticity Score". 
4.  **ZKP Generation:** The verified tech stack is passed through a SHA-256 cryptographic hash function to output a ZKP token. 
5.  **Interactive Assistant:** A local AI chatbot is provisioned with the full parsed payload, allowing the candidate to dynamically converse with the system about their specific skill gaps and strengths.

### E. RESULTS AND ADVANTAGES
*   **Advantages over Prior Art:** Unmatched fraud detection through live cognitive metrics; Complete elimination of initial screening bias via ZKP integration; Superior user experience for candidates via immediate upskilling pathways.
*   **Results:** The prototype successfully parses raw text into structured JSON, initiates functional live WebRTC transcripts, renders accurate career decay predictive charts, and provisions live external coding sandboxes seamlessly.

### F. EXPANSION
The architecture can easily be expanded to include:
*   **Multi-Agent Interview Panels:** Deploying concurrent AI agents (Technical Lead, HR Manager) to evaluate the candidate simultaneously.
*   **Live GitHub Repository Scraping:** Integrating the GitHub API to dynamically scan a candidate's commit history to mathematically prove programming language competency.

### G. WORKING PROTOTYPE / FORMULATION / DESIGN / COMPOSITION
**Yes, a working prototype is ready.** It is implemented as a local web application using Python 3.x, Flask, SpaCy `en_core_web_sm` model, Vanilla JavaScript, Chart.js, and WebRTC Speech Recognition.

### H. EXISTING DATA
No clinical data. Comparative data shows standard ATS systems rely on 100% static text evaluation, whereas this system relies on 60% text evaluation and 40% real-time cognitive evaluation.

## 4. USE AND DISCLOSURE
The invention is currently a prototype built for academic/class presentation and has not been publicly disclosed, commercialized, or published in any journals.

## 5. LINKS AND DATES FOR PUBLIC DISCLOSURE
N/A - Not publicly disclosed.

## 6. TERMS AND CONDITIONS OF MOU
N/A - Developed internally without external industry MOUs.

## 7. POTENTIAL CHANCES OF COMMERCIALIZATION
High. The Global HR Technology Market is valued at over $30 Billion. Enterprise clients are actively seeking solutions that integrate AI while simultaneously reducing systemic hiring bias.

## 8. LIST OF COMPANIES FOR COMMERCIALIZATION
*   Workday
*   Oracle (Taleo)
*   Greenhouse Software
*   Lever
*   LinkedIn (Microsoft)
*   Indeed

## 9. BASIC PATENT USED (ROYALTY)
None identified. Built utilizing open-source libraries (Python, Flask, SpaCy, Chart.js).

## 10. FILING OPTIONS
Complete Filing (Recommended due to the presence of a fully functional working prototype and novel algorithmic pathways).

## 11. KEYWORDS
Applicant Tracking System (ATS), Biometric Authentication, Zero-Knowledge Proof, Blind Hiring, Resume Parsing, Cognitive Load Tracking, HR Technology, Upskilling Sandbox.
