import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="성동구 도시 건강 대시보드",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* ── 배경 ── */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* ── 헤더 배너 ── */
.hero-banner {
    background: linear-gradient(135deg, #0f2027 0%, #1a3a2e 50%, #0d3a2e 100%);
    border: 1px solid #2ea043;
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(46,160,67,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1rem;
    color: #8b949e;
    margin: 0;
    font-weight: 300;
}
.hero-tag {
    display: inline-block;
    background: rgba(46,160,67,0.2);
    border: 1px solid #2ea043;
    color: #3fb950;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}

/* ── KPI 카드 ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.kpi-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px 28px;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2ea043; }
.kpi-label {
    font-size: 0.75rem;
    color: #8b949e;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #f0f6fc;
    font-family: 'DM Mono', monospace;
    line-height: 1;
}
.kpi-unit {
    font-size: 1rem;
    color: #8b949e;
    font-weight: 400;
}
.kpi-delta {
    font-size: 0.85rem;
    margin-top: 8px;
    font-weight: 500;
}
.kpi-delta.pos { color: #3fb950; }
.kpi-delta.neg { color: #f85149; }
.kpi-delta.neu { color: #d29922; }

/* ── 섹션 헤더 ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 36px 0 18px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid #21262d;
}
.section-icon {
    width: 32px; height: 32px;
    background: rgba(46,160,67,0.15);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0;
}
.section-desc {
    font-size: 0.82rem;
    color: #8b949e;
    margin: 0;
}

/* ── 인사이트 카드 ── */
.insight-box {
    background: #161b22;
    border-left: 4px solid #2ea043;
    border-radius: 0 10px 10px 0;
    padding: 20px 24px;
    margin-top: 16px;
}
.insight-box p { color: #c9d1d9; font-size: 0.92rem; line-height: 1.8; margin: 0; }
.insight-box strong { color: #3fb950; }

/* ── 정책 카드 ── */
.policy-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 16px;
}
.policy-item {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 18px 20px;
    display: flex; align-items: flex-start; gap: 12px;
}
.policy-icon { font-size: 1.4rem; line-height: 1; }
.policy-text { font-size: 0.88rem; color: #c9d1d9; line-height: 1.5; }
.policy-text strong { color: #f0f6fc; display: block; margin-bottom: 4px; }

/* ── 상관관계 배지 ── */
.corr-badge {
    display: inline-block;
    background: rgba(248, 81, 73, 0.15);
    border: 1px solid #f85149;
    color: #f85149;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 1rem;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}

/* ── 슬라이더 커스텀 ── */
.stSlider > div > div > div > div { background: #2ea043 !important; }

/* ── matplotlib 배경 맞춤 ── */
.stPlotlyChart, .stPyplot { border-radius: 12px; overflow: hidden; }

/* ── 구분선 ── */
hr { border-color: #21262d !important; }

/* ── 텍스트 ── */
p { color: #c9d1d9 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# DATA
# ─────────────────────────────────────────
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

# 변화량 계산
obesity_peak = max(obesity)
obesity_latest = df.iloc[-1]["obesity_rate"]
obesity_change = obesity_latest - obesity_peak
activity_latest = df.iloc[-1]["activity_rate"]
activity_start = df.iloc[0]["activity_rate"]
corr = np.corrcoef(df["activity_rate"], df["obesity_rate"])[0, 1]


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 20px 0;'>
        <div style='font-size:0.7rem; color:#8b949e; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px;'>연구 주제</div>
        <div style='font-size:1rem; font-weight:700; color:#f0f6fc; line-height:1.4;'>도시 환경과 비만율의 상관관계</div>
        <div style='font-size:0.8rem; color:#8b949e; margin-top:4px;'>성동구 사례 분석 (1995–2024)</div>
    </div>
    <hr style='border-color:#30363d; margin-bottom:20px;'/>
    """, unsafe_allow_html=True)

    st.markdown("#### 🎛️ 정책 시뮬레이터")
    st.markdown("<p style='font-size:0.8rem; color:#8b949e !important;'>외부활동율 증가 시 비만율 예상 변화를 확인하세요</p>", unsafe_allow_html=True)

    activity_increase = st.slider(
        "외부활동율 증가량 (%p)",
        min_value=0.0, max_value=10.0, value=2.0, step=0.5,
        help="회귀계수 β = -0.68 기반 추정"
    )

    predicted_change = activity_increase * -0.68
    predicted_obesity = obesity_latest + predicted_change

    st.markdown(f"""
    <div style='background:#0d1117; border:1px solid #30363d; border-radius:10px; padding:16px; margin-top:16px;'>
        <div style='font-size:0.72rem; color:#8b949e; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:10px;'>시뮬레이션 결과</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='color:#8b949e; font-size:0.85rem;'>현재 비만율</span>
            <span style='color:#f0f6fc; font-weight:600; font-family:DM Mono,monospace;'>{obesity_latest}%</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='color:#8b949e; font-size:0.85rem;'>예상 변화량</span>
            <span style='color:#f85149; font-weight:600; font-family:DM Mono,monospace;'>{predicted_change:.2f}%p</span>
        </div>
        <div style='border-top:1px solid #30363d; padding-top:10px; display:flex; justify-content:space-between;'>
            <span style='color:#8b949e; font-size:0.85rem;'>예상 비만율</span>
            <span style='color:#3fb950; font-weight:700; font-size:1.1rem; font-family:DM Mono,monospace;'>{predicted_obesity:.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#484f58; line-height:1.6;'>
        회귀계수 β = -0.68<br>
        데이터 출처: 성동구 보건통계<br>
        분석 기간: 1995 – 2024
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────

# ── HERO ──
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">📍 서울시 성동구 · 30년 종단 분석</div>
    <h1 class="hero-title">🌿 도시 환경과 비만율 분석</h1>
    <p class="hero-sub">서울숲 조성 이후 외부활동율 증가가 비만율 감소에 미치는 영향 — 1995~2024 데이터 기반 검증</p>
</div>
""", unsafe_allow_html=True)


# ── KPI ──
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">📉 현재 비만율 (2024)</div>
        <div><span class="kpi-value">20.6</span><span class="kpi-unit"> %</span></div>
        <div class="kpi-delta neg">▼ 피크 대비 {:.1f}%p 감소</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🏃 현재 외부활동율</div>
        <div><span class="kpi-value">41.8</span><span class="kpi-unit"> %</span></div>
        <div class="kpi-delta pos">▲ 1995 대비 +{:.1f}%p 증가</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🔗 피어슨 상관계수</div>
        <div><span class="kpi-value">{:.3f}</span></div>
        <div class="kpi-delta neg">강한 음의 상관관계 확인</div>
    </div>
</div>
""".format(
    abs(obesity_change),
    activity_latest - activity_start,
    corr
), unsafe_allow_html=True)


# ── CHART 1: TIME SERIES ──
st.markdown("""
<div class="section-header">
    <div class="section-icon">📈</div>
    <div>
        <p class="section-title">비만율 & 외부활동율 추세 (1995–2024)</p>
        <p class="section-desc">서울숲 조성(2005) 전후 추세 변화를 주목하세요</p>
    </div>
</div>
""", unsafe_allow_html=True)

fig1, ax1 = plt.subplots(figsize=(12, 5))
fig1.patch.set_facecolor("#0d1117")
ax1.set_facecolor("#161b22")

# 서울숲 이전/이후 배경
ax1.axvspan(1995, 2005, alpha=0.06, color="#f85149", zorder=0)
ax1.axvspan(2005, 2024, alpha=0.06, color="#2ea043", zorder=0)

# 데이터 라인
ax1.plot(df["year"], df["obesity_rate"], color="#f85149", linewidth=2.5,
         label="비만율 (%)", zorder=3, solid_capstyle="round")
ax1.plot(df["year"], df["activity_rate"], color="#3fb950", linewidth=2.5,
         label="외부활동율 (%)", zorder=3, solid_capstyle="round")

# 면적 채우기
ax1.fill_between(df["year"], df["obesity_rate"], alpha=0.12, color="#f85149")
ax1.fill_between(df["year"], df["activity_rate"], alpha=0.10, color="#3fb950")

# 서울숲 수직선
ax1.axvline(x=2005, color="#d29922", linestyle="--", linewidth=1.5, alpha=0.8, zorder=4)
ax1.text(2005.3, 33.8, "서울숲 조성\n(2005)", color="#d29922",
         fontsize=8.5, fontfamily="Noto Sans KR", va="top",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#161b22",
                   edgecolor="#d29922", alpha=0.9))

# 스타일
for spine in ax1.spines.values():
    spine.set_color("#30363d")
ax1.tick_params(colors="#8b949e", labelsize=9)
ax1.set_xlabel("연도", color="#8b949e", fontsize=9, fontfamily="Noto Sans KR")
ax1.set_ylabel("비율 (%)", color="#8b949e", fontsize=9, fontfamily="Noto Sans KR")
ax1.grid(axis="y", color="#21262d", linewidth=0.8, linestyle="--")
ax1.set_xlim(1995, 2024)

legend = ax1.legend(
    loc="upper right", fontsize=9,
    facecolor="#21262d", edgecolor="#30363d",
    labelcolor="#c9d1d9",
    prop={"family": "Noto Sans KR", "size": 9}
)

# 배경 레이블
ax1.text(1999.5, 24.5, "서울숲 조성 전", color="#f85149",
         alpha=0.5, fontsize=8, fontfamily="Noto Sans KR", ha="center")
ax1.text(2014, 24.5, "서울숲 조성 후", color="#3fb950",
         alpha=0.5, fontsize=8, fontfamily="Noto Sans KR", ha="center")

fig1.tight_layout()
st.pyplot(fig1, use_container_width=True)


# ── CHART 2: SCATTER ──
col_l, col_r = st.columns([3, 2], gap="large")

with col_l:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div>
            <p class="section-title">외부활동율 vs 비만율 산점도</p>
            <p class="section-desc">회귀선 및 분포 확인</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(7, 5))
    fig2.patch.set_facecolor("#0d1117")
    ax2.set_facecolor("#161b22")

    # 시간 색상 매핑 (오래될수록 붉은색 → 최근일수록 초록색)
    norm_years = [(y - 1995) / (2024 - 1995) for y in years]
    colors = plt.cm.RdYlGn(norm_years)

    scatter = ax2.scatter(
        df["activity_rate"], df["obesity_rate"],
        c=norm_years, cmap="RdYlGn", s=55, alpha=0.85,
        edgecolors="#0d1117", linewidths=0.6, zorder=3
    )

    # 회귀선
    z = np.polyfit(df["activity_rate"], df["obesity_rate"], 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(df["activity_rate"].min(), df["activity_rate"].max(), 100)
    ax2.plot(x_range, p_line(x_range), color="#d29922", linewidth=2,
             linestyle="--", alpha=0.8, zorder=4, label=f"회귀선 (β={z[0]:.2f})")

    # 스타일
    for spine in ax2.spines.values():
        spine.set_color("#30363d")
    ax2.tick_params(colors="#8b949e", labelsize=9)
    ax2.set_xlabel("외부활동율 (%)", color="#8b949e", fontsize=9, fontfamily="Noto Sans KR")
    ax2.set_ylabel("비만율 (%)", color="#8b949e", fontsize=9, fontfamily="Noto Sans KR")
    ax2.grid(color="#21262d", linewidth=0.8, linestyle="--", alpha=0.6)

    legend2 = ax2.legend(
        facecolor="#21262d", edgecolor="#30363d",
        labelcolor="#c9d1d9", fontsize=9,
        prop={"family": "Noto Sans KR", "size": 9}
    )

    # 컬러바
    cbar = fig2.colorbar(scatter, ax=ax2, shrink=0.8)
    cbar.set_label("시간 (1995 → 2024)", color="#8b949e",
                   fontsize=8, fontfamily="Noto Sans KR")
    cbar.ax.yaxis.set_tick_params(color="#8b949e")
    cbar.outline.set_edgecolor("#30363d")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#8b949e", fontsize=7)

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

with col_r:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🔍</div>
        <div>
            <p class="section-title">분석 요약</p>
            <p class="section-desc">핵심 통계 지표</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 회귀 통계
    z = np.polyfit(df["activity_rate"], df["obesity_rate"], 1)
    r2 = corr ** 2

    st.markdown(f"""
    <div style='display:flex; flex-direction:column; gap:12px;'>
        <div style='background:#161b22; border:1px solid #30363d; border-radius:10px; padding:16px 20px;'>
            <div style='font-size:0.72rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>피어슨 상관계수 (r)</div>
            <span class="corr-badge">{corr:.4f}</span>
            <div style='font-size:0.78rem; color:#8b949e; margin-top:8px;'>강한 음의 선형 관계</div>
        </div>
        <div style='background:#161b22; border:1px solid #30363d; border-radius:10px; padding:16px 20px;'>
            <div style='font-size:0.72rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>결정계수 (R²)</div>
            <span style='font-size:1.5rem; font-weight:800; color:#f0f6fc; font-family:DM Mono,monospace;'>{r2:.4f}</span>
            <div style='font-size:0.78rem; color:#8b949e; margin-top:4px;'>분산의 {r2*100:.1f}% 설명</div>
        </div>
        <div style='background:#161b22; border:1px solid #30363d; border-radius:10px; padding:16px 20px;'>
            <div style='font-size:0.72rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>회귀 기울기 (β)</div>
            <span style='font-size:1.5rem; font-weight:800; color:#d29922; font-family:DM Mono,monospace;'>{z[0]:.3f}</span>
            <div style='font-size:0.78rem; color:#8b949e; margin-top:4px;'>활동 1%p ↑ → 비만율 {abs(z[0]):.3f}%p ↓</div>
        </div>
        <div style='background:#161b22; border:1px solid #30363d; border-radius:10px; padding:16px 20px;'>
            <div style='font-size:0.72rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;'>분석 기간</div>
            <span style='font-size:1.1rem; font-weight:700; color:#f0f6fc; font-family:DM Mono,monospace;'>30년</span>
            <div style='font-size:0.78rem; color:#8b949e; margin-top:4px;'>1995 – 2024 · N=30</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── INSIGHTS ──
st.markdown("""
<div class="section-header">
    <div class="section-icon">💡</div>
    <div>
        <p class="section-title">핵심 인사이트 & 정책 제안</p>
        <p class="section-desc">데이터 기반 도시 건강 정책 방향</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
    <p>
    성동구의 <strong>서울숲 조성(2005)</strong>을 기점으로 외부활동율은 지속적으로 증가했으며, 
    이와 동시에 비만율은 피크치(33.4%) 대비 <strong>{abs(obesity_change):.1f}%p 감소</strong>하였습니다.
    피어슨 상관계수 <strong>r = {corr:.3f}</strong>은 두 변수 간의 강한 음의 선형 관계를 나타내며,
    회귀 기울기 β = {z[0]:.3f}은 <strong>외부활동율 1%p 증가 시 비만율이 약 {abs(z[0]):.2f}%p 감소</strong>함을 시사합니다.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="policy-grid">
    <div class="policy-item">
        <div class="policy-icon">🌳</div>
        <div class="policy-text">
            <strong>생활밀착형 공원 확대</strong>
            도보 5분 내 접근 가능한 소규모 녹지 조성으로 일상적 외부활동 기회 증가
        </div>
    </div>
    <div class="policy-item">
        <div class="policy-icon">🏋️</div>
        <div class="policy-text">
            <strong>운동시설 접근성 강화</strong>
            도보 10분 내 공공 운동시설 확충 및 개방 시간 확대로 참여 장벽 완화
        </div>
    </div>
    <div class="policy-item">
        <div class="policy-icon">🚶</div>
        <div class="policy-text">
            <strong>보행 친화 도시 인프라</strong>
            자동차 중심 도로를 보행자·자전거 우선 환경으로 재편하여 활동량 자연 증대
        </div>
    </div>
    <div class="policy-item">
        <div class="policy-icon">📊</div>
        <div class="policy-text">
            <strong>지속적 건강 데이터 모니터링</strong>
            연 단위 코호트 추적 조사로 정책 효과를 정량적으로 평가 및 피드백
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top: 1px solid #21262d; padding-top: 20px; display:flex; justify-content:space-between; align-items:center;'>
    <div style='font-size:0.78rem; color:#484f58;'>성동구 질병 데이터 분석 · 권용현 · 임슬기</div>
    <div style='font-size:0.78rem; color:#484f58;'>데이터 기간: 1995–2024 · 분석 모델: OLS 단순 선형 회귀</div>
</div>
""", unsafe_allow_html=True)
