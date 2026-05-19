import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Research Pipeline",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #0a0a0a;
    --surface:  #111111;
    --card:     #1a1a1a;
    --border:   #2e2e2e;
    --accent:   #6366f1;
    --blue:     #38bdf8;
    --purple:   #a78bfa;
    --orange:   #fb923c;
    --green:    #4ade80;
    --text:     #f5f5f5;
    --muted:    #888888;
    --danger:   #f87171;
}

html, body, .stApp { background: var(--bg) !important; color: var(--text) !important; font-family: 'Syne', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1200px; }
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ---- Hero ---- */
.hero { margin-bottom: 2.5rem; }
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 400;
    color: var(--accent); letter-spacing: 0.2em;
    text-transform: uppercase; margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 3rem; font-weight: 800; line-height: 1;
    color: var(--text); letter-spacing: -2px; margin-bottom: 0.5rem;
}
.hero-title span { color: var(--accent); }
.hero-sub { color: var(--muted); font-size: 0.9rem; font-weight: 400; }

/* ---- Pipeline tracker ---- */
.pipeline {
    display: flex; gap: 0; margin-bottom: 2rem;
    border: 1px solid var(--border); border-radius: 12px; overflow: hidden;
    background: var(--surface);
}
.pipe-step {
    flex: 1; padding: 0.9rem 1rem; text-align: center;
    border-right: 1px solid var(--border); position: relative;
}
.pipe-step:last-child { border-right: none; }
.pipe-step.idle   { background: #161616; }
.pipe-step.active { background: #1e1b4b; border-bottom: 3px solid var(--accent); }
.pipe-step.done   { background: #052e16; border-bottom: 3px solid var(--green); }
.pipe-icon { font-size: 1.2rem; margin-bottom: 0.2rem; }
.pipe-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--muted);
}
.pipe-step.active .pipe-label { color: #a5b4fc; font-weight: 600; }
.pipe-step.done   .pipe-label { color: var(--green); font-weight: 600; }

/* ---- Input area ---- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
.stTextInput label, .stTextArea label { display: none; }

/* ---- Buttons ---- */
.stButton > button {
    background: var(--accent) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 2rem !important;
    letter-spacing: 0.04em;
    width: 100%;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #4f46e5 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(99,102,241,0.35) !important;
}

/* ---- Result cards ---- */
.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.result-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
}
.result-card.search  { border-color: #1e3a5f; background: #0d1f33; }
.result-card.reader  { border-color: #2e1a4a; background: #150d2a; }
.result-card.writer  { border-color: #4a2410; background: #271208; }
.result-card.critic  { border-color: #0f3320; background: #071a10; }
.result-card.search::before  { background: var(--blue); }
.result-card.reader::before  { background: var(--purple); }
.result-card.writer::before  { background: var(--orange); }
.result-card.critic::before  { background: var(--green); }

.result-card-header {
    display: flex; align-items: center; gap: 0.6rem;
    margin-bottom: 0.8rem;
}
.result-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px;
}
.badge-search { background: #0369a1; color: #e0f2fe; }
.badge-reader { background: #5b21b6; color: #ede9fe; }
.badge-writer { background: #9a3412; color: #ffedd5; }
.badge-critic { background: #15803d; color: #dcfce7; }

.result-card-title { font-size: 0.9rem; font-weight: 700; color: #f5f5f5; }
.result-card-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; line-height: 1.7;
    color: #d1d5db;
    white-space: pre-wrap; word-break: break-word;
    max-height: 320px; overflow-y: auto;
}
.result-card-body::-webkit-scrollbar { width: 4px; }
.result-card-body::-webkit-scrollbar-track { background: transparent; }
.result-card-body::-webkit-scrollbar-thumb { background: #404040; border-radius: 4px; }

/* ---- Metrics ---- */
.metrics-row { display: flex; gap: 0.75rem; margin-top: 1.5rem; flex-wrap: wrap; }
.metric-pill {
    background: #1a1a1a; border: 1px solid #2e2e2e;
    border-radius: 50px; padding: 0.45rem 1rem;
    display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
}
.metric-pill-label { color: #888; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-pill-value { color: #f5f5f5; font-weight: 700; margin-left: 0.2rem; }

/* ---- Section header ---- */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.15em;
    text-transform: uppercase; color: #888;
    margin-bottom: 0.75rem; margin-top: 1.5rem;
}

/* ---- History sidebar ---- */
.history-entry {
    background: #1a1a1a; border: 1px solid #2e2e2e;
    border-radius: 8px; padding: 0.65rem 0.85rem;
    margin-bottom: 0.5rem; font-size: 0.8rem;
}
.history-topic { color: #f5f5f5; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.history-time { color: #888; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; margin-top: 0.2rem; }

.divider { border: none; border-top: 1px solid #2e2e2e; margin: 1.5rem 0; }

.streamlit-expanderHeader {
    background: #1a1a1a !important; border: 1px solid #2e2e2e !important;
    border-radius: 8px !important; color: #888 !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []
if "active_step" not in st.session_state:
    st.session_state.active_step = -1

STEPS = [
    {"icon": "🔍", "label": "Search Agent"},
    {"icon": "📄", "label": "Reader Agent"},
    {"icon": "✍️", "label": "Writer Chain"},
    {"icon": "🧐", "label": "Critic Chain"},
]

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; letter-spacing:0.15em;
         text-transform:uppercase; color:#a5b4fc; margin-bottom:1.5rem; font-weight:700;">
        ⚙ Control Panel
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Quick Topics</div>', unsafe_allow_html=True)
    quick_topics = [
        "Artificial General Intelligence 2025",
        "Quantum Computing breakthroughs",
        "Climate change latest research",
        "Large Language Models architecture",
    ]
    selected_quick = None
    for topic in quick_topics:
        if st.button(topic[:36] + ("…" if len(topic) > 36 else ""), key=f"qt_{topic[:8]}"):
            selected_quick = topic

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Run History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for h in reversed(st.session_state.history[-6:]):
            st.markdown(f"""
            <div class="history-entry">
                <div class="history-topic">{h['topic'][:38]}</div>
                <div class="history-time">{h['time']} · {h['duration']}s</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#555860; font-size:0.8rem; font-family:\'JetBrains Mono\',monospace;">No runs yet.</div>', unsafe_allow_html=True)

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">📡 Multi-Agent Research System</div>
    <div class="hero-title">Research<span>.</span><br>Synthesized<span>.</span></div>
    <div class="hero-sub">Search → Scrape → Write → Critique — fully automated.</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PIPELINE TRACKER
# ==========================================

def render_pipeline_tracker(active: int):
    html = '<div class="pipeline">'
    for i, step in enumerate(STEPS):
        if active == -1:
            cls = "idle"
        elif i < active:
            cls = "done"
        elif i == active:
            cls = "active"
        else:
            cls = "idle"
        html += f'<div class="pipe-step {cls}"><div class="pipe-icon">{step["icon"]}</div><div class="pipe-label">{step["label"]}</div></div>'
    html += "</div>"
    return html

tracker_slot = st.empty()
tracker_slot.markdown(render_pipeline_tracker(-1), unsafe_allow_html=True)

# ==========================================
# INPUT
# ==========================================

col_in, col_btn = st.columns([5, 1])
with col_in:
    topic = st.text_input(
        "topic",
        value=selected_quick or "",
        placeholder="Enter a research topic — e.g. 'Quantum computing in 2025'",
        label_visibility="collapsed"
    )
with col_btn:
    run_btn = st.button("▶  Run")

# ==========================================
# HELPERS
# ==========================================

def render_step_card(card_type, title, content, loading=False):
    badges = {
        "search": ("badge-search", "Search Agent"),
        "reader": ("badge-reader", "Reader Agent"),
        "writer": ("badge-writer", "Writer Chain"),
        "critic": ("badge-critic", "Critic Chain"),
    }
    badge_cls, badge_label = badges.get(card_type, ("", ""))
    body = "<em style='color:#555;'>⏳ Running…</em>" if loading else (content or "—")
    st.markdown(f"""
    <div class="result-card {card_type}">
        <div class="result-card-header">
            <span class="result-badge {badge_cls}">{badge_label}</span>
            <span class="result-card-title">{title}</span>
        </div>
        <div class="result-card-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PIPELINE RUN
# ==========================================

st.markdown('<hr class="divider">', unsafe_allow_html=True)

if run_btn and topic.strip():
    import datetime

    st.markdown('<div class="section-header">Pipeline Output</div>', unsafe_allow_html=True)
    s1 = st.empty()
    s2 = st.empty()
    s3 = st.empty()
    s4 = st.empty()
    metrics_slot = st.empty()

    state = {}
    start = time.time()

    try:
        # STEP 1 — Search
        tracker_slot.markdown(render_pipeline_tracker(0), unsafe_allow_html=True)
        with s1.container():
            render_step_card("search", "Search Agent", None, loading=True)

        search_agent = build_search_agent()
        res = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = res['messages'][-1].content
        with s1.container():
            render_step_card("search", "Search Agent", state["search_results"])

        # STEP 2 — Reader
        tracker_slot.markdown(render_pipeline_tracker(1), unsafe_allow_html=True)
        with s2.container():
            render_step_card("reader", "Reader Agent", None, loading=True)

        reader_agent = build_reader_agent()
        res = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = res['messages'][-1].content
        with s2.container():
            render_step_card("reader", "Reader Agent", state["scraped_content"])

        # STEP 3 — Writer
        tracker_slot.markdown(render_pipeline_tracker(2), unsafe_allow_html=True)
        with s3.container():
            render_step_card("writer", "Writer Chain", None, loading=True)

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        with s3.container():
            render_step_card("writer", "Writer Chain", str(state["report"]))

        # STEP 4 — Critic
        tracker_slot.markdown(render_pipeline_tracker(3), unsafe_allow_html=True)
        with s4.container():
            render_step_card("critic", "Critic Chain", None, loading=True)

        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        with s4.container():
            render_step_card("critic", "Critic Chain", str(state["feedback"]))

        # All done
        tracker_slot.markdown(render_pipeline_tracker(4), unsafe_allow_html=True)
        duration = round(time.time() - start, 1)

        st.session_state.history.append({
            "topic": topic,
            "time": datetime.datetime.now().strftime("%H:%M"),
            "duration": duration
        })

        metrics_slot.markdown(f"""
        <div class="metrics-row">
            <div class="metric-pill">⏱ <span class="metric-pill-label">Duration</span><span class="metric-pill-value">{duration}s</span></div>
            <div class="metric-pill">🔍 <span class="metric-pill-label">Search</span><span class="metric-pill-value">{len(state['search_results'])} chars</span></div>
            <div class="metric-pill">📄 <span class="metric-pill-label">Scraped</span><span class="metric-pill-value">{len(state['scraped_content'])} chars</span></div>
            <div class="metric-pill">✅ <span class="metric-pill-label">Status</span><span class="metric-pill-value" style="color:var(--green)">Complete</span></div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📦 Raw Pipeline State"):
            st.json({
                "search_results": state["search_results"][:600] + "…",
                "scraped_content": state["scraped_content"][:600] + "…",
                "report": str(state["report"])[:600] + "…",
                "feedback": str(state["feedback"])[:600] + "…",
            })

    except Exception as e:
        st.markdown(f"""
        <div style="background:#2d0a0a; border:1px solid #7f1d1d;
             border-radius:10px; padding:1.2rem; color:#fca5a5;
             font-family:'JetBrains Mono',monospace; font-size:0.82rem;">
            ❌ Pipeline Error: {str(e)}
        </div>
        """, unsafe_allow_html=True)

elif run_btn:
    st.markdown("""
    <div style="background:#1c1200; border:1px solid #854d0e;
         border-radius:10px; padding:1rem; color:#fcd34d;
         font-family:'JetBrains Mono',monospace; font-size:0.82rem;">
        ⚠ Please enter a research topic first.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style="text-align:center; margin-top:4rem; padding-top:1.5rem;
     border-top:1px solid #2e2e2e;
     font-family:'JetBrains Mono',monospace; font-size:0.6rem;
     letter-spacing:0.15em; color:#444; text-transform:uppercase;">
    SEARCH · SCRAPE · WRITE · CRITIQUE — AGENTIX RESEARCH PIPELINE
</div>
""", unsafe_allow_html=True)