
import streamlit as st

st.set_page_config(page_title="Food Behavior Agent", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.big-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1f2937;
}
.sub-title {
    color: #6b7280;
    margin-bottom: 20px;
}
.high-risk {
    color: #dc2626;
    font-weight: bold;
    font-size: 1.6rem;
}
.badge {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 6px 12px;
    border-radius: 12px;
    display: inline-block;
    margin-top: 5px;
}
.card-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="big-title">🥗 Food Behavior Agent Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">소비데이터 기반 식습관 행동 변화 Agent</div>', unsafe_allow_html=True)

# ---------- TOP CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🟥 Risk Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="high-risk">High Risk</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge">야식 · 고지방 · 채소부족형</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 ID3 Decision Result</div>', unsafe_allow_html=True)
    st.write("LATE_EAT = YES")
    st.write("HIGH_FAT = YES")
    st.write("VEG_LOW = YES")
    st.success("→ High 판정")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎯 이번 주 행동 목표</div>', unsafe_allow_html=True)
    st.write("• 야식 2회 감소")
    st.write("• 단백질 식사 3회 확보")
    st.write("• 채소 구매 증가")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------- MIDDLE ----------
col4, col5 = st.columns(2)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🛒 Agent 추천 장바구니</div>', unsafe_allow_html=True)
    st.write("✔ 닭가슴살")
    st.write("✔ 샐러드 채소")
    st.write("✔ 그릭요거트")
    st.write("✔ 현미밥")
    st.write("✔ 저염 도시락")
    st.link_button("쿠팡프레시 보기", "https://www.coupang.com")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🍱 대체 메뉴 추천</div>', unsafe_allow_html=True)
    st.write("🥗 포케")
    st.write("🥙 샐러드볼")
    st.write("🍱 저염 도시락")
    st.write("🍚 현미 도시락")
    st.link_button("배달앱 메뉴 보기", "https://www.baemin.com")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------- FEEDBACK ----------
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔄 Feedback Loop</div>', unsafe_allow_html=True)
st.write("최근 건강식 추천 거절 데이터를 반영하여 실행 난이도를 자동 조정합니다.")
col6, col7 = st.columns(2)

with col6:
    st.button("👍 추천 수락")

with col7:
    st.button("👎 추천 거절")

st.info("거절 데이터가 누적될수록 Agent가 사용자의 선호도와 실행 가능성을 학습합니다.")
st.markdown('</div>', unsafe_allow_html=True)
