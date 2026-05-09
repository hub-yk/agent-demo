import streamlit as st
from datetime import datetime
from urllib.parse import quote

st.set_page_config(page_title="소비데이터 기반 식습관 교정 Agent", page_icon="🥗", layout="wide")

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


def yn(condition: bool) -> str:
    return "YES" if condition else "NO"


def to_features(data: dict) -> dict:
    """Convert fake card/payment records into ID3-ready YES/NO features."""
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
    """A compact ID3-like decision tree aligned with the presentation.
    The real ID3 training process is simplified for classroom demo purposes.
    """
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
    """Create behavior-change actions and feedback-loop strategy."""
    if level == "High":
        title = "강한 개입: 건강식 장바구니 + 주문 연결"
        goal = "이번 주 배달/야식 2회 줄이고, 단백질·채소 기반 식사 3회 확보"
        cart = [
            "닭가슴살 또는 두부 3팩",
            "샐러드 채소/쌈채소 2종",
            "현미밥 또는 잡곡밥 3개",
            "무가당 그릭요거트",
            "저염 닭가슴살 샐러드/포케 메뉴",
        ]
        menu = ["닭가슴살 포케", "연어 샐러드", "두부 샐러드볼", "현미 도시락"]
    elif level == "Medium":
        title = "부분 개입: 덜 나쁜 대체식 + 식단 조정"
        goal = "현재 소비패턴을 급격히 바꾸지 않고, 카페·배달 선택을 더 나은 대안으로 교체"
        cart = [
            "무가당 두유 또는 저당 요거트",
            "삶은 달걀/단백질 간식",
            "견과류 소포장",
            "샐러드 키트 1~2개",
        ]
        menu = ["샐러드+단백질 추가", "쌀국수/국밥 소량", "저당 음료", "구운 치킨 샐러드"]
    else:
        title = "유지 전략: 모니터링 + 작은 개선"
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
# UI
# -----------------------------
st.title("🥗 소비데이터 기반 식습관 교정 Agent")
st.caption("발표용 프로토타입 | 가상 카드소비 데이터 → ID3 판단 → Agentic AI 실행 연결")

with st.expander("⚠️ 데모 안내", expanded=True):
    st.write("이 데모는 의료 진단이 아니라, 가상 소비데이터를 바탕으로 식습관 패턴과 행동 개입 구조를 보여주는 발표용 프로토타입입니다.")

col_left, col_right = st.columns([0.95, 1.05])

with col_left:
    st.subheader("1) 가상 소비데이터 입력")
    scenario = st.selectbox("데모 시나리오 선택", list(SCENARIOS.keys()))
    base = SCENARIOS[scenario]

    st.write("카드·배달·식품 구매 기록이 아래와 같이 수집되었다고 가정합니다.")
    delivery_count = st.slider("주간 배달/외식 결제 횟수", 0, 10, base["delivery_count"])
    cafe_count = st.slider("주간 카페/디저트 결제 횟수", 0, 14, base["cafe_count"])
    convenience_count = st.slider("주간 편의점 식사 결제 횟수", 0, 10, base["convenience_count"])
    late_count = st.slider("밤 9시 이후 음식 결제 횟수", 0, 10, base["late_count"])
    high_fat_count = st.slider("튀김·패스트푸드·고지방 메뉴 결제 횟수", 0, 10, base["high_fat_count"])
    veg_count = st.slider("샐러드·채소·건강식 구매 횟수", 0, 10, base["veg_count"])
    exercise = st.radio("운동/헬스장/웨어러블 활동 데이터", ["YES", "NO"], index=0 if base["exercise"] == "YES" else 1, horizontal=True)
    rejections = st.slider("최근 건강식 추천 거절 횟수", 0, 5, base["rejections"])

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

with col_right:
    st.subheader("2) ID3 기반 판단 결과")
    features = to_features(data)
    level, interpretation, path = id3_decision(features)
    actions = agent_actions(level, features, rejections)

    m1, m2, m3 = st.columns(3)
    m1.metric("LATE_EAT", features["LATE_EAT"])
    m2.metric("HIGH_FAT", features["HIGH_FAT"])
    m3.metric("VEG_LOW", features["VEG_LOW"])

    if level == "High":
        st.error(f"판정: {level} — {interpretation}")
    elif level == "Medium":
        st.warning(f"판정: {level} — {interpretation}")
    else:
        st.success(f"판정: {level} — {interpretation}")

    st.markdown("**ID3 판단 경로**")
    for item in path:
        st.write("- " + item)

    st.code("""LATE_EAT?
├─ YES → HIGH_FAT? → VEG_LOW? → High/Medium
└─ NO  → EXERCISE? → VEG_LOW? → Medium/Low""", language="text")

st.divider()

st.subheader("3) Agent 실행: 추천이 아니라 행동으로 연결")
a1, a2 = st.columns([1, 1])

with a1:
    st.markdown(f"### 🎯 {actions['title']}")
    st.write("**이번 주 행동 목표**")
    st.info(actions["goal"])

    st.write("**Agent가 구성한 장바구니**")
    for item in actions["cart"]:
        st.write(f"- {item}")

with a2:
    st.write("**주문/구매 연결 예시**")
    for item in actions["cart"][:4]:
        c1, c2 = st.columns(2)
        c1.link_button(f"쿠팡에서 '{item}' 검색", search_link("쿠팡", item), use_container_width=True)
        c2.link_button(f"마켓컬리에서 '{item}' 검색", search_link("마켓컬리", item), use_container_width=True)

    st.write("**배달앱 대체 메뉴 예시**")
    for item in actions["menu"][:3]:
        st.link_button(f"배민에서 '{item}' 검색", search_link("배민", item), use_container_width=True)

st.divider()

st.subheader("4) Feedback Loop: 거절할수록 진화하는 Agent")
f1, f2 = st.columns([1, 1])
with f1:
    st.write("**실패/성공 데이터 반영**")
    st.write(actions["feedback"])
    st.write(actions["strategy"])

with f2:
    st.write("**사용자 반응 시뮬레이션**")
    if "accepted" not in st.session_state:
        st.session_state.accepted = 0
    if "rejected" not in st.session_state:
        st.session_state.rejected = 0

    b1, b2 = st.columns(2)
    if b1.button("✅ 주문 연결 수락", use_container_width=True):
        st.session_state.accepted += 1
    if b2.button("❌ 추천 거절", use_container_width=True):
        st.session_state.rejected += 1

    st.metric("수락", st.session_state.accepted)
    st.metric("거절", st.session_state.rejected)
    if st.session_state.rejected >= 2:
        st.warning("거절 데이터가 누적되었습니다. 다음 추천은 ‘완벽한 건강식’보다 ‘덜 나쁜 대체식’으로 조정됩니다.")

st.divider()

st.subheader("5) 발표용 한 줄 요약")
st.markdown(
    "> 이 시스템은 카드소비 데이터를 단순히 보여주는 앱이 아니라, ID3로 식습관 상태를 판단하고 Agentic AI가 장바구니·주문 연결까지 수행하는 행동 변화 Agent입니다."
)
st.caption(f"Demo generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
