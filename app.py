import os
import re
import hashlib
from flask import Flask, request, jsonify, render_template
import spacy
import pdfplumber
import docx
from werkzeug.utils import secure_filename
from dataset import JOB_ROLES, LEARNING_ROADMAPS, DEFAULT_ROADMAP, TRENDING_SKILLS, COURSE_LINKS, SALARY_IMPACT, INTERVIEW_QUESTIONS, ROLE_INTERVIEW_QUESTIONS, GENERIC_INTERVIEW_QUESTIONS, SKILL_DECAY_RATES, CORPORATE_DNA, SANDBOX_LINKS
import random
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit
app.secret_key = 'supersecretkey'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    nlp = spacy.load("en_core_web_sm")
    USE_SPACY = True
except OSError:
    USE_SPACY = False

def extract_text_from_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: text += page_text + "\n"
    except Exception as e: print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs: text += para.text + "\n"
    except Exception as e: print(f"Error reading DOCX: {e}")
    return text

def extract_personal_info(text):
    info = {"name": "Candidate", "email": "Not Found", "phone": "Not Found"}
    
    # Extract Email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match: info["email"] = email_match.group()
        
    # Extract Phone
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match: info["phone"] = phone_match.group()
        
    # Extract Name (Heuristic: First proper noun in the first 500 chars)
    if USE_SPACY:
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Ensure it's not a single generic word
                if len(ent.text.split()) >= 2:
                    info["name"] = ent.text.strip().title()
                    break
    return info

def extract_skills(text, target_role_skills):
    text_lower = text.lower()
    # Replace weird characters with space so "numpy,pandas" becomes "numpy pandas"
    text_clean = re.sub(r'[^a-z0-9\+\#\.]', ' ', text_lower)
    
    extracted = []
    for skill in target_role_skills:
        skill_lower = skill.lower()
        
        # For very short or specific skills, use word boundaries to avoid false positives (e.g., 'c' in 'machine')
        if skill_lower in ['c', 'r', 'c++', 'aws', 'sql', 'git', 'api', 'css']:
            if re.search(rf"\b{re.escape(skill_lower)}\b", text_lower):
                extracted.append(skill)
        else:
            # For longer skills (e.g. pandas, numpy), use direct substring check on cleaned text
            skill_clean = re.sub(r'[^a-z0-9\+\#\.]', ' ', skill_lower)
            if skill_clean in text_clean:
                extracted.append(skill)
                
    return list(set(extracted))

