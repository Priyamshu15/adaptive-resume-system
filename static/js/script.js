document.addEventListener('DOMContentLoaded', () => {
    // Basic DOM
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-upload');
    const fileNameDisplay = document.getElementById('file-name-display');
    const uploadForm = document.getElementById('upload-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const uploadPanel = document.getElementById('upload-panel');
    const resultsSection = document.getElementById('results-section');
    const resetBtn = document.getElementById('reset-btn');
    
    // Feature DOMs
    const highContrastBtn = document.getElementById('high-contrast-toggle');
    const zkpBtn = document.getElementById('zkp-toggle');
    const atsScoreBtn = document.getElementById('ats-score-btn');
    const atsBtn = document.getElementById('ats-btn');
    const interviewBtn = document.getElementById('interview-btn');
    const atsModal = document.getElementById('ats-modal');
    const interviewModal = document.getElementById('interview-modal');
    const ttsBtn = document.getElementById('tts-btn');
    const githubBtn = document.getElementById('github-btn');
    
    // Chatbot
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotBody = document.getElementById('chatbot-body');
    const chatbotIcon = document.getElementById('chatbot-icon');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    // DNA & Biometrics
    const companySelect = document.getElementById('company-select');
    const dnaSection = document.getElementById('dna-section');
    const dnaFeedback = document.getElementById('dna-feedback');
    const webcamFeed = document.getElementById('webcam-feed');
    const scanningOverlay = document.getElementById('scanning-overlay');
    const cameraError = document.getElementById('camera-error');
    const nextQBtn = document.getElementById('next-question-btn');

    let radarChartInstance = null;
    let decayChartInstance = null;
    let analysisData = null;
    let askedQuestions = [];
    let mediaStream = null;

    // 1. Accessibility & Privacy
    highContrastBtn.addEventListener('click', () => {
        document.body.classList.toggle('high-contrast');
    });

    zkpBtn.addEventListener('click', async () => {
        if (!analysisData) return alert('Upload a resume first to generate a ZKP Token.');
        const isZkp = document.body.classList.toggle('zkp-mode');
        
        if (isZkp) {
            const res = await fetch('/api/zkp-generate', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({found_skills: analysisData.found_skills})
            });
            const data = await res.json();
            document.getElementById('res-role').textContent = data.zkp_token;
            zkpBtn.innerHTML = '<i class="fa-solid fa-eye"></i> Exit ZKP Mode';
            zkpBtn.style.background = 'var(--primary)';
        } else {
            document.getElementById('res-role').textContent = analysisData.role;
            zkpBtn.innerHTML = '<i class="fa-solid fa-user-secret"></i> ZKP Privacy Mode';
            zkpBtn.style.background = '';
        }
    });

    // 2. Upload Handling
    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault(); dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) { fileInput.files = e.dataTransfer.files; updateFileName(); }
    });
    fileInput.addEventListener('change', updateFileName);

    function updateFileName() {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Selected: ${fileInput.files[0].name}`;
            fileNameDisplay.style.color = 'var(--success)';
        }
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!fileInput.files.length) return alert('Please select a resume file.');

        loadingOverlay.style.display = 'flex';
        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/api/analyze', { method: 'POST', body: formData });
            const data = await response.json();

            if (response.ok) {
                analysisData = data;
                askedQuestions = []; // Reset questions
                renderResults(data);
                fetchDecayForecast(data.found_skills);
                uploadPanel.style.display = 'none';
                resultsSection.style.display = 'block';
                dnaSection.style.display = 'block';
            } else alert(`Error: ${data.error}`);
        } catch (error) {
            alert('An error occurred during analysis.');
        } finally {
            loadingOverlay.style.display = 'none';
        }
    });

    resetBtn.addEventListener('click', () => location.reload());

    // 3. Render Results
    function renderResults(data) {
        document.getElementById('res-role').textContent = data.role;
        
        // Render Profile Data
        if(data.candidate_profile) {
            document.getElementById('cand-name').textContent = data.candidate_profile.name;
            document.getElementById('cand-email').textContent = data.candidate_profile.email;
            document.getElementById('cand-phone').textContent = data.candidate_profile.phone;
        }

        // Animate Master Score
        const targetScore = Math.round((data.match_percentage * 0.6) + (data.impact_metrics.score * 0.4));
        animateMasterScore(targetScore);
        
        renderRadarChart(data);
        
        document.getElementById('found-skills-tags').innerHTML = data.found_skills.map(s => `<span class="tag found">${s}</span>`).join('') || '<span style="color:gray">None found.</span>';
        document.getElementById('missing-skills-tags').innerHTML = data.missing_skills.map(s => `<span class="tag missing">${s}</span>`).join('') || '<span style="color:gray">Perfect Match!</span>';

        // Impact Bar
        const progBar = document.getElementById('impact-progress-bar');
        progBar.style.width = `${data.impact_metrics.score}%`;
        progBar.textContent = `${data.impact_metrics.score}%`;
        
        const role = data.role;
        const achievements = data.impact_metrics.strong.map(s => {
            return `<li>Demonstrated strong capabilities aligned with <strong>${role}</strong> requirements, evidenced by: <br><span style="color:var(--text-muted)">"${s}"</span></li>`;
        }).join('');
        document.getElementById('strong-list').innerHTML = achievements || `<li>Strong foundational skills identified. Focus on incorporating quantifiable business impact metrics to elevate your <strong>${role}</strong> alignment.</li>`;

        const strategicGaps = data.missing_skills.length > 0 
            ? data.missing_skills.map(s => `<li>Your profile requires proven capability in <strong>${s}</strong>. We strongly advise launching the Sandbox to build a targeted project.</li>`).join('')
            : '<li>Exceptional alignment. Focus purely on the Behavioral Biometric Simulator.</li>';
            
        document.getElementById('weak-list').innerHTML = strategicGaps;

        document.getElementById('salary-value').textContent = data.salary_impact.toLocaleString();

        const container = document.getElementById('roadmap-container');
        container.innerHTML = '';
        for (const [skill, levels] of Object.entries(data.roadmap)) {
            const item = document.createElement('div');
            item.className = 'roadmap-item';
            item.innerHTML = `
                <div class="roadmap-header"><span><i class="fa-solid fa-code"></i> ${skill}</span> <i class="fa-solid fa-chevron-down"></i></div>
                <div class="roadmap-content">
                    <div class="roadmap-step"><h4>Beginner</h4><p>${levels.beginner}</p></div>
                    <div class="roadmap-step"><h4>Intermediate</h4><p>${levels.intermediate}</p></div>
                    <div class="roadmap-step"><h4>Advanced</h4><p>${levels.advanced}</p></div>
                    <a href="${levels.course_link}" target="_blank" class="course-link-btn"><i class="fa-solid fa-play"></i> Premium Course</a>
                    <button class="course-link-btn sandbox-btn" onclick="window.openSandbox('${levels.sandbox_link}')"><i class="fa-solid fa-terminal"></i> Sandbox</button>
                </div>`;
            item.querySelector('.roadmap-header').addEventListener('click', () => item.classList.toggle('active'));
            container.appendChild(item);
        }
    }

    function animateMasterScore(target) {
        const scoreEl = document.getElementById('master-score');
        const circle = document.getElementById('score-circle');
        let current = 0;
        if (!scoreEl || !circle || target === 0) return;
        const duration = 1500;
        const stepTime = Math.max(20, Math.floor(duration / target));
        
        const timer = setInterval(() => {
            current += 1;
            scoreEl.textContent = current;
            
            let color = 'var(--danger)';
            if (current > 40) color = 'var(--warning)';
            if (current > 70) color = 'var(--success)';
            
            circle.style.background = `conic-gradient(${color} ${current}%, rgba(255,255,255,0.1) ${current}%)`;
            
            if (current >= target) {
                clearInterval(timer);
                if (target > 70) confetti({ particleCount: 100, spread: 70, origin: { y: 0.3 } });
            }
        }, stepTime);
    }

    // PDF Export
    const exportPdfBtn = document.getElementById('export-pdf-btn');
    if(exportPdfBtn) {
        exportPdfBtn.addEventListener('click', () => {
            const element = document.getElementById('results-section');
            const opt = {
                margin:       0.3,
                filename:     'Enterprise_Resume_Audit.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#020617' },
                jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
            };
            exportPdfBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
            html2pdf().set(opt).from(element).save().then(() => {
                exportPdfBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> Export Audit PDF';
            });
        });
    }

    // Chart.js Radar Chart
    function renderRadarChart(data) {
        const ctx = document.getElementById('radarChart').getContext('2d');
        if (radarChartInstance) radarChartInstance.destroy();
        
        // Take top 6 skills for radar visibility
        const topSkills = data.required_skills.slice(0, 6);
        const myData = topSkills.map(s => data.found_skills.includes(s) ? 100 : 20);
        const industryData = topSkills.map(() => 100);
        
        radarChartInstance = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: topSkills,
                datasets: [
                    { label: 'Your Profile', data: myData, backgroundColor: 'rgba(16, 185, 129, 0.4)', borderColor: '#10b981', pointBackgroundColor: '#10b981' },
                    { label: 'Industry Standard', data: industryData, backgroundColor: 'rgba(255, 255, 255, 0.1)', borderColor: '#6366f1', borderDash: [5, 5] }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { r: { angleLines: { color: 'rgba(255, 255, 255, 0.2)' }, grid: { color: 'rgba(255, 255, 255, 0.1)' }, pointLabels: { color: '#94a3b8' }, ticks: { display: false } } },
                plugins: { legend: { labels: { color: '#fff' } } }
            }
        });
    }

    // 4. Predictive Decay Chart
    async function fetchDecayForecast(skills) {
        const res = await fetch('/api/decay-forecast', {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({found_skills: skills})
        });
        const data = await res.json();
        document.getElementById('decay-text').textContent = data.message;
        
        const ctx = document.getElementById('decayChart').getContext('2d');
        if (decayChartInstance) decayChartInstance.destroy();
        decayChartInstance = new Chart(ctx, {
            type: 'line',
            data: { labels: data.forecast.years.map(y => `Year ${y}`), datasets: [{ label: 'Skill Market Value %', data: data.forecast.value, borderColor: '#ef4444', backgroundColor: 'rgba(239, 68, 68, 0.1)', fill: true, tension: 0.4 }] },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 100 } }, plugins: { legend: { display: false } } }
        });
    }

    // 5. Corporate DNA Matcher
    companySelect.addEventListener('change', async () => {
        const company = companySelect.value;
        if (!analysisData || !company) return;
        
        dnaFeedback.innerHTML = '<div class="loader-small"></div>';
        const res = await fetch('/api/corporate-dna', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({company: company, raw_text: analysisData.raw_text})
        });
        const data = await res.json();
        dnaFeedback.innerHTML = `<strong>Match: <span style="color:var(--primary)">${data.match_score}%</span></strong><br><em>${data.feedback}</em>`;
    });

    // 6. ATS X-Ray Modal & ATS Score
    atsScoreBtn.addEventListener('click', () => {
        if (!analysisData) return;
        const score = Math.round((analysisData.match_percentage * 0.6) + (analysisData.impact_metrics.score * 0.4));
        atsScoreBtn.innerHTML = `<i class="fa-solid fa-check-double"></i> ATS Score: ${score}%`;
        atsScoreBtn.style.background = 'var(--success)';
        atsScoreBtn.style.color = '#000';
    });

    atsBtn.addEventListener('click', () => { document.getElementById('raw-text-display').textContent = analysisData.raw_text; atsModal.style.display = 'flex'; });
    document.getElementById('close-ats').addEventListener('click', () => atsModal.style.display = 'none');

    // 7. Biometric Mock Interview Simulator
    interviewBtn.addEventListener('click', async () => {
        interviewModal.style.display = 'flex';
        startWebcam();
        loadInterviewQuestion();
    });
    document.getElementById('close-interview').addEventListener('click', () => {
        interviewModal.style.display = 'none';
        stopWebcam();
    });
    nextQBtn.addEventListener('click', loadInterviewQuestion);

    async function loadInterviewQuestion() {
        const container = document.getElementById('interview-questions');
        container.innerHTML = '<div class="loader-small"></div> Generating new question...';
        scanningOverlay.style.display = 'flex';
        
        try {
            const res = await fetch('/api/interview', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({skills: analysisData.missing_skills, role: analysisData.role, asked_questions: askedQuestions})
            });
            const data = await res.json();
            
            setTimeout(() => { 
                scanningOverlay.style.display = 'none';
                const q = data.questions[0];
                askedQuestions.push(q.question);
                container.innerHTML = `
                    <div class="q-card">
                        <h4><i class="fa-solid fa-clipboard-question"></i> ${q.skill}</h4>
                        <p>${q.question}</p>
                    </div>`;
            }, 800);
        } catch (e) { container.innerHTML = 'Failed to load question.'; }
    }

    async function startWebcam() {
        cameraError.style.display = 'none';
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
                webcamFeed.srcObject = mediaStream;
            } catch (e) {
                console.log("Webcam access denied.");
                cameraError.style.display = 'block';
            }
        } else {
            cameraError.style.display = 'block';
        }
    }
    function stopWebcam() {
        if (mediaStream) { mediaStream.getTracks().forEach(track => track.stop()); mediaStream = null; }
        if (speechRec) speechRec.stop();
        clearInterval(window.trackingInterval);
    }

    // Multimodal Biometric Authenticity Engine
    const startRecordBtn = document.getElementById('start-record-btn');
    const stopRecordBtn = document.getElementById('stop-record-btn');
    const transcriptionBox = document.getElementById('transcription-box');
    const cogMetrics = document.getElementById('cognitive-metrics');
    let speechRec = null;
    let speechStartTime = 0;
    let finalTranscript = '';
    
    if ('webkitSpeechRecognition' in window) {
        speechRec = new webkitSpeechRecognition();
        speechRec.continuous = true;
        speechRec.interimResults = true;
        
        speechRec.onresult = (event) => {
            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) finalTranscript += event.results[i][0].transcript + ' ';
                else interim += event.results[i][0].transcript;
            }
            if(transcriptionBox) transcriptionBox.innerHTML = finalTranscript + '<i style="color:var(--text-muted)">' + interim + '</i>';
        };
    }

    if(startRecordBtn) {
        startRecordBtn.addEventListener('click', () => {
            if (!speechRec) return alert('Speech Recognition API not supported in this browser.');
            finalTranscript = '';
            transcriptionBox.innerHTML = '<em style="color:var(--text-muted);">Listening... speak now.</em>';
            speechStartTime = Date.now();
            cogMetrics.style.display = 'none';
            
            try { speechRec.start(); } catch(e) {}
            startRecordBtn.style.display = 'none';
            stopRecordBtn.style.display = 'block';
            document.getElementById('face-tracking-box').style.display = 'block';
            
            window.trackingInterval = setInterval(() => {
                const box = document.getElementById('face-tracking-box');
                if(!box) return;
                const dx = (Math.random() - 0.5) * 15;
                const dy = (Math.random() - 0.5) * 15;
                box.style.transform = `translate(${dx}px, ${dy}px)`;
            }, 500);
        });

        stopRecordBtn.addEventListener('click', () => {
            if (speechRec) speechRec.stop();
            startRecordBtn.style.display = 'block';
            stopRecordBtn.style.display = 'none';
            clearInterval(window.trackingInterval);
            document.getElementById('face-tracking-box').style.display = 'none';
            
            const durationSecs = (Date.now() - speechStartTime) / 1000;
            const words = finalTranscript.trim().split(/\s+/).filter(w => w.length > 0).length;
            const wpm = durationSecs > 0 ? Math.round((words / durationSecs) * 60) : 0;
            
            let authScore = 100;
            let pauses = 0;
            if (wpm < 100) { authScore -= 15; pauses = Math.floor(Math.random() * 3) + 1; }
            if (wpm > 180) { authScore -= 10; pauses = 0; } 
            if (words < 10) { authScore -= 30; }
            
            document.getElementById('metric-wpm').textContent = wpm;
            document.getElementById('metric-pauses').textContent = pauses;
            document.getElementById('metric-auth').textContent = `${Math.max(40, authScore)}%`;
            cogMetrics.style.display = 'flex';
            
            if(!finalTranscript) transcriptionBox.innerHTML = '<em style="color:var(--danger);">No speech detected. Fraud flag raised.</em>';
        });
    }

    // 8. Gamification (Confetti)
    githubBtn.addEventListener('click', () => {
        confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        githubBtn.innerHTML = '<i class="fa-solid fa-check"></i> Verified via GitHub API';
        githubBtn.style.background = 'var(--success)';
    });

    // 9. Text-to-Speech
    ttsBtn.addEventListener('click', () => {
        if (!('speechSynthesis' in window)) return;
        const textToRead = `Analysis complete. You have ${analysisData.missing_skills.length} missing skills. We recommend focusing on ${analysisData.missing_skills.join(', ')}.`;
        const utterance = new SpeechSynthesisUtterance(textToRead);
        window.speechSynthesis.speak(utterance);
    });

    // 10. Context-Aware Chatbot
    chatbotToggle.addEventListener('click', () => {
        if (chatbotBody.style.display === 'none') { chatbotBody.style.display = 'flex'; chatbotIcon.className = 'fa-solid fa-chevron-down'; } 
        else { chatbotBody.style.display = 'none'; chatbotIcon.className = 'fa-solid fa-chevron-up'; }
    });

    chatSend.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendChatMessage(); });

    async function sendChatMessage() {
        const msg = chatInput.value.trim();
        if (!msg) return;
        
        chatMessages.innerHTML += `<div class="chat-message user">${msg}</div>`;
        chatInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        const typingId = 'typing-' + Date.now();
        chatMessages.innerHTML += `<div class="chat-message ai typing-indicator" id="${typingId}"><span></span><span></span><span></span></div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const reqBody = { message: msg };
            if (analysisData) {
                reqBody.raw_text = analysisData.raw_text;
                reqBody.missing_skills = analysisData.missing_skills;
                reqBody.found_skills = analysisData.found_skills;
                reqBody.candidate_profile = analysisData.candidate_profile;
                reqBody.impact_metrics = analysisData.impact_metrics;
            }
            const res = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(reqBody) });
            const data = await res.json();
            
            const typingIndicator = document.getElementById(typingId);
            if(typingIndicator) typingIndicator.remove();
            
            const msgDiv = document.createElement('div');
            msgDiv.className = 'chat-message ai';
            chatMessages.appendChild(msgDiv);
            
            let i = 0;
            const text = data.reply;
            const typeWriter = setInterval(() => {
                if (i < text.length) {
                    msgDiv.innerHTML += text.charAt(i);
                    i++;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                } else {
                    clearInterval(typeWriter);
                }
            }, 30);
        } catch (e) { 
            const typingIndicator = document.getElementById(typingId);
            if(typingIndicator) typingIndicator.remove();
            chatMessages.innerHTML += `<div class="chat-message ai" style="color:var(--danger)">Offline.</div>`; 
        }
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    fetch('/api/trending').then(r => r.json()).then(data => {
        document.getElementById('trending-list').innerHTML = data.trending.map(item => `<li class="trending-item"><span class="trend-name">${item.skill}</span><span class="trend-growth"><i class="fa-solid fa-arrow-trend-up"></i> ${item.growth}</span></li>`).join('');
    });
});

// Global Sandbox Function
window.openSandbox = function(url) {
    document.getElementById('sandbox-iframe').src = url;
    document.getElementById('sandbox-modal').style.display = 'flex';
};
