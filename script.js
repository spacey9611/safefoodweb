// Australian Food Safety Practice Test - Main Logic
// Programmatic SEO & Quiz Game Logic

import { QUESTIONS } from './questions.js';

const PROGRESS_KEY  = 'fs_progress_v1';
const GAMIFY_KEY    = 'fs_gamify_v1';
const THEME_KEY     = 'fs_theme_v1';
const EXAM_SECONDS_PER_Q = 60; // Exam Mode: time budget per question

// ─── DARK MODE ───────────────────────────────────────────────────────────────
function applyTheme(theme) {
    if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
    document.querySelectorAll('.theme-toggle').forEach((btn) => {
        btn.textContent = theme === 'dark' ? '☀️' : '🌙';
        btn.setAttribute('aria-pressed', String(theme === 'dark'));
    });
}
function initTheme() {
    let theme = 'light';
    try { theme = localStorage.getItem(THEME_KEY) || 'light'; } catch {}
    // Inject a toggle button into the header tools area if not already present
    const tools = document.querySelector('.site-header__tools') || document.querySelector('.site-header__top');
    if (tools && !document.querySelector('.theme-toggle')) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'theme-toggle';
        btn.setAttribute('aria-label', 'Toggle dark mode');
        btn.title = 'Toggle dark mode';
        btn.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const next = isDark ? 'light' : 'dark';
            applyTheme(next);
            try { localStorage.setItem(THEME_KEY, next); } catch {}
        });
        tools.appendChild(btn);
    }
    applyTheme(theme);
}

// ─── GAMIFICATION ────────────────────────────────────────────────────────────

const XP_CORRECT = 10;
const XP_WRONG   = 2;

const LEVELS = [
    { label: 'Kitchen Hand',    min: 0    },
    { label: 'Line Cook',      min: 100  },
    { label: 'Chef',    min: 500  },
    { label: 'Head Chef',   min: 1500 },
    { label: 'Food Safety Supervisor', min: 3000 },
    { label: 'Food Safety Champion', min: 6000 },
];

function getLevel(xp) {
    let level = LEVELS[0];
    for (const l of LEVELS) { if (xp >= l.min) level = l; }
    return level;
}

function todayStr() {
    return new Date().toISOString().slice(0, 10);
}

function loadGamify() {
    try {
        const raw = localStorage.getItem(GAMIFY_KEY);
        if (raw) return JSON.parse(raw);
    } catch {}
    return { xp: 0, streak: 0, lastDate: null };
}

function saveGamify(data) {
    try { localStorage.setItem(GAMIFY_KEY, JSON.stringify(data)); } catch {}
}

function addXP(correct, wrong) {
    const earned = correct * XP_CORRECT + wrong * XP_WRONG;
    if (earned <= 0) return;
    const g = loadGamify();
    const today = todayStr();
    // Streak logic
    if (g.lastDate === today) {
        // same day, no streak change
    } else {
        const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
        g.streak = g.lastDate === yesterday ? (g.streak || 0) + 1 : 1;
        g.lastDate = today;
    }
    g.xp = (g.xp || 0) + earned;
    saveGamify(g);
    return { earned, xp: g.xp, streak: g.streak };
}

function getDailyChallenge() {
    // Deterministic question based on today's date
    const seed = todayStr().replace(/-/g, '');
    const idx  = parseInt(seed, 10) % QUESTIONS.length;
    return QUESTIONS[idx];
}

function mountGamificationDashboard() {
    const startScreen = document.getElementById('start-screen');
    if (!startScreen || document.getElementById('gamify-dashboard')) return;

    const progress = loadProgress();
    if (!hasPriorAttempt(progress)) return;

    const g = loadGamify();
    const best = getBestScore(progress);
    const attempts = Array.isArray(progress?.attempts) ? progress.attempts.length : (progress?.attemptCount || 0);

    const dashboard = document.createElement('div');
    dashboard.id = 'gamify-dashboard';
    dashboard.className = 'gamify-dashboard';
    dashboard.setAttribute('aria-label', 'Your progress');
    dashboard.innerHTML = `
        <div class="gamify-stat">
            <span class="gamify-value">${best}%</span>
            <span class="gamify-label">Best score</span>
        </div>
        <div class="gamify-stat">
            <span class="gamify-value">${attempts}</span>
            <span class="gamify-label">Tests completed</span>
        </div>
        <div class="gamify-stat">
            <span class="gamify-value">${g.streak || 0}</span>
            <span class="gamify-label">Day streak</span>
        </div>
    `;

    const modeSelection = document.getElementById('mode-selection');
    if (modeSelection) {
        startScreen.insertBefore(dashboard, modeSelection);
    } else {
        startScreen.appendChild(dashboard);
    }
}

