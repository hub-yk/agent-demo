
import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Food Behavior Agent", layout="wide")

# ---------- URL HELPERS ----------
def coupang_search(keyword):
    return f"https://www.coupang.com/np/search?q={quote(keyword)}"

def kurly_search(keyword):
    return f"https://www.kurly.com/search?sword={quote(keyword)}"

def coupangeats_search(keyword):
    return f"https://www.coupangeats.com/search?keyword={quote(keyword)}"

def baemin_search(keyword):
    return f"https://www.baemin.com/search?keyword={quote(keyword)}"

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 0.6rem;
    padding-bottom: 2rem;
}
.dashboard-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.main-title {
    font-size: 1.65rem;
    line-height: 1.25;
    font-weight: 800;
    color: #1f2937;
    margin: 0;
    white-space: normal;
    overflow: visible;
    word-break: keep-all;
}
.sub-title {
    color: #6b7280;
    font-size: 0.95rem;
    margin-top: 4px;
}
.risk-title {
    font-size: clamp(1.55rem, 4vw, 2rem);
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
.store-card {
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 13px 14px;
    margin: 10px 0 14px 0;
    background: #ffffff;
    box-shadow: 0 1px 6px rgba(0,0,0,0.035);
}
.store-title {
    font-size: 1.02rem;
    font-weight: 750;
    color: #111827;
    margin-bottom: 4px;
}
.store-meta {
    color: #4b5563;
    font-size: 0.9rem;
    line-height: 1.55;
}
.reason {
    display:inline-block;
    margin-top: 6px;
    background:#ecfdf5;
    color:#047857;
    padding:5px 10px;
    border-radius: 12px;
    font-size: 0.82rem;
    font-weight: 650;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="dashboard-header">
  <div class="main-title">🥗 Food Behavior Agent Dashboard</div>
  <div class="sub-title">소비데이터 기반 식습관 행동 변화 Agent</div>
</div>
""", unsafe_allow_html=True)

# ---------- TOP CARDS ----------
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

# ---------- ACTION CARDS ----------
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

        delivery_cards = [
            {
                "menu": "포케",
                "store": "포케올데이 강남점",
                "price": "예상 12,900원",
                "time": "예상 28~38분",
                "rating": "⭐ 4.8",
                "reason": "야식 대체 · 단백질/채소 균형",
                "keyword": "포케"
            },
            {
                "menu": "샐러드볼",
                "store": "샐러디 역삼점",
                "price": "예상 10,900원",
                "time": "예상 24~34분",
                "rating": "⭐ 4.7",
                "reason": "채소 부족 보완",
                "keyword": "샐러드볼"
            },
            {
                "menu": "저염 도시락",
                "store": "건강한끼 도시락",
                "price": "예상 9,800원",
                "time": "예상 30~40분",
                "rating": "⭐ 4.6",
                "reason": "고지방 식단 대체",
                "keyword": "저염 도시락"
            },
            {
                "menu": "닭가슴살 샐러드",
                "store": "그린키친",
                "price": "예상 11,500원",
                "time": "예상 25~35분",
                "rating": "⭐ 4.8",
                "reason": "단백질 식사 확보",
                "keyword": "닭가슴살 샐러드"
            },
        ]

        for item in delivery_cards:
            st.markdown(f"""
            <div class="store-card">
                <div class="store-title">🍽 {item['menu']} · {item['store']}</div>
                <div class="store-meta">{item['rating']} &nbsp; | &nbsp; {item['time']} &nbsp; | &nbsp; {item['price']}</div>
                <div class="reason">{item['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

            e1, e2 = st.columns(2)
            with e1:
                st.link_button("쿠팡이츠에서 보기", coupangeats_search(item["keyword"]), use_container_width=True)
            with e2:
                st.link_button("배민에서 보기", baemin_search(item["keyword"]), use_container_width=True)

st.write("")

# ---------- FEEDBACK ----------
with st.container(border=True):
    st.subheader("🔄 Feedback Loop")
    f1, f2 = st.columns(2)
    with f1:
        if st.button("👍 추천 수락", use_container_width=True):
            st.success("수락 데이터가 반영되었습니다.")
    with f2:
        if st.button("👎 추천 거절", use_container_width=True):
            st.warning("다음 추천에서 더 쉬운 대체식으로 조정됩니다.")
