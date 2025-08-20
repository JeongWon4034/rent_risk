# --- 1. Library Imports ---
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px

# --- 2. Page Configuration ---
st.set_page_config(layout="wide", page_title="수원시 전세사기 위험 매물 지도", page_icon="💰")

# --- 3. Premium Header ---
st.markdown("""
<div style="background: var(--secondary-background-color); 
            padding: 2rem; border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
    <h1 style="margin:0; font-size:2.2rem; font-weight:700; color: var(--text-color);">
        💰 수원시 전세사기 위험 매물 분석 시스템
    </h1>
</div>
""", unsafe_allow_html=True)

# --- 4. Sidebar ---
analysis_mode = st.sidebar.radio(
    "🔍 분석 모드 선택",
    ["🏘️ 매물 현황보기", "🔄 GPT 챗봇 상담"]
)

# --- 5. Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_14.csv")
    # 숫자형 변환
    df["전세가율"] = pd.to_numeric(df["전세가율"], errors="coerce")
    df["보증금.만원."] = pd.to_numeric(df["보증금.만원."], errors="coerce")
    return df.dropna(subset=["위도", "경도"])

df = load_data()

# --- 6. Main Content ---
if analysis_mode == "🏘️ 매물 현황보기":
    tab_report, tab_map, tab_data = st.tabs([
        "📊 종합 리포트",
        "🗺️ 인터랙티브 맵",
        "📄 상세 데이터 조회"
    ])

    # 📊 종합 리포트
    with tab_report:
        st.subheader("📊 주요 지표 요약")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("총 매물 수", len(df))
        with col2: st.metric("평균 전세가율", f"{df['전세가율'].mean():.2f}%")
        with col3: st.metric("최고 전세가율", f"{df['전세가율'].max():.2f}%")

        st.markdown("### 전세가율 분포")
        fig = px.histogram(df, x="전세가율", nbins=30, title="전세가율 분포 히스토그램")
        st.plotly_chart(fig, use_container_width=True)

    # 🗺️ 인터랙티브 맵
    with tab_map:
        st.subheader("🗺️ 수원시 전세사기 위험 매물 지도")


                
                
        m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
        st_folium(m, width=900, height=600)

                
                

        for _, row in df.iterrows():
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=(
                    f"<b>{row['단지명']}</b><br>"
                    f"보증금: {row['보증금.만원.']}만원<br>"
                    f"전세가율: {row['전세가율']}%<br>"
                    f"계약유형: {row['계약유형']}"
                ),
            ).add_to(marker_cluster)
        st_folium(m, width=900, height=600)

    # 📄 상세 데이터 조회
    with tab_data:
        st.subheader("📄 상세 데이터 조회 및 다운로드")
        cause_filter = st.multiselect(
            "계약유형 선택", options=df["계약유형"].unique(), default=df["계약유형"].unique()
        )
        filtered = df[df["계약유형"].isin(cause_filter)]
        st.dataframe(filtered, use_container_width=True, height=500)
        csv = filtered.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 CSV 다운로드", csv, "rent_risk_filtered.csv", "text/csv")

else:  # 🔄 GPT 챗봇 상담
    st.subheader("🔄 GPT 챗봇 상담")
    st.info("향후 GPT 기반 상담 기능이 여기에 추가될 예정입니다.")