function mountDailyChallenge() {
    const startScreen = document.getElementById('start-screen');
    if (!startScreen || document.getElementById('daily-challenge')) return;

    const q = getDailyChallenge();
    const dcKey = `fs_dc_${todayStr()}`;
    const answered = localStorage.getItem(dcKey);

    const widget = document.createElement('div');
    widget.id = 'daily-challenge';
    widget.className = 'daily-challenge';

    if (answered) {
        const wasCorrect = answered === 'correct';
        widget.innerHTML = `
            <p class="dc-title">Daily Challenge: <strong>Done!</strong></p>
            <p class="dc-result ${wasCorrect ? 'dc-correct' : 'dc-wrong'}">
                ${wasCorrect ? 'Correct! +10 XP' : 'Wrong: review and try again tomorrow'}
            </p>
        `;
    } else {
        widget.innerHTML = `
            <p class="dc-title">Daily Challenge</p>
            <p class="dc-question">${q.question}</p>
            <div class="dc-options">
                ${shuffle(q.options.map((_, i) => i)).map((i) => `
                    <button type="button" class="dc-opt-btn" data-idx="${i}">${q.options[i]}</button>
                `).join('')}
            </div>
        `;
        // Wire up answers after inserting
        setTimeout(() => {
            widget.querySelectorAll('.dc-opt-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const selected = parseInt(btn.dataset.idx, 10);
                    const correct  = selected === q.answer;
                    const result   = correct ? 'correct' : 'wrong';
                    try { localStorage.setItem(dcKey, result); } catch {}

                    widget.querySelectorAll('.dc-opt-btn').forEach((b) => {
                        b.disabled = true;
                        const di = parseInt(b.dataset.idx, 10);
                        if (di === q.answer) b.classList.add('dc-correct');
                        else if (di === selected && !correct) b.classList.add('dc-wrong');
                    });

                    const msg = document.createElement('p');
                    msg.className = `dc-result ${correct ? 'dc-correct' : 'dc-wrong'}`;
                    msg.textContent = correct
                        ? 'Correct! +10 XP earned.'
                        : `The answer was: ${q.options[q.answer]}`;
                    widget.appendChild(msg);

                    if (correct) addXP(1, 0);
                    else addXP(0, 1);

                    // Refresh dashboard XP
                    const dash = document.getElementById('gamify-dashboard');
                    if (dash) { dash.remove(); mountGamificationDashboard(); }
                });
            });
        }, 0);
    }

    // Bonus card placed after the practice options
    const modeSelection = document.getElementById('mode-selection');
    if (modeSelection) {
        modeSelection.parentNode.insertBefore(widget, modeSelection.nextSibling);
    } else {
        startScreen.appendChild(widget);
    }
}

const TOPIC_LABELS = [
    { slug: 'food-standards', label: 'Food Standards Code & Legislation' },
    { slug: 'food-handler', label: 'Food Handler Responsibilities' },
    { slug: 'temperature', label: 'Temperature & Danger Zone' },
    { slug: 'cross-contamination', label: 'Cross Contamination' },
    { slug: 'hygiene', label: 'Personal Hygiene' },
    { slug: 'cleaning', label: 'Cleaning & Sanitising' },
    { slug: 'allergens', label: 'Allergen Management' },
    { slug: 'storage', label: 'Food Storage & Labelling' },
    { slug: 'pest-control', label: 'Pest Control' },
    { slug: 'haccp', label: 'HACCP Basics' },
    { slug: 'fss-duties', label: 'Food Safety Supervisor Duties' },
    { slug: 'high-risk', label: 'High-Risk Foods & Vulnerable Groups' }
];

function loadProgress() {
    if (!window.localStorage) return null;
    try {
        const raw = localStorage.getItem(PROGRESS_KEY);
        if (!raw) return null;
        return JSON.parse(raw);
    } catch {
        return null;
    }
}

function saveProgress(percentage, answers, wrongQuestions) {
    if (!window.localStorage) return;

    const progress = loadProgress() || {
        attempts: [],
        bestScore: 0,
        weakQuestionIds: [],
    };

    progress.attempts.push({
        percentage,
        at: new Date().toISOString(),
    });

    progress.bestScore = Math.max(progress.bestScore ?? 0, percentage);

    const weakSet = new Set(progress.weakQuestionIds ?? []);
    wrongQuestions.forEach((q) => weakSet.add(q.id));
    answers
        .filter((a) => a.correct)
        .forEach((a) => weakSet.delete(a.id));
    progress.weakQuestionIds = [...weakSet];

    try {
        localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
    } catch {
        // ignore quota / private mode errors
    }
}

function hasPriorAttempt(progress) {
    if (!progress) return false;
    if (Array.isArray(progress.attempts) && progress.attempts.length > 0) {
        return true;
    }
    if (typeof progress.attemptCount === 'number' && progress.attemptCount > 0) {
        return true;
    }
    return false;
}

function getBestScore(progress) {
    if (!progress) return 0;
    if (typeof progress.bestScore === 'number') {
        return progress.bestScore;
    }
    if (Array.isArray(progress.attempts) && progress.attempts.length > 0) {
        return Math.max(
            ...progress.attempts.map(
                (a) => a.percentage ?? a.bestScore ?? 0
            )
        );
    }
    return 0;
}

function getWeakQuestions() {
    const progress = loadProgress();
    const ids = progress?.weakQuestionIds ?? [];
    return QUESTIONS.filter((q) => ids.includes(q.id));
}

// Unbiased Fisher-Yates shuffle (returns a new array, does not mutate input)
function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// Stratified, lightly-weighted selection so a full test always covers every topic
// (with extra weight on the most-tested areas) rather than a lopsided random draw.
function pickStratified(pool, n) {
    const WEIGHT = { temperature: 2, 'cross-contamination': 1.5, hygiene: 1.5, allergens: 1.5, 'high-risk': 1.5 };
    const byTopic = {};
    pool.forEach((q) => { (byTopic[q.topic] = byTopic[q.topic] || []).push(q); });
    const topics = Object.keys(byTopic);
    if (!topics.length) return [];
    topics.forEach((t) => { byTopic[t] = shuffle(byTopic[t]); });
    const totalW = topics.reduce((s, t) => s + (WEIGHT[t] || 1), 0);
    let picked = [];
    topics.forEach((t) => {
        const want = Math.max(1, Math.round(n * (WEIGHT[t] || 1) / totalW));
        picked.push(...byTopic[t].slice(0, want));
    });
    picked = shuffle(picked);
    if (picked.length < n) {
        const have = new Set(picked.map((q) => q.id));
        const rest = shuffle(pool.filter((q) => !have.has(q.id)));
        picked = picked.concat(rest.slice(0, n - picked.length));
    }
    return picked.slice(0, n);
}

