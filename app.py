
import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Food Behavior Agent", layout="wide")

def coupang_search(keyword):
    return f"https://www.coupang.com/np/search?q={quote(keyword)}"

def kurly_search(keyword):
    return f"https://www.kurly.com/search?sword={quote(keyword)}"

def baemin_search(keyword):
    return f"https://www.google.com/search?q={quote('배달의민족 ' + keyword)}"

st.markdown("""
<style>
.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
}
.main-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 0.25rem;
}
.sub-title {
    color: #6b7280;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}
.risk-title {
    font-size: 2rem;
    font-weight: 800;
    color: #dc2626;
}
.badge {
    display:inline-block;
    background:#fee2e2;
    color:#991b1b;
    padding:8px 14px;
    border-radius:14px;
    font-weight:700;
    margin-top: 0.4rem;
    margin-bottom: 0.8rem;
}
.food-chip {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    margin: 8px 0;
    background: #ffffff;
    font-weight: 600;
}
.small-muted {
    color:#6b7280;
    font-size:0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🥗 Food Behavior Agent Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">소비데이터 기반 식습관 행동 변화 Agent</div>', unsafe_allow_html=True)

# Top dashboard cards
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🟥 Risk Status")
        st.markdown('<div class="risk-title">High Risk</div>', unsafe_allow_html=True)
        st.markdown('<div class="badge">야식 · 고지방 · 채소부족형</div>', unsafe_allow_html=True)
        st.progress(85)
        st.caption("위험도 85%")

with col2:
    with st.container(border=True):
        st.subheader("🧠 ID3 Decision Result")
        st.write("**LATE_EAT** = YES")
        st.write("**HIGH_FAT** = YES")
        st.write("**VEG_LOW** = YES")
        st.success("→ High 판정")

with col3:
    with st.container(border=True):
        st.subheader("🎯 이번 주 행동 목표")
        st.write("✔ 야식 2회 감소")
        st.progress(40)
        st.write("✔ 단백질 식사 확보")
        st.progress(60)
        st.write("✔ 채소 구매 증가")
        st.progress(35)

st.write("")

# Action cards
left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.subheader("🛒 Agent 추천 장바구니")
        cart_items = [
            ("닭가슴살", "닭가슴살"),
            ("샐러드 채소", "샐러드 채소"),
            ("그릭요거트", "그릭요거트"),
            ("현미밥", "현미밥"),
        ]

        for label, keyword in cart_items:
            st.markdown(f'<div class="food-chip">🥬 {label}</div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                st.link_button("쿠팡 검색", coupang_search(keyword), use_container_width=True)
            with b2:
                st.link_button("마켓컬리 검색", kurly_search(keyword), use_container_width=True)

with right:
    with st.container(border=True):
        st.subheader("🍱 대체 메뉴 추천")
        menu_items = ["포케", "샐러드볼", "저염 도시락", "닭가슴살 샐러드"]

        for menu in menu_items:
            st.markdown(f'<div class="food-chip">🍽 {menu}</div>', unsafe_allow_html=True)
            st.link_button("배달앱 메뉴 검색", baemin_search(menu), use_container_width=True)

st.write("")

with st.container(border=True):
    st.subheader("🔄 Feedback Loop")
    f1, f2 = st.columns(2)
    with f1:
        if st.button("👍 추천 수락", use_container_width=True):
            st.success("수락 데이터가 반영되었습니다.")
    with f2:
        if st.button("👎 추천 거절", use_container_width=True):
            st.warning("다음 추천에서 더 쉬운 대체식으로 조정됩니다.")
