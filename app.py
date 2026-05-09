
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
    padding-top: 1.5rem;
    background-color: #f5f7fb;
}

.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #1f2937;
}

.sub {
    color: #6b7280;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    min-height: 240px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 12px;
}

.badge {
    display:inline-block;
    background:#fee2e2;
    color:#b91c1c;
    padding:8px 14px;
    border-radius:14px;
    font-weight:600;
}

.risk {
    font-size:2rem;
    font-weight:800;
    color:#dc2626;
}

.small {
    color:#6b7280;
    font-size:0.9rem;
}

.menu-card {
    background:#ffffff;
    padding:14px;
    border-radius:14px;
    border:1px solid #e5e7eb;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🥗 Food Behavior Agent Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">소비데이터 기반 식습관 행동 변화 Agent</div>', unsafe_allow_html=True)

# Top cards
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🟥 Risk Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="risk">High Risk</div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="badge">야식 · 고지방 · 채소부족형</div>', unsafe_allow_html=True)
    st.progress(85)
    st.markdown('<div class="small">위험도 85%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 ID3 Decision Result</div>', unsafe_allow_html=True)
    st.write("LATE_EAT = YES")
    st.write("HIGH_FAT = YES")
    st.write("VEG_LOW = YES")
    st.success("→ High 판정")
    st.code("""LATE_EAT?
 ├─ YES → HIGH_FAT?
 │        ├─ YES → VEG_LOW? → High
 └─ NO  → Medium/Low""")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎯 이번 주 행동 목표</div>', unsafe_allow_html=True)
    st.write("✔ 야식 2회 감소")
    st.progress(40)
    st.write("✔ 단백질 식사 확보")
    st.progress(60)
    st.write("✔ 채소 구매 증가")
    st.progress(35)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Bottom cards
b1, b2 = st.columns(2)

with b1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🛒 Agent 추천 장바구니</div>', unsafe_allow_html=True)

    items = [
        ("닭가슴살", "닭가슴살"),
        ("샐러드 채소", "샐러드 채소"),
        ("그릭요거트", "그릭요거트"),
        ("현미밥", "현미밥")
    ]

    for label, keyword in items:
        st.markdown(f'<div class="menu-card">🥬 {label}</div>', unsafe_allow_html=True)
        x1, x2 = st.columns(2)
        with x1:
            st.link_button("쿠팡", coupang_search(keyword))
        with x2:
            st.link_button("마켓컬리", kurly_search(keyword))

    st.markdown('</div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🍱 대체 메뉴 추천</div>', unsafe_allow_html=True)

    menus = ["포케", "샐러드볼", "저염 도시락", "닭가슴살 샐러드"]

    for menu in menus:
        st.markdown(f'<div class="menu-card">🍽 {menu}</div>', unsafe_allow_html=True)
        st.link_button("배달앱 메뉴 검색", baemin_search(menu))

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Feedback
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔄 Feedback Loop</div>', unsafe_allow_html=True)

f1, f2 = st.columns(2)

with f1:
    if st.button("👍 추천 수락"):
        st.success("추천 전략을 강화합니다.")

with f2:
    if st.button("👎 추천 거절"):
        st.warning("다음 추천에서 난이도를 조정합니다.")

st.markdown('</div>', unsafe_allow_html=True)