function pickQuestions(mode, topic) {
    if (mode === 'review') {
        return shuffle(getWeakQuestions());
    }
    // Only surface state-specific questions on the matching state page (default = none).
    const state = (typeof getCurrentState === 'function') ? getCurrentState() : 'default';
    let pool = topic ? QUESTIONS.filter((q) => q.topic === topic) : QUESTIONS.slice();
    pool = pool.filter((q) => !q.state || q.state === state);

    if (mode === 'quick') return shuffle(pool).slice(0, 5);
    if (topic) return shuffle(pool).slice(0, Math.min(40, pool.length)); // topic drill: single-topic
    return pickStratified(pool, 40); // full / exam: guarantee topic coverage
}

function track(eventName, data = {}) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: eventName, ...data });
    // Also send to GA4 directly so events show without extra GTM config
    if (typeof window.gtag === 'function') window.gtag('event', eventName, data);
}

let lastSession = null;
let activeQuizController = null;

function showResults(score, wrongQuestions, mode, topic, total) {
    const container = document.getElementById('result-screen');
    if (!container) return;

    const questionTotal = total || score + wrongQuestions.length;
    const percentage =
        questionTotal > 0 ? Math.round((score / questionTotal) * 100) : 0;
    const passed = percentage >= 80;
    const wrongCount = wrongQuestions.length;

    lastSession = {
        score,
        wrongQuestions,
        mode,
        topic,
        total: questionTotal,
        percentage,
    };

    const reviewMarkup =
        wrongCount > 0
            ? `<button type="button" class="btn btn-review results-review-btn">Review your ${wrongCount} wrong answer${wrongCount === 1 ? '' : 's'}</button>`
            : '';

    container.innerHTML = `
        <div class="result-content result-content--premium">
            <h2 class="results-title">Test Complete</h2>
            <div class="results-ring-wrap">
                <div class="results-ring ${passed ? 'results-ring--pass' : 'results-ring--fail'}" style="--score: ${percentage}">
                    <div class="results-ring__inner">
                        <span class="results-score-pct ${passed ? 'results-score-pct--pass' : 'results-score-pct--fail'}" aria-label="Score ${percentage} percent">${percentage}%</span>
                        <span class="results-ring__label">${passed ? 'Exam ready' : 'Keep practising'}</span>
                    </div>
                </div>
            </div>
            <p class="results-score-detail">You got ${score} out of ${questionTotal} correct.</p>
            <p class="results-readiness ${passed ? 'results-readiness--pass' : 'results-readiness--fail'}">${
                passed
                    ? "Strong work: you're on track. Most RTOs require around 80% to pass the official food safety assessment."
                    : "Review your weak spots and try again. Aim for 80%+ before sitting your official assessment."
            }</p>
            <div class="results-actions">
                ${reviewMarkup}
                <button type="button" class="btn btn-primary results-restart-btn">Try Again</button>
            </div>
            <div class="ad-slot" data-ad-slot="results-incontent" role="complementary" aria-label="Advertisement"><span class="ad-slot__label">Advertisement</span></div>
            <aside class="results-affiliate-cta">
                <p class="results-affiliate-copy">${
                    passed
                        ? 'You scored 80%+. Compare accredited courses and book your official certificate from $85.'
                        : 'Keep practising until you hit 80%, then compare accredited courses to get certified.'
                }</p>
                <a href="/find-a-course.html" class="results-affiliate-btn" rel="sponsored nofollow">Compare courses in your state</a>
            </aside>
        </div>
    `;

    const reviewBtn = container.querySelector('.results-review-btn');
    if (reviewBtn) {
        reviewBtn.addEventListener('click', () => {
            const shuffled = shuffle(lastSession.wrongQuestions);
            startQuiz(lastSession.mode, lastSession.topic, shuffled);
        });
    }

    container.querySelector('.results-restart-btn').addEventListener('click', () => {
        startQuiz(lastSession.mode, lastSession.topic);
    });

    const affiliateLink = container.querySelector('.results-affiliate-btn');
    affiliateLink.addEventListener('click', () => {
        track('affiliate_click', { placement: 'results_cta' });
    });
}

// State Regulator Dictionary
const stateRegulators = {
    'nsw': 'NSW Food Authority',
    'vic': 'Department of Health Victoria',
    'qld': 'Queensland Health',
    'wa': 'WA Department of Health',
    'sa': 'SA Health',
    'act': 'ACT Health',
    'nt': 'NT Health',
    'tas': 'Department of Health Tasmania',
    'default': 'Food Standards Australia New Zealand'
};

// State Display Names
const stateNames = {
    'nsw': 'NSW',
    'vic': 'VIC',
    'qld': 'QLD',
    'wa': 'WA',
    'sa': 'SA',
    'act': 'ACT',
    'nt': 'NT',
    'tas': 'TAS',
    'default': 'Australia'
};

// Parse URL parameters
function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Get current state, checks URL param first, then the page's <meta name="state"> tag
function getCurrentState() {
    const paramState = getURLParameter('state');
    if (paramState && stateRegulators[paramState.toLowerCase()]) {
        return paramState.toLowerCase();
    }
    const stateMeta = document.querySelector('meta[name="state"]');
    if (stateMeta) {
        const metaState = stateMeta.getAttribute('content');
        if (metaState && stateRegulators[metaState.toLowerCase()]) {
            return metaState.toLowerCase();
        }
    }
    return 'default';
}