def analyze_impact_metrics(text):
    raw_lines = text.split('\n')
    lines = []
    curr = ""
    for r in raw_lines:
        r = r.strip()
        if not r: continue
        
        # Detect bullet character
        has_bullet_char = re.match(r'^(•||⁃||·|\*|-)\s*', r)
        
        if has_bullet_char or (not curr):
            if curr: lines.append(curr)
            curr = re.sub(r'^(•||⁃||·|\*|-)\s*', '', r)
        else:
            # If no bullet char, but starts with Capital and previous line ended with period/colon, it might be a new sentence.
            if re.match(r'^[A-Z]', r) and (curr.endswith('.') or curr.endswith(':')):
                lines.append(curr)
                curr = r
            else:
                # Otherwise it's a continuation of the previous line
                curr += " " + r
                
    if curr: lines.append(curr)

    strong_bullets, weak_bullets = [], []
    
    ignore_keywords = ('languages', 'frameworks', 'tools', 'platforms', 'soft skills', 'skills', 'technologies', 'education', 'certifications', 'hobbies', 'interests', 'links', 'profile', 'summary', 'github', 'linkedin', 'email', 'experience', 'work history', 'projects')
    
    for s in lines:
        clean_s = s.strip()
        clean_s_lower = clean_s.lower()
        
        if len(clean_s) < 30: continue
        if any(clean_s_lower.startswith(kw) for kw in ignore_keywords): continue
        if clean_s.count(',') > 3 and not re.search(r'\d', clean_s): continue
            
        if USE_SPACY:
            doc = nlp(clean_s[:150]) 
            has_verb = any(token.pos_ in ["VERB", "AUX"] for token in doc)
            if not has_verb: continue

        has_metric = False
        # Fast Regex check for common metrics
        if re.search(r'(\d+%|\$\d+|\d+x|\d+[kmb]\b)', clean_s_lower):
            has_metric = True
        else:
            numbers = re.findall(r'\b\d+\b', clean_s)
            non_year_numbers = [n for n in numbers if not (len(n) == 4 and (n.startswith('19') or n.startswith('20')))]
            if len(non_year_numbers) > 0:
                has_metric = True
                
        # Advanced Spacy NLP check for written metrics (e.g. "five", "millions", "twenty percent")
        if not has_metric and USE_SPACY:
            doc_full = nlp(clean_s)
            for ent in doc_full.ents:
                if ent.label_ in ["CARDINAL", "PERCENT", "MONEY", "QUANTITY"]:
                    text_val = ent.text.strip()
                    if text_val.isdigit() and len(text_val) == 4 and (text_val.startswith('19') or text_val.startswith('20')):
                        continue # Ignore years
                    has_metric = True
                    break
                
        if has_metric:
            if len(strong_bullets) < 4: strong_bullets.append(clean_s)
        else:
            if len(weak_bullets) < 4: weak_bullets.append(clean_s)
            
    total = len(strong_bullets) + len(weak_bullets)
    impact_score = int((len(strong_bullets) / total) * 100) if total > 0 else 0
            
    return {"strong": strong_bullets, "weak": weak_bullets, "score": impact_score}

@app.route('/')
def index():
    return render_template('index.html', roles=list(JOB_ROLES.keys()), companies=list(CORPORATE_DNA.keys()))

