import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="도시 건강 데이터 대시보드", layout="wide")

# ---------------------------
# 1. 타이틀
# ---------------------------
st.title("🏙️ 도시 환경과 비만율 분석 대시보드")
st.markdown("""
성동구 사례 기반  
👉 외부활동율 증가 → 비만율 감소 가설 검증
""")

# ---------------------------
# 2. 샘플 데이터 생성 (보고서 기반)
# ---------------------------
years = list(range(1995, 2025))

obesity = [
    29.8, 30.5, 31.2, 31.5, 31.9,
    32.3, 32.7, 33.0, 33.2, 33.4,
    32.8, 31.8, 30.8, 29.5, 28.4,
    27.3, 26.1, 25.2, 24.4, 23.7,
    23.0, 22.5, 22.1, 21.9, 21.5,
    21.2, 20.9, 20.7, 20.6, 20.6
]

activity = [
    28.4, 27.9, 26.8, 26.2, 25.8,
    25.3, 24.9, 24.5, 24.3, 24.1,
    25.1, 26.8, 28.1, 30.2, 31.4,
    32.6, 33.8, 35.1, 36.2, 37.2,
    38.0, 38.5, 39.0, 38.2, 39.5,
    40.2, 40.9, 41.3, 41.8, 41.8
]

df = pd.DataFrame({
    "year": years,
    "obesity_rate": obesity,
    "activity_rate": activity
})

# ---------------------------
# 3. 사이드바 (정책 시뮬레이션)
# ---------------------------
st.sidebar.header("📊 정책 시뮬레이션")

activity_increase = st.sidebar.slider(
    "외부활동율 증가 (%)",
    0.0, 10.0, 2.0
)

# 보고서 기반 계수 (-0.68)
predicted_change = activity_increase * -0.68

# ---------------------------
# 4. KPI
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("현재 비만율 (2024)", f"{df.iloc[-1]['obesity_rate']}%")
col2.metric("현재 외부활동율", f"{df.iloc[-1]['activity_rate']}%")
col3.metric("예상 비만율 변화", f"{predicted_change:.2f}%p")

# ---------------------------
# 5. 시계열 그래프
# ---------------------------
st.subheader("📈 비만율 추세")

fig, ax = plt.subplots()
ax.plot(df["year"], df["obesity_rate"], label="비만율")
ax.axvline(x=2005, linestyle="--", label="서울숲 조성")
ax.legend()

st.pyplot(fig)

# ---------------------------
# 6. 상관관계 분석
# ---------------------------
st.subheader("📊 외부활동율 vs 비만율")

fig2, ax2 = plt.subplots()
ax2.scatter(df["activity_rate"], df["obesity_rate"])

# 회귀선
z = np.polyfit(df["activity_rate"], df["obesity_rate"], 1)
p = np.poly1d(z)
ax2.plot(df["activity_rate"], p(df["activity_rate"]))

st.pyplot(fig2)

corr = np.corrcoef(df["activity_rate"], df["obesity_rate"])[0, 1]

st.write(f"📉 상관계수: {corr:.3f}")

# ---------------------------
# 7. 정책 인사이트
# ---------------------------
st.subheader("💡 정책 인사이트")

st.markdown(f"""
- 외부활동율이 증가하면 비만율은 감소하는 경향  
- 시뮬레이션 결과: **{activity_increase}% 증가 시 → {predicted_change:.2f}%p 감소**

👉 정책 제안  
- 도보 10분 내 운동시설 확충  
- 생활밀착형 공원 확대  
""")