// Apply Programmatic SEO, only updates meta/title on index.html (no state meta tag).
// State HTML pages already have correct static SEO in their HTML; this function
// leaves their content untouched and only runs full updates on the national page.
function applySEO() {
    const state = getCurrentState();
    if (state === 'default') return;

    const stateName = stateNames[state];
    const regulator = stateRegulators[state];

    // On index.html (?state=xxx) update the title/meta dynamically.
    // On dedicated state pages the static HTML already has these set correctly,
    // so we only update if we're on the index (no meta[name="state"] tag).
    const hasStateMeta = !!document.querySelector('meta[name="state"]');
    if (!hasStateMeta) {
        document.title = `Free Food Safety Practice Test ${stateName} 2026 | SITXFSA005 Questions`;

        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            metaDesc.setAttribute('content', `Free Food Safety practice test for ${stateName}. 400 questions aligned with ${regulator} and SITXFSA005 standards. Pass your food safety certification today.`);
        }

        const ogTitle = document.querySelector('meta[property="og:title"]');
        if (ogTitle) ogTitle.setAttribute('content', `Free Food Safety Practice Test ${stateName} 2026 | SITXFSA005`);

        const ogDesc = document.querySelector('meta[property="og:description"]');
        if (ogDesc) ogDesc.setAttribute('content', `Free Food Safety practice test for ${stateName}. 400 questions aligned with ${regulator}.`);

        // Canonicalise ?state=xx to its dedicated state page to avoid duplicate URLs
        const canon = document.querySelector('link[rel="canonical"]');
        if (canon) canon.setAttribute('href', `https://food-safety-practice-test-au.com/food-safety-${state}.html`);
    }

    // Update H1 only if it still shows the generic text (handles index.html ?state= visits)
    const h1 = document.querySelector('h1');
    if (h1 && h1.textContent.trim() === 'Food Safety Practice Test') {
        h1.textContent = `Food Safety Practice Test ${stateName}`;
    }
    // NOTE: the SEO article content is NOT overwritten here, static HTML is preserved
    // so Googlebot gets the full rich content on first render.
}

function getQuizConfig() {
    const modeParam = (getURLParameter('mode') || 'full').toLowerCase();
    const topicParam = getURLParameter('topic');
    const mode = ['full', 'quick', 'topic', 'review', 'exam'].includes(modeParam)
        ? modeParam
        : 'full';
    const topic = mode === 'topic' && topicParam ? topicParam : null;
    return { mode, topic };
}

function selectMode(mode, topic = null) {
    track('mode_selected', topic ? { mode, topic } : { mode });

    if (mode === 'review' && getWeakQuestions().length === 0) {
        return null;
    }

    return startQuiz(mode, topic);
}

function mountModeSelection() {
    if (document.getElementById('mode-selection')) return;
    const startScreen = document.getElementById('start-screen');
    if (!startScreen) return;

    const progress = loadProgress();
    const bestScore = getBestScore(progress);
    const showWelcome = hasPriorAttempt(progress);
    const weakCount = getWeakQuestions().length;

    const welcomeMarkup = showWelcome
        ? `<p class="welcome-back">Welcome back, your best score is ${bestScore}%. ${
              bestScore >= 80 ? 'You look ready!' : 'Keep practising.'
          }</p>`
        : '';

    const topicButtons = TOPIC_LABELS.map(
        ({ slug, label }) =>
            `<button type="button" class="btn btn-topic" data-topic="${slug}">${label}</button>`
    ).join('');

    const reviewHint =
        weakCount === 0
            ? '<p class="review-mode-hint" id="review-mode-hint">Complete a practice test to unlock review of your wrong answers.</p>'
            : '';

    const mount = document.createElement('div');
    mount.id = 'mode-selection';
    mount.className = 'mode-selection';
    mount.innerHTML = `
        <p class="mode-selection__title">Choose how to practise</p>
        ${welcomeMarkup}
        <div class="mode-buttons" role="group" aria-label="Quiz mode">
            <button type="button" class="btn btn-mode" data-mode="quick">Quick Quiz · 5 questions · ~3 min</button>
            <button type="button" class="btn btn-mode" data-mode="full">Full Test · 40 questions · ~25 min</button>
            <button type="button" class="btn btn-mode" data-mode="exam">Timed Exam · 40 questions · 40 min</button>
            <button type="button" class="btn btn-mode" data-mode="review" ${
                weakCount === 0 ? 'disabled aria-describedby="review-mode-hint"' : ''
            }>Review weak questions</button>
        </div>
        ${reviewHint}
        <div class="topic-drill">
            <p class="topic-drill-label">Or drill a single topic</p>
            <div class="topic-buttons" role="group" aria-label="Topic drill">
                ${topicButtons}
            </div>
        </div>
    `;

    const mountTarget =
        document.getElementById('practice-modes') ||
        document.querySelector('.intro-content--modes') ||
        document.getElementById('start-screen');
    mountTarget?.appendChild(mount);

    mount.querySelectorAll('[data-mode]').forEach((btn) => {
        btn.addEventListener('click', () => {
            selectMode(btn.dataset.mode);
        });
    });

    mount.querySelectorAll('[data-topic]').forEach((btn) => {
        btn.addEventListener('click', () => {
            selectMode('topic', btn.dataset.topic);
        });
    });
}

class QuizController {
    constructor(container, mode, topic, questions = null) {
        this.container = container;
        this.mode = mode;
        this.topic = topic;
        this.questions = questions ?? pickQuestions(mode, topic);
        this.index = 0;
        this.score = 0;
        this.answers = [];
        this.wrongQuestions = [];
        this.answered = false;
        this.mount();
    }

