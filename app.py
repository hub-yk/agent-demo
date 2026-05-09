
import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Food Behavior Agent", layout="wide")

# ---------- HELPER ----------
def coupang_search_url(keyword):
    return f"https://www.coupang.com/np/search?q={quote(keyword)}"

def baemin_search_url(keyword):
    # 배민은 외부 검색 딥링크 제한이 있을 수 있어 웹 검색 링크로 우회
    return f"https://www.google.com/search?q={quote('배달의민족 ' + keyword)}"

def marketkurly_search_url(keyword):
    return f"https://www.kurly.com/search?sword={quote(keyword)}"

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
    min-height: 220px;
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
.small-caption {
    font-size: 0.85rem;
    color: #6b7280;
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("최근 소비패턴에서 밤 9시 이후 결제와 고지방 메뉴 결제가 반복적으로 확인되었습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 ID3 Decision Result</div>', unsafe_allow_html=True)
    st.write("LATE_EAT = YES")
    st.write("HIGH_FAT = YES")
    st.write("VEG_LOW = YES")
    st.success("→ High 판정")
    st.markdown('<div class="small-caption">ID3 판단 규칙에 따라 강한 행동 개입이 필요한 유형으로 분류됩니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎯 이번 주 행동 목표</div>', unsafe_allow_html=True)
    st.write("• 야식 2회 감소")
    st.write("• 단백질 식사 3회 확보")
    st.write("• 채소 구매 증가")
    st.write("• 배달음식 1회 건강식으로 대체")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------- MIDDLE ----------
col4, col5 = st.columns(2)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🛒 Agent 추천 장바구니</div>', unsafe_allow_html=True)
    cart_items = [
        ("닭가슴살 3팩", "닭가슴살"),
        ("샐러드 채소", "샐러드 채소"),
        ("무가당 그릭요거트", "무가당 그릭요거트"),
        ("현미밥", "현미밥"),
        ("저염 도시락", "저염 도시락"),
    ]
    for label, keyword in cart_items:
        c1, c2, c3 = st.columns([2.2, 1, 1])
        with c1:
            st.write(f"✔ {label}")
        with c2:
            st.link_button("쿠팡", coupang_search_url(keyword))
        with c3:
            st.link_button("마켓컬리", marketkurly_search_url(keyword))
    st.markdown('<div class="small-caption">추천 품목을 바로 검색 결과로 연결해 구매 실행 단계를 줄입니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🍱 대체 메뉴 추천</div>', unsafe_allow_html=True)
    menu_items = [
        ("포케", "포케"),
        ("샐러드볼", "샐러드볼"),
        ("저염 도시락", "저염 도시락"),
        ("현미 도시락", "현미 도시락"),
        ("닭가슴살 샐러드", "닭가슴살 샐러드"),
    ]
    for label, keyword in menu_items:
        m1, m2 = st.columns([2.4, 1])
        with m1:
            st.write(f"🍽 {label}")
        with m2:
            st.link_button("메뉴 검색", baemin_search_url(keyword))
    st.markdown('<div class="small-caption">배달앱 직접 딥링크가 제한될 수 있어 발표 데모에서는 메뉴 검색 연결로 구현했습니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------- FEEDBACK ----------
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔄 Feedback Loop</div>', unsafe_allow_html=True)
st.write("최근 건강식 추천 거절 데이터를 반영하여 실행 난이도를 자동 조정합니다.")

col6, col7, col8 = st.columns(3)

with col6:
    if st.button("👍 추천 수락"):
        st.success("수락 데이터가 기록되었습니다. 다음 추천에서 유사한 건강식 전략을 강화합니다.")

with col7:
    if st.button("👎 추천 거절"):
        st.warning("거절 데이터가 기록되었습니다. 다음 추천에서는 더 저렴하고 쉬운 대체식으로 조정합니다.")

with col8:
    st.metric("Persona Update", "실행 난이도 완화", "거절 2회 반영")

st.info("거절 데이터가 누적될수록 Agent가 사용자의 선호도와 실행 가능성을 학습합니다.")
st.markdown('</div>', unsafe_allow_html=True)
