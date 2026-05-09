# 소비데이터 기반 식습관 교정 Agent 데모

발표용 Streamlit 프로토타입입니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 배포 방법

1. GitHub에 `app.py`, `requirements.txt` 업로드
2. Streamlit Community Cloud에서 New app 생성
3. 배포 URL을 QR코드로 변환
4. PPT에 QR코드 삽입

## 발표용 설명

이 데모는 실제 카드 API를 연결하지 않고, 가상 소비데이터를 이용해 다음 흐름을 보여줍니다.

- 카드/배달/식품 소비데이터 입력
- ID3 기반 High/Medium/Low 판정
- Agentic AI 행동 전략 생성
- 장바구니/배달앱 검색 연결
- 추천 수락/거절 피드백 루프 시뮬레이션

의료 진단이 아니라 식습관 소비행동 개선을 위한 라이프스타일 Agent 프로토타입입니다.