    mount() {
        this.container.innerHTML = `
            <div class="quiz-shell">
                <div class="progress-container">
                    <div class="progress-header">
                        <span class="progress-label">Question <span class="quiz-current">1</span> of <span class="quiz-total">1</span></span>
                        <span class="quiz-meta">
                            <span class="combo-pill" hidden>Streak <span class="combo-num">0</span></span>
                            <span class="timer-pill" hidden>Time <span class="timer-text">00:00</span></span>
                            <span class="progress-pct">0%</span>
                        </span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
                <div class="question-container">
                    <h3 class="question-text"></h3>
                    <div class="question-tools">
                        <button type="button" class="q-tool q-tts" aria-label="Read question aloud">Read aloud</button>
                        <button type="button" class="q-tool q-bookmark" aria-pressed="false">Bookmark</button>
                    </div>
                    <div class="options-container"></div>
                    <div class="explanation"></div>
                    <button type="button" class="btn btn-primary quiz-next-btn" style="display: none;">Next Question</button>
                </div>
            </div>
        `;

        this.progressFill = this.container.querySelector('.progress-fill');
        this.progressPct = this.container.querySelector('.progress-pct');
        this.currentEl = this.container.querySelector('.quiz-current');
        this.totalEl = this.container.querySelector('.quiz-total');
        this.questionText = this.container.querySelector('.question-text');
        this.optionsContainer = this.container.querySelector('.options-container');
        this.explanationEl = this.container.querySelector('.explanation');
        this.nextBtn = this.container.querySelector('.quiz-next-btn');
        this.ttsBtn = this.container.querySelector('.q-tts');
        this.bookmarkBtn = this.container.querySelector('.q-bookmark');
        this.comboPill = this.container.querySelector('.combo-pill');
        this.comboNum = this.container.querySelector('.combo-num');
        this.timerPill = this.container.querySelector('.timer-pill');
        this.timerText = this.container.querySelector('.timer-text');

        this.nextBtn.addEventListener('click', () => this.handleNext());
        if (this.ttsBtn) {
            this.ttsBtn.addEventListener('click', () => {
                const q = this.questions[this.index];
                speakText(`${q.question}. ${q.options.join('. ')}`);
            });
        }
        if (this.bookmarkBtn) {
            this.bookmarkBtn.addEventListener('click', () => {
                const q = this.questions[this.index];
                const on = toggleBookmark(q.id);
                this.updateBookmarkBtn(on);
            });
        }
    }

    updateBookmarkBtn(on) {
        if (!this.bookmarkBtn) return;
        this.bookmarkBtn.setAttribute('aria-pressed', String(on));
        this.bookmarkBtn.classList.toggle('is-on', on);
        this.bookmarkBtn.innerHTML = on ? 'Saved' : 'Bookmark';
    }

