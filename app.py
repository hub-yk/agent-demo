import streamlit as st
from datetime import datetime
from urllib.parse import quote

st.set_page_config(
    page_title="소비데이터 기반 식습관 교정 Agent",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Design CSS
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }
    .hero {
        padding: 30px 34px;
        border-radius: 28px;
        background: linear-gradient(135deg, #0f766e 0%, #16a34a 48%, #84cc16 100%);
        color: white;
        box-shadow: 0 18px 42px rgba(15, 118, 110, 0.24);
        margin-bottom: 22px;
    }
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 2.3rem;
        line-height: 1.18;
        letter-spacing: -0.04em;
    }
    .hero p {
        margin: 0;
        font-size: 1.02rem;
        opacity: 0.95;
    }
    .badge-row { margin-top: 16px; }
    .badge {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px 6px 0 0;
        border-radius: 999px;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.24);
        color: white;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .notice {
        padding: 15px 18px;
        border-radius: 18px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #334155;
        margin-bottom: 16px;
    }
    .card {
        padding: 20px 22px;
        border-radius: 24px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 26px rgba(15, 23, 42, 0.06);
        margin-bottom: 16px;
    }
    .card h3 {
        margin-top: 0;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
    }
    .mini-card {
        padding: 16px;
        border-radius: 20px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    .mini-card .label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .mini-card .value {
        color: #0f172a;
        font-size: 1.35rem;
        font-weight: 800;
        margin-top: 4px;
    }
    .level-high {
        padding: 18px;
        border-radius: 22px;
        background: linear-gradient(135deg, #fef2f2, #fff7ed);
        border: 1px solid #fecaca;
        color: #991b1b;
        font-weight: 800;
    }
    .level-medium {
        padding: 18px;
        border-radius: 22px;
        background: linear-gradient(135deg, #fffbeb, #fff7ed);
        border: 1px solid #fed7aa;
        color: #92400e;
        font-weight: 800;
    }
    .level-low {
        padding: 18px;
        border-radius: 22px;
        background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
        border: 1px solid #bbf7d0;
        color: #166534;
        font-weight: 800;
    }
    .flow {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 14px 0 6px 0;
    }
    .flow-step {
        flex: 1 1 150px;
        padding: 14px;
        text-align: center;
        border-radius: 18px;
        background: #f0fdfa;
        border: 1px solid #ccfbf1;
        color: #0f766e;
        font-weight: 800;
    }
    .pill {
        display: inline-block;
        padding: 7px 11px;
        margin: 4px 4px 4px 0;
        border-radius: 999px;
        background: #ecfeff;
        border: 1px solid #a5f3fc;
        color: #0e7490;
        font-size: 0.84rem;
        font-weight: 800;
    }
    .cart-item {
        padding: 12px 14px;
        border-radius: 15px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .summary-box {
        padding: 22px 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%);
        border: 1px solid #bfdbfe;
        font-size: 1.05rem;
        font-weight: 800;
        color: #1e3a8a;
        line-height: 1.65;
    }
    .small-muted { color: #64748b; font-size: 0.9rem; }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }
    .stButton>button {
        border-radius: 14px;
        font-weight: 800;
        border: 0;
        background: linear-gradient(135deg, #0f766e, #16a34a);
        color: white;
    }
    .stLinkButton>a {
        border-radius: 14px;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Demo data and rules
# -----------------------------
SCENARIOS = {
    "A. 야식·고지방·채소부족형 (High)": {
        "delivery_count": 6,
        "cafe_count": 7,
        "convenience_count": 5,
        "late_count": 5,
        "high_fat_count": 6,
        "veg_count": 1,
        "exercise": "NO",
        "rejections": 2,
    },
    "B. 카페·당류 과다형 (Medium)": {
        "delivery_count": 3,
        "cafe_count": 10,
        "convenience_count": 3,
        "late_count": 2,
        "high_fat_count": 2,
        "veg_count": 2,
        "exercise": "NO",
        "rejections": 1,
    },
    "C. 균형 유지형 (Low)": {
        "delivery_count": 1,
        "cafe_count": 2,
        "convenience_count": 1,
        "late_count": 0,
        "high_fat_count": 1,
        "veg_count": 5,
        "exercise": "YES",
        "rejections": 0,
    },
}

LEVEL_STYLE = {
    "High": ("🚨 High", "level-high", "강한 개입 필요"),
    "Medium": ("⚠️ Medium", "level-medium", "부분 개입 필요"),
    "Low": ("✅ Low", "level-low", "유지·모니터링"),
}


def yn(condition: bool) -> str:
    return "YES" if condition else "NO"


def to_features(data: dict) -> dict:
    return {
        "LATE_EAT": yn(data["late_count"] >= 3),
        "HIGH_FAT": yn(data["high_fat_count"] >= 4),
        "VEG_LOW": yn(data["veg_count"] <= 2),
        "EXERCISE": data["exercise"],
        "ORDER_FREQ": "HIGH" if data["delivery_count"] >= 4 else "LOW",
        "SUGAR_HIGH": yn(data["cafe_count"] >= 6),
        "CONVENIENCE_HIGH": yn(data["convenience_count"] >= 4),
    }


def id3_decision(features: dict) -> tuple[str, str, list[str]]:
    path = []
    path.append(f"Root: LATE_EAT = {features['LATE_EAT']}")
    if features["LATE_EAT"] == "YES":
        path.append(f"→ HIGH_FAT = {features['HIGH_FAT']}")
        if features["HIGH_FAT"] == "YES":
            path.append(f"→ VEG_LOW = {features['VEG_LOW']}")
            if features["VEG_LOW"] == "YES":
                return "High", "야식·고지방·채소부족이 동시에 나타나는 강한 개입 필요 유형", path
            return "Medium", "야식과 고지방은 있으나 채소 섭취는 일부 유지되는 조정 필요 유형", path
        path.append(f"→ VEG_LOW = {features['VEG_LOW']}")
        if features["VEG_LOW"] == "YES":
            return "Medium", "야식은 있으나 고지방은 낮고 채소 섭취가 부족한 대체식 필요 유형", path
        return "Low", "야식은 있으나 전반적 식단 균형은 유지되는 관찰 유형", path
    path.append(f"→ EXERCISE = {features['EXERCISE']}")
    if features["EXERCISE"] == "NO":
        path.append(f"→ VEG_LOW = {features['VEG_LOW']}")
        if features["VEG_LOW"] == "YES":
            return "Medium", "야식은 적지만 운동·채소 섭취가 부족한 생활 조정 필요 유형", path
        return "Low", "운동은 부족하지만 식습관 위험은 낮은 유지·관찰 유형", path
    return "Low", "운동과 식습관 균형이 비교적 유지되는 유형", path


def agent_actions(level: str, features: dict, rejections: int) -> dict:
    if level == "High":
        title = "건강식 장바구니 + 주문 연결"
        goal = "이번 주 배달/야식 2회 줄이고, 단백질·채소 기반 식사 3회 확보"
        cart = ["닭가슴살 또는 두부 3팩", "샐러드 채소/쌈채소 2종", "현미밥 또는 잡곡밥 3개", "무가당 그릭요거트", "저염 닭가슴살 샐러드/포케 메뉴"]
        menu = ["닭가슴살 포케", "연어 샐러드", "두부 샐러드볼", "현미 도시락"]
    elif level == "Medium":
        title = "덜 나쁜 대체식 + 식단 조정"
        goal = "현재 소비패턴을 급격히 바꾸지 않고, 카페·배달 선택을 더 나은 대안으로 교체"
        cart = ["무가당 두유 또는 저당 요거트", "삶은 달걀/단백질 간식", "견과류 소포장", "샐러드 키트 1~2개"]
        menu = ["샐러드+단백질 추가", "쌀국수/국밥 소량", "저당 음료", "구운 치킨 샐러드"]
    else:
        title = "모니터링 + 작은 개선"
        goal = "현재 패턴을 유지하면서 주 1회 건강식 장보기 루틴 확보"
        cart = ["제철 과일", "채소 믹스", "단백질 간편식", "무가당 음료"]
        menu = ["균형식 도시락", "샐러드볼", "단백질 추가 메뉴"]

    if rejections >= 2:
        feedback = "최근 건강식 추천 거절이 누적되어, 완벽한 건강식 대신 ‘덜 나쁜 대체식’ 중심으로 전략을 완화합니다."
        strategy = "Persona 업데이트: 가격·선호도·귀찮음 장벽을 반영하여 실행 난이도를 낮춤"
    elif rejections == 1:
        feedback = "이전 추천 1회 거절 기록이 있어, 기존 추천보다 선택지를 2개 이상 제시합니다."
        strategy = "Persona 업데이트: 단일 추천보다 선택형 대안을 제공"
    else:
        feedback = "거절 데이터가 없어 기본 건강식 개입 전략을 적용합니다."
        strategy = "초기 Persona: 소비패턴 기반 기본 전략"

    return {"title": title, "goal": goal, "cart": cart, "menu": menu, "feedback": feedback, "strategy": strategy}


def search_link(platform: str, keyword: str) -> str:
    q = quote(keyword)
    if platform == "쿠팡":
        return f"https://www.coupang.com/np/search?q={q}"
    if platform == "마켓컬리":
        return f"https://www.kurly.com/search?sword={q}"
    if platform == "배민":
        return f"https://www.baemin.com/search/{q}"
    return f"https://www.google.com/search?q={q}"


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🥗 소비데이터 기반 식습관 교정 Agent</h1>
        <p>가상 카드소비 데이터 → ID3 판단 → Agentic AI 실행 연결 → Feedback Loop</p>
        <div class="badge-row">
            <span class="badge">Agentic AI</span>
            <span class="badge">ID3 Decision Tree</span>
            <span class="badge">Behavior Change</span>
            <span class="badge">Feedback Loop</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">
        <b>⚠️ 데모 안내</b><br>
        이 화면은 의료 진단이 아니라, <b>가상 소비데이터</b>를 바탕으로 식습관 패턴과 행동 개입 구조를 보여주는 발표용 프로토타입입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flow">
        <div class="flow-step">① 소비데이터</div>
        <div class="flow-step">② ID3 판단</div>
        <div class="flow-step">③ Agent 실행</div>
        <div class="flow-step">④ 피드백 학습</div>
        <div class="flow-step">⑤ 행동 변화</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar input
# -----------------------------
st.sidebar.title("🎛️ 데모 조작 패널")
st.sidebar.caption("시나리오를 선택하거나 슬라이더를 바꿔 결과 변화를 확인하세요.")
scenario = st.sidebar.selectbox("데모 시나리오", list(SCENARIOS.keys()))
base = SCENARIOS[scenario]

st.sidebar.markdown("---")
delivery_count = st.sidebar.slider("배달/외식 결제", 0, 10, base["delivery_count"])
cafe_count = st.sidebar.slider("카페/디저트 결제", 0, 14, base["cafe_count"])
convenience_count = st.sidebar.slider("편의점 식사 결제", 0, 10, base["convenience_count"])
late_count = st.sidebar.slider("밤 9시 이후 음식 결제", 0, 10, base["late_count"])
high_fat_count = st.sidebar.slider("튀김·패스트푸드·고지방", 0, 10, base["high_fat_count"])
veg_count = st.sidebar.slider("샐러드·채소·건강식", 0, 10, base["veg_count"])
exercise = st.sidebar.radio("운동/헬스장/웨어러블", ["YES", "NO"], index=0 if base["exercise"] == "YES" else 1, horizontal=True)
rejections = st.sidebar.slider("최근 추천 거절 횟수", 0, 5, base["rejections"])

if st.sidebar.button("🔄 기본 시나리오로 보기", use_container_width=True):
    st.rerun()

# Compute
data = {
    "delivery_count": delivery_count,
    "cafe_count": cafe_count,
    "convenience_count": convenience_count,
    "late_count": late_count,
    "high_fat_count": high_fat_count,
    "veg_count": veg_count,
    "exercise": exercise,
    "rejections": rejections,
}
features = to_features(data)
level, interpretation, path = id3_decision(features)
actions = agent_actions(level, features, rejections)
level_label, level_class, level_subtitle = LEVEL_STYLE[level]

# -----------------------------
# Main dashboard
# -----------------------------
left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="card"><h3>1) 가상 소비데이터 입력 결과</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("배달/외식", f"{delivery_count}회")
    c2.metric("카페/디저트", f"{cafe_count}회")
    c3.metric("야식", f"{late_count}회")
    c4, c5, c6 = st.columns(3)
    c4.metric("고지방", f"{high_fat_count}회")
    c5.metric("채소/건강식", f"{veg_count}회")
    c6.metric("운동 데이터", exercise)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>2) ID3 변수 변환</h3>', unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown(f'<div class="mini-card"><div class="label">LATE_EAT</div><div class="value">{features["LATE_EAT"]}</div></div>', unsafe_allow_html=True)
    p2.markdown(f'<div class="mini-card"><div class="label">HIGH_FAT</div><div class="value">{features["HIGH_FAT"]}</div></div>', unsafe_allow_html=True)
    p3.markdown(f'<div class="mini-card"><div class="label">VEG_LOW</div><div class="value">{features["VEG_LOW"]}</div></div>', unsafe_allow_html=True)
    p4.markdown(f'<div class="mini-card"><div class="label">EXERCISE</div><div class="value">{features["EXERCISE"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><h3>3) ID3 판단 결과</h3>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="{level_class}">{level_label} · {level_subtitle}<br><span style="font-size:0.92rem;font-weight:600;">{interpretation}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("**판단 경로**")
    for item in path:
        st.markdown(f'<span class="pill">{item}</span>', unsafe_allow_html=True)
    st.code("""LATE_EAT?
├─ YES → HIGH_FAT? → VEG_LOW? → High/Medium
└─ NO  → EXERCISE? → VEG_LOW? → Medium/Low""", language="text")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Agent execution
st.markdown('<div class="card"><h3>4) Agent 실행: 추천이 아니라 행동으로 연결</h3>', unsafe_allow_html=True)
exec1, exec2, exec3 = st.columns([0.9, 1.1, 1.1], gap="large")

with exec1:
    st.markdown(f"### 🎯 {actions['title']}")
    st.info(actions["goal"])
    st.markdown("**실행 전략**")
    st.markdown("- 사용자 확인 후 장바구니/주문 연결")
    st.markdown("- 거절 기록을 다음 추천에 반영")
    st.markdown("- 완벽한 식단보다 실행 가능한 대안 우선")

with exec2:
    st.markdown("### 🛒 Agent 장바구니")
    for item in actions["cart"]:
        st.markdown(f'<div class="cart-item">✅ {item}</div>', unsafe_allow_html=True)

with exec3:
    st.markdown("### 🔗 주문/구매 연결")
    for item in actions["cart"][:3]:
        col_a, col_b = st.columns(2)
        col_a.link_button("쿠팡 검색", search_link("쿠팡", item), use_container_width=True)
        col_b.link_button("마켓컬리 검색", search_link("마켓컬리", item), use_container_width=True)
    st.markdown("**배달앱 대체 메뉴**")
    for item in actions["menu"][:2]:
        st.link_button(f"배민: {item}", search_link("배민", item), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Feedback loop
fb1, fb2 = st.columns([1, 1], gap="large")
with fb1:
    st.markdown('<div class="card"><h3>5) Feedback Loop</h3>', unsafe_allow_html=True)
    st.markdown(f"**실패/성공 데이터 반영**  ")
    st.write(actions["feedback"])
    st.success(actions["strategy"])
    st.markdown('</div>', unsafe_allow_html=True)

with fb2:
    st.markdown('<div class="card"><h3>6) 사용자 반응 시뮬레이션</h3>', unsafe_allow_html=True)
    if "accepted" not in st.session_state:
        st.session_state.accepted = 0
    if "rejected" not in st.session_state:
        st.session_state.rejected = 0
    b1, b2 = st.columns(2)
    if b1.button("✅ 주문 연결 수락", use_container_width=True):
        st.session_state.accepted += 1
    if b2.button("❌ 추천 거절", use_container_width=True):
        st.session_state.rejected += 1
    m1, m2 = st.columns(2)
    m1.metric("수락", st.session_state.accepted)
    m2.metric("거절", st.session_state.rejected)
    if st.session_state.rejected >= 2:
        st.warning("거절 데이터가 누적되었습니다. 다음 추천은 ‘덜 나쁜 대체식’ 중심으로 조정됩니다.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="summary-box">
    발표용 한 줄 요약<br>
    이 시스템은 카드소비 데이터를 단순히 보여주는 앱이 아니라, ID3로 식습관 상태를 판단하고 Agentic AI가 장바구니·주문 연결까지 수행하는 행동 변화 Agent입니다.
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(f"Demo generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