@app.route('/api/trending', methods=['GET'])
def get_trending():
    return jsonify({"trending": TRENDING_SKILLS})

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files: return jsonify({"error": "No file part"}), 400
    file = request.files['resume']
    role = request.form.get('role')
    
    if file.filename == '': return jsonify({"error": "No selected file"}), 400
    if not role or role not in JOB_ROLES: return jsonify({"error": "Invalid role"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext not in ['pdf', 'docx']: return jsonify({"error": "Only PDF and DOCX supported."}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        extracted_text = extract_text_from_pdf(filepath) if ext == 'pdf' else extract_text_from_docx(filepath)
        try: os.remove(filepath)
        except: pass
            
        if not extracted_text.strip(): return jsonify({"error": "Could not extract text."}), 400
            
        required_skills = JOB_ROLES[role]
        found_skills = extract_skills(extracted_text, required_skills)
        missing_skills = list(set(required_skills) - set(found_skills))
        
        total_required = len(required_skills)
        match_percentage = int((len(found_skills) / total_required) * 100) if total_required > 0 else 0
        
        roadmap = {}
        total_salary_impact = 0
        for skill in missing_skills:
            rm = LEARNING_ROADMAPS.get(skill, DEFAULT_ROADMAP).copy()
            rm['course_link'] = COURSE_LINKS.get(skill, f"https://www.youtube.com/results?search_query={skill}+tutorial")
            rm['sandbox_link'] = SANDBOX_LINKS.get(skill, "https://codesandbox.io/embed/vanilla")
            roadmap[skill] = rm
            total_salary_impact += SALARY_IMPACT.get(skill, 2000)
            
        impact_analysis = analyze_impact_metrics(extracted_text)
        personal_info = extract_personal_info(extracted_text)
            
        return jsonify({
            "status": "success", "role": role, "match_percentage": match_percentage,
            "found_skills": found_skills, "missing_skills": missing_skills,
            "required_skills": required_skills,
            "roadmap": roadmap, "raw_text": extracted_text, 
            "impact_metrics": impact_analysis, "salary_impact": total_salary_impact,
            "candidate_profile": personal_info
        })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Context-Aware Chatbot API."""
    data = request.json
    message = data.get("message", "").lower()
    
    # Simulate LLM latency
    time.sleep(0.8)
    
    # If no resume has been uploaded yet, the frontend won't send candidate_profile
    if "candidate_profile" not in data and "raw_text" not in data:
        return jsonify({"reply": "I am the Enterprise AI Coach. Please upload your resume first so I can perform a deep algorithmic analysis on your profile!"})

    raw_text = data.get("raw_text", "").lower()
    missing_skills = data.get("missing_skills", [])
    found_skills = data.get("found_skills", [])
    candidate_profile = data.get("candidate_profile", {})
    impact_metrics = data.get("impact_metrics", {})
    
    if "name" in message or "who am i" in message or "candidate" in message:
        name = candidate_profile.get("name", "Candidate")
        email = candidate_profile.get("email", "")
        reply = f"Based on the parsed resume, your name is **{name}**. I also found your contact email: {email}." if email and email != "Not Found" else f"Your name is extracted as **{name}**."
        
    elif "strong" in message or "strength" in message or "good" in message or "achievements" in message:
        strong_pts = impact_metrics.get("strong", [])
        if strong_pts:
            summary = "<br>- ".join(strong_pts[:2])
            reply = f"Your resume shows strong quantified impact, such as:<br>- {summary}<br><br>You've done well adding metrics here!"
        elif found_skills:
            reply = f"While I didn't find many quantifiable metrics, your hard skills like **{', '.join(found_skills[:3])}** are excellent strengths for this role."
        else:
            reply = "I'm having trouble finding specific strengths. Please add more quantifiable metrics to your experience section."
            
    elif "skills" in message or "what do i know" in message:
        if found_skills:
            reply = f"I've verified the following hard skills from your resume: **{', '.join(found_skills)}**. These align perfectly with the target role."
        else:
            reply = "I haven't been able to verify any required technical skills. Ensure you are using the exact keywords requested in the job description."

    elif "weak" in message or "lacking" in message or "improve" in message or "missing" in message or "need metrics" in message:
        if missing_skills:
            reply = f"You are currently lacking these critical skills for the role: **{', '.join(missing_skills)}**. I highly recommend launching the Stealth Learning Sandbox from your roadmap to acquire these skills immediately."
        else:
            weak_pts = impact_metrics.get("weak", [])
            if weak_pts:
                reply = "You have the right skills, but your bullet points lack numbers! Change generic phrases to include quantifiable metrics (e.g., 'improved performance by 25%')."
            else:
                reply = "Your profile is incredibly strong. Just focus on your behavioral interview prep!"
                
    elif "score" in message or "ats" in message:
        score = impact_metrics.get("score", 0)
        reply = f"Your quantifiable impact score is **{score}%**. The higher this is, the better your chances of passing Enterprise ATS filters."
        
    elif "salary" in message or "worth" in message or "money" in message:
        reply = "My predictive models indicate that closing your current skill gaps can significantly alter your compensation trajectory. For instance, mastering Enterprise Cloud Architecture alone correlates with a 15-20% bump in base salary within modern tech hubs."
        
    elif any(skill in message for skill in missing_skills):
        skill = next((s for s in missing_skills if s in message), "that skill")
        reply = f"Excellent question regarding {skill}. Our data shows that candidates who demonstrate proficiency in {skill} are 3x more likely to clear the initial technical screen. You can use the Sandbox embedded in your dashboard to practice this!"
        
    elif any(skill in message for skill in found_skills):
        skill = next((s for s in found_skills if s in message), "that skill")
        reply = f"I see you already have experience with **{skill}**. Make sure you prepare for deep-dive technical questions on this during the Biometric Interview!"
        
    else:
        responses = [
            "That's an insightful query. Based on your target DNA match, prioritizing your missing skills and practicing your delivery in the Biometric Simulator will yield the highest ROI.",
            "As your Enterprise AI Coach, I suggest re-evaluating the 'Role Alignment' section of your report. Strong bullet points are the foundation of passing initial heuristic filters.",
            "Did you know? Modifying your phrasing to match the exact 'Corporate Tone' (e.g., highly analytical vs. developer-first) can improve your callback probability by up to 34%."
        ]
        reply = random.choice(responses)
        
    return jsonify({"reply": reply})

@app.route('/api/interview', methods=['POST'])
def get_interview_questions():
    """Returns random mock interview questions avoiding repeats. Uses Role-based and Generic fallbacks."""
    data = request.json
    skills = data.get("skills", [])
    role = data.get("role", "")
    asked_questions = data.get("asked_questions", [])
    
    questions = []
    
    # 1. Try to find specific skill questions
    for skill in skills:
        if skill in INTERVIEW_QUESTIONS:
            available_qs = [q for q in INTERVIEW_QUESTIONS[skill] if q not in asked_questions]
            if available_qs:
                questions.append({"skill": skill, "question": random.choice(available_qs)})
                
    # 2. If we need more questions, pull from Role Specific Bank
    if len(questions) < 3 and role in ROLE_INTERVIEW_QUESTIONS:
        available_role_qs = [q for q in ROLE_INTERVIEW_QUESTIONS[role] if q not in asked_questions]
        if available_role_qs:
            questions.append({"skill": f"{role} Domain", "question": random.choice(available_role_qs)})
            
    # 3. If we STILL need more, pull from Generic Bank
    if len(questions) < 3:
        available_gen_qs = [q for q in GENERIC_INTERVIEW_QUESTIONS if q not in asked_questions]
        if available_gen_qs:
            questions.append({"skill": "Behavioral", "question": random.choice(available_gen_qs)})
        else:
            questions.append({"skill": "Fallback", "question": "Are there any other technical achievements you'd like to share?"})
            
    random.shuffle(questions)
    # Return just one question at a time for the biometric interviewer
    return jsonify({"questions": questions[:1]})

@app.route('/api/decay-forecast', methods=['POST'])
def get_decay_forecast():
    """Predictive Career Decay Forecast"""
    data = request.json
    found_skills = data.get("found_skills", [])
    forecast_data = {"years": [0, 1, 2, 3, 4, 5], "value": []}
    
    total_decay = 0
    count = 0
    for skill in found_skills:
        if skill in SKILL_DECAY_RATES:
            total_decay += SKILL_DECAY_RATES[skill]["decay_rate"]
            count += 1
            
    avg_decay = total_decay / count if count > 0 else 0.10 
    current_value = 100
    for year in forecast_data["years"]:
        forecast_data["value"].append(round(current_value, 2))
        current_value = current_value * (1 - avg_decay)
        
    return jsonify({
        "forecast": forecast_data,
        "message": f"Your current skill stack is decaying at approximately {avg_decay*100:.1f}% per year."
    })

@app.route('/api/corporate-dna', methods=['POST'])
def match_corporate_dna():
    """Reverse-Engineered Corporate DNA Matching"""
    data = request.json
    company = data.get("company", "")
    raw_text = data.get("raw_text", "").lower()
    
    if company not in CORPORATE_DNA: return jsonify({"error": "Company not found"}), 400
        
    dna = CORPORATE_DNA[company]
    matches = sum(1 for keyword in dna["keywords"] if keyword in raw_text)
    match_score = int((matches / len(dna["keywords"])) * 100) if dna["keywords"] else 0
    
    return jsonify({
        "company": company, "match_score": match_score, "tone": dna["tone"],
        "feedback": f"Your resume is {match_score}% aligned with {company}'s DNA. They prefer a {dna['tone']} tone. Try incorporating keywords like: {', '.join(dna['keywords'][:3])}."
    })

@app.route('/api/zkp-generate', methods=['POST'])
def generate_zkp():
    """Zero-Knowledge Proof Resume Generator Simulation"""
    data = request.json
    skills = data.get("found_skills", [])
    hash_input = "".join(skills) + str(time.time())
    zkp_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    return jsonify({
        "zkp_token": f"ZKP-VERIFIED-{zkp_hash[:16].upper()}",
        "message": "Your ZKP token mathematically proves you possess the verified skills without revealing your identity."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