    start() {
        if (this.questions.length === 0) {
            return false;
        }

        track('quiz_start', {
            mode: this.mode,
            topic: this.topic,
            total: this.questions.length,
        });

        this.index = 0;
        this.score = 0;
        this.answers = [];
        this.wrongQuestions = [];
        this.answered = false;
        this.combo = 0;
        this.maxCombo = 0;
        this.updateCombo();

        // Exam Mode: start a countdown timer that auto-submits at zero
        if (this.mode === 'exam' && this.timerPill) {
            this.timeLeft = this.questions.length * EXAM_SECONDS_PER_Q;
            this.timerPill.hidden = false;
            this.updateTimer();
            this.timerId = setInterval(() => {
                this.timeLeft -= 1;
                this.updateTimer();
                if (this.timeLeft <= 0) {
                    this.stopTimer();
                    this.complete();
                }
            }, 1000);
        }

        showScreen('quiz-screen');
        this.renderQuestion();
        requestAnimationFrame(() => {
            this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        return true;
    }

    updateCombo() {
        if (!this.comboPill) return;
        this.comboNum.textContent = String(this.combo);
        this.comboPill.hidden = this.combo < 2;
    }

    updateTimer() {
        if (!this.timerText) return;
        const t = Math.max(0, this.timeLeft);
        const m = String(Math.floor(t / 60)).padStart(2, '0');
        const s = String(t % 60).padStart(2, '0');
        this.timerText.textContent = `${m}:${s}`;
        if (this.timerPill) this.timerPill.classList.toggle('timer-pill--warning', t <= 30);
    }

    stopTimer() {
        if (this.timerId) { clearInterval(this.timerId); this.timerId = null; }
    }

    renderQuestion() {
        const question = this.questions[this.index];
        const total = this.questions.length;
        const position = this.index + 1;

        this.answered = false;
        const pct = Math.round((position / total) * 100);
        this.progressFill.style.width = `${pct}%`;
        if (this.progressPct) this.progressPct.textContent = `${pct}%`;
        this.currentEl.textContent = String(position);
        this.totalEl.textContent = String(total);
        this.questionText.textContent = question.question;
        this.updateBookmarkBtn(loadBookmarks().includes(question.id));

        this.optionsContainer.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
        // Shuffle the option order each render so the correct answer is not always first.
        const order = shuffle(question.options.map((_, i) => i));
        this.correctRenderedIndex = order.indexOf(question.answer);
        order.forEach((origIndex, renderIndex) => {
            const option = question.options[origIndex];
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'option-btn';
            btn.innerHTML = `<span class="option-btn__letter">${letters[renderIndex] || '?'}</span><span class="option-btn__text">${option}</span>`;
            btn.addEventListener('click', () => this.handleAnswer(renderIndex, question));
            this.optionsContainer.appendChild(btn);
        });

        this.explanationEl.textContent = '';
        this.explanationEl.style.display = 'none';
        this.nextBtn.style.display = 'none';
        this.nextBtn.textContent =
            position === total ? 'See Results' : 'Next Question';
    }

    handleAnswer(selectedIndex, question) {
        if (this.answered) return;

        this.answered = true;
        const correct = selectedIndex === this.correctRenderedIndex;
        const buttons = this.optionsContainer.querySelectorAll('.option-btn');

        this.answers.push({ id: question.id, correct });

        track('question_answered', {
            id: question.id,
            correct,
            mode: this.mode,
            topic: this.topic,
            question_index: this.index + 1,
            total: this.questions.length,
        });

        if (correct) {
            this.score += 1;
            this.combo += 1;
            if (this.combo > this.maxCombo) this.maxCombo = this.combo;
            buttons[selectedIndex].classList.add('correct');
        } else {
            this.combo = 0;
            this.wrongQuestions.push(question);
            buttons[selectedIndex].classList.add('incorrect');
            buttons[this.correctRenderedIndex].classList.add('correct');
        }
        this.updateCombo();

        buttons.forEach((btn) => {
            btn.disabled = true;
        });

        // Exam Mode keeps it exam-like: no explanation until the end
        if (this.mode !== 'exam') {
            this.explanationEl.textContent = question.explanation;
            this.explanationEl.style.display = 'block';
            this.explanationEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        this.nextBtn.style.display = 'block';
    }

    handleNext() {
        if (!this.answered) return;

        if (this.index >= this.questions.length - 1) {
            this.complete();
            return;
        }

        this.index += 1;
        this.renderQuestion();
    }

    complete() {
        this.stopTimer();
        const total = this.questions.length;
        const percentage =
            total > 0 ? Math.round((this.score / total) * 100) : 0;

        saveProgress(percentage, this.answers, this.wrongQuestions);

        // Award XP
        const correctCount = this.score;
        const wrongCount   = this.wrongQuestions.length;
        addXP(correctCount, wrongCount);

        track('quiz_complete', {
            score: this.score,
            total,
            mode: this.mode,
            topic: this.topic,
            wrong_count: this.wrongQuestions.length,
        });

        showResults(
            this.score,
            this.wrongQuestions,
            this.mode,
            this.topic,
            this.questions.length
        );
        showScreen('result-screen');
    }
}

function startQuiz(mode, topic, questions = null) {
    const container = document.getElementById('quiz-screen');
    if (!container) return null;

    if (activeQuizController && typeof activeQuizController.stopTimer === 'function') {
        activeQuizController.stopTimer();
    }
    activeQuizController = new QuizController(container, mode, topic, questions);
    if (!activeQuizController.start()) {
        activeQuizController = null;
        return null;
    }
    return activeQuizController;
}

function goHome() {
    if (activeQuizController && typeof activeQuizController.stopTimer === 'function') {
        activeQuizController.stopTimer();
    }
    activeQuizController = null;
    const startScreen = document.getElementById('start-screen');
    if (startScreen) {
        showScreen('start-screen');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
    }
    window.location.href = '/';
}

function updateHomeNav() {
    const btn = document.getElementById('home-nav-btn');
    if (!btn) return;

    const startScreen = document.getElementById('start-screen');
    if (!startScreen) {
        btn.hidden = true;
        return;
    }

    btn.hidden = startScreen.classList.contains('active');
}

function ensureHomeNav() {
    const header = document.querySelector('body > header .site-header__top, body > header .container');
    if (!header || document.getElementById('home-nav-btn')) return;
    if (!document.getElementById('start-screen')) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'home-nav-btn';
    btn.className = 'home-nav-btn';
    btn.textContent = '← Home';
    btn.hidden = true;
    btn.setAttribute('aria-label', 'Back to home');
    btn.addEventListener('click', goHome);
    header.insertBefore(btn, header.firstChild);
}

function closeSiteNav(header) {
    header.classList.remove('nav-open');
    document.body.classList.remove('nav-menu-open');
    const toggle = header.querySelector('.nav-toggle');
    if (toggle) {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = 'Menu';
    }
}

function bindSiteNav(header) {
    const toggle = header.querySelector('.nav-toggle');
    if (!toggle || toggle.dataset.bound) return;
    toggle.dataset.bound = '1';

    toggle.addEventListener('click', () => {
        if (header.classList.contains('nav-open')) {
            closeSiteNav(header);
        } else {
            header.classList.add('nav-open');
            document.body.classList.add('nav-menu-open');
            toggle.setAttribute('aria-expanded', 'true');
            toggle.textContent = 'Close';
        }
    });

    header.querySelectorAll('.secondary-nav a').forEach((link) => {
        link.addEventListener('click', () => closeSiteNav(header));
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && header.classList.contains('nav-open')) {
            closeSiteNav(header);
        }
    });
}

function initNav() {
    const header = document.querySelector('body > header');
    if (!header) return;
    const secondary = header.querySelector('.secondary-nav');

    if (secondary && !secondary.querySelector('a[href="/"], a[href="index.html"], a[href="/index.html"]')) {
        const home = document.createElement('a');
        home.href = '/';
        home.className = 'nav-link';
        home.textContent = 'Practice Test';
        secondary.insertBefore(home, secondary.firstChild);
    }

    const path = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '') || '/';
    header.querySelectorAll('.secondary-nav .nav-link.state-link').forEach((a) => {
        const href = a.getAttribute('href');
        if (!href) return;
        let norm = href.replace(/index\.html$/, '');
        if (norm.endsWith('/')) norm = norm.slice(0, -1) || '/';
        if (norm === path || (path.endsWith('.html') && norm === path)) {
            a.setAttribute('aria-current', 'page');
        } else {
            a.removeAttribute('aria-current');
        }
    });

    bindSiteNav(header);
}

function setQuizChrome(isQuiz) {
    document.body.classList.toggle('is-quiz-active', isQuiz);
    const aff = document.getElementById('affiliate-box');
    if (aff) aff.hidden = isQuiz;
    const hero = document.querySelector('.home-editorial-hero');
    if (hero) hero.hidden = isQuiz;
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    setQuizChrome(screenId === 'quiz-screen');
    updateHomeNav();
}


// Google Consent Mode update helper
function onUserAcceptsCookies() {
    if (typeof gtag === "function") {
        gtag("consent", "update", {
            "ad_storage": "granted",
            "ad_user_data": "granted",
            "ad_personalization": "granted",
            "analytics_storage": "granted"
        });
    }
    if (window.dataLayer) {
        window.dataLayer.push({ event: "consent_update" });
    }
}

// ─── FONT RESIZE ─────────────────────────────────────────────────────────────
const FONT_KEY   = 'fs_font_size_v1';
const FONT_SIZES = [14, 16, 18, 20, 22]; // px
const FONT_DEFAULT_IDX = 1;

function applyFontSize(idx) {
    document.documentElement.style.fontSize = FONT_SIZES[idx] + 'px';
    try { localStorage.setItem(FONT_KEY, String(idx)); } catch {}
}

function initFontResize() {
    let idx;
    try { idx = parseInt(localStorage.getItem(FONT_KEY) ?? '', 10); } catch {}
    if (isNaN(idx) || idx < 0 || idx >= FONT_SIZES.length) idx = FONT_DEFAULT_IDX;
    applyFontSize(idx);

    const dec = document.getElementById('font-decrease');
    const inc = document.getElementById('font-increase');
    if (!dec || !inc) return;
    if (dec.dataset.fontBound) return; // guard: avoid double-binding when site-ui.js also loads
    dec.dataset.fontBound = '1';

    dec.addEventListener('click', () => {
        let i = FONT_SIZES.indexOf(parseInt(document.documentElement.style.fontSize, 10));
        if (i < 0) i = FONT_DEFAULT_IDX;
        applyFontSize(Math.max(0, i - 1));
    });
    inc.addEventListener('click', () => {
        let i = FONT_SIZES.indexOf(parseInt(document.documentElement.style.fontSize, 10));
        if (i < 0) i = FONT_DEFAULT_IDX;
        applyFontSize(Math.min(FONT_SIZES.length - 1, i + 1));
    });
}

// ─── STUDY FEATURES (bookmarks · text-to-speech · progress · flashcards) ──────

const BOOKMARKS_KEY = 'fs_bookmarks_v1';

function loadBookmarks() {
    try { return JSON.parse(localStorage.getItem(BOOKMARKS_KEY)) || []; }
    catch { return []; }
}
function saveBookmarks(arr) {
    try { localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(arr)); } catch {}
}
function toggleBookmark(id) {
    const arr = loadBookmarks();
    const i = arr.indexOf(id);
    if (i >= 0) arr.splice(i, 1); else arr.push(id);
    saveBookmarks(arr);
    return arr.includes(id);
}

function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    try {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-AU';
        u.rate = 0.95;
        window.speechSynthesis.speak(u);
    } catch {}
}

function esc(str) {
    return String(str).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function initProgressPage() {
    const el = document.getElementById('progress-app');
    if (!el) return;

    const g = loadGamify();
    const p = loadProgress();
    const best = getBestScore(p);
    const level = getLevel(g.xp || 0);
    const attempts = (p && Array.isArray(p.attempts)) ? p.attempts : [];
    const weak = getWeakQuestions().length;
    const avg = attempts.length
        ? Math.round(attempts.reduce((s, a) => s + (a.percentage || 0), 0) / attempts.length)
        : 0;

    let band, colour;
    if (best >= 80) { band = "Exam-ready"; colour = 'var(--green)'; }
    else if (best >= 50) { band = "Getting there"; colour = 'var(--amber, #C9852B)'; }
    else { band = "Keep practising"; colour = 'var(--red)'; }

    if (attempts.length === 0) {
        el.innerHTML = `<div class="progress-empty">
            <p>No attempts yet. Your XP, streak, best score and exam-readiness will appear here once you start practising.</p>
            <p style="margin-top:14px;"><a class="btn btn-primary" href="/">Start your first test →</a></p>
        </div>`;
        return;
    }

    const recent = attempts.slice(-8).reverse().map((a) => {
        const d = a.at ? new Date(a.at).toLocaleDateString('en-AU', { day: 'numeric', month: 'short' }) : '';
        return `<div class="review-item"><span class="rq">${a.percentage}%</span> <span class="re">${d}</span></div>`;
    }).join('');

    el.innerHTML = `
        <div class="readiness-card">
            <p style="color:var(--muted);font-weight:700;margin-bottom:2px;">Exam readiness</p>
            <p class="readiness-label" style="color:${colour};font-size:1.4rem;">${band}</p>
            <div class="readiness-track"><div class="readiness-fill" style="width:${best}%;background:${colour};"></div></div>
            <p style="color:var(--muted);font-size:.85rem;">Based on your best score of ${best}%. Aim for 80%+.</p>
        </div>
        <div class="progress-grid">
            <div class="progress-stat"><div class="v">${(g.xp || 0).toLocaleString()}</div><div class="l">XP · ${level.label}</div></div>
            <div class="progress-stat"><div class="v">${g.streak || 0}</div><div class="l">Day streak</div></div>
            <div class="progress-stat"><div class="v">${best}%</div><div class="l">Best score</div></div>
            <div class="progress-stat"><div class="v">${avg}%</div><div class="l">Average score</div></div>
            <div class="progress-stat"><div class="v">${attempts.length}</div><div class="l">Tests taken</div></div>
            <div class="progress-stat"><div class="v">${weak}</div><div class="l">Weak questions</div></div>
        </div>
        <h3 style="margin:8px 0 12px;">Recent attempts</h3>
        ${recent}
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;">
            <a class="btn btn-primary" href="/">Take another test →</a>
            ${weak > 0 ? '<a class="btn btn-secondary" href="/?mode=review">Review weak questions</a>' : ''}
            <a class="btn btn-secondary" href="/bookmarks.html">View bookmarks</a>
            <a class="btn btn-secondary" href="/progress.html">Full progress</a>
        </div>`;
}

function renderReviewList(el, questions, emptyMsg, withRemove) {
    if (!questions.length) {
        el.innerHTML = `<div class="feature-empty">${emptyMsg}</div>`;
        return;
    }
    el.innerHTML = questions.map((q) => `
        <div class="review-item" data-id="${q.id}">
            <p class="rq">${esc(q.question)}</p>
            <p class="ra"><strong>Answer:</strong> ${esc(q.options[q.answer])}</p>
            <p class="re">${esc(q.explanation || '')}</p>
            ${withRemove ? '<button type="button" class="review-remove">Remove bookmark</button>' : ''}
        </div>`).join('');

    if (withRemove) {
        el.querySelectorAll('.review-remove').forEach((btn) => {
            btn.addEventListener('click', () => {
                const item = btn.closest('.review-item');
                toggleBookmark(item.dataset.id);
                item.remove();
                if (!el.querySelector('.review-item')) {
                    el.innerHTML = `<div class="feature-empty">${emptyMsg}</div>`;
                }
            });
        });
    }
}

function initBookmarksPage() {
    const el = document.getElementById('bookmarks-app');
    if (!el) return;
    const ids = loadBookmarks();
    const qs = QUESTIONS.filter((q) => ids.includes(q.id));
    renderReviewList(el, qs,
        'No bookmarks yet. Tap Bookmark on any question during a test to save it here for later review.',
        true);
}

function initFlashcards() {
    const el = document.getElementById('flashcards-app');
    if (!el) return;

    let order = shuffle(QUESTIONS);
    let idx = 0;
    let flipped = false;

    function render() {
        const q = order[idx];
        const saved = loadBookmarks().includes(q.id);
        el.innerHTML = `
            <div class="flashcard" role="button" tabindex="0" aria-label="Tap to flip">
                <p class="flashcard__hint">${flipped ? 'Answer' : 'Question. Tap to flip'}</p>
                <p class="flashcard__q">${esc(q.question)}</p>
                ${flipped ? `<div class="flashcard__a">
                    <p class="flashcard__answer"><strong>Answer:</strong> ${esc(q.options[q.answer])}</p>
                    <p class="flashcard__exp">${esc(q.explanation || '')}</p>
                </div>` : ''}
            </div>
            <div class="flashcard-controls">
                <button type="button" class="btn btn-secondary" data-act="prev">← Previous</button>
                <button type="button" class="btn btn-primary" data-act="flip">${flipped ? 'Hide answer' : 'Show answer'}</button>
                <button type="button" class="btn btn-secondary" data-act="next">Next →</button>
            </div>
            <div class="flashcard-controls">
                <button type="button" class="q-tool q-tts" data-act="tts">Read aloud</button>
                <button type="button" class="q-tool q-bookmark ${saved ? 'is-on' : ''}" data-act="bm">${saved ? 'Saved' : 'Bookmark'}</button>
                <button type="button" class="q-tool" data-act="shuffle">Shuffle</button>
            </div>
            <p class="flashcard-meta">Card ${idx + 1} of ${order.length}</p>`;

        el.querySelector('.flashcard').addEventListener('click', () => { flipped = !flipped; render(); });
        el.querySelectorAll('[data-act]').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const act = btn.dataset.act;
                if (act === 'prev') { idx = (idx - 1 + order.length) % order.length; flipped = false; render(); }
                else if (act === 'next') { idx = (idx + 1) % order.length; flipped = false; render(); }
                else if (act === 'flip') { flipped = !flipped; render(); }
                else if (act === 'shuffle') { order = shuffle(QUESTIONS); idx = 0; flipped = false; render(); }
                else if (act === 'tts') { speakText(`${q.question}. The answer is: ${q.options[q.answer]}. ${q.explanation || ''}`); }
                else if (act === 'bm') { toggleBookmark(q.id); render(); }
            });
        });
    }
    render();
}

// ─── KEYBOARD CONTROLS (answer A–D / 1–4, Enter or → for next) ────────────────
function initQuizKeyboard() {
    document.addEventListener('keydown', (e) => {
        const quizScreen = document.getElementById('quiz-screen');
        if (!quizScreen || !quizScreen.classList.contains('active')) return;
        if (!activeQuizController) return;
        const tag = (e.target.tagName || '').toLowerCase();
        if (tag === 'input' || tag === 'textarea') return;

        const ctrl = activeQuizController;
        const map = { a: 0, b: 1, c: 2, d: 3, e: 4, f: 5, '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5 };
        const key = e.key.toLowerCase();

        if (!ctrl.answered && Object.prototype.hasOwnProperty.call(map, key)) {
            const opts = ctrl.optionsContainer.querySelectorAll('.option-btn');
            if (opts[map[key]]) { e.preventDefault(); opts[map[key]].click(); }
        } else if (ctrl.answered && (e.key === 'Enter' || e.key === 'ArrowRight')) {
            if (ctrl.nextBtn && ctrl.nextBtn.style.display !== 'none') { e.preventDefault(); ctrl.nextBtn.click(); }
        }
    });
}

function onDomReady(fn) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fn);
    } else {
        fn();
    }
}

// Event Listeners
onDomReady(() => {
    // Apply SEO on load
    applySEO();

    initTheme();
    initQuizKeyboard();
    initFontResize();
    initNav();
    ensureHomeNav();
    updateHomeNav();
    mountModeSelection();
    mountGamificationDashboard();
    mountDailyChallenge();
    initProgressPage();
    initBookmarksPage();
    initFlashcards();

    // Auto-start only when mode/topic are in the URL (e.g. from topic pages)
    if (location.search.includes('mode=') || location.search.includes('topic=')) {
        const { mode, topic } = getQuizConfig();
        selectMode(mode, topic);
    }

    // Cookie banner handled by cookie-consent.js

});

