# --- 1. 라이브러리 임포트 ---
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import openai

# ✅ OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- 2. 페이지 설정 ---
st.set_page_config(layout="wide", page_title="수원시 전세사기 위험 매물 지도", page_icon="💰")

# --- 3. 데이터 로드 ---
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_14.csv")
    df["전세가율"] = pd.to_numeric(df["전세가율"], errors="coerce")
    df["보증금.만원."] = pd.to_numeric(df["보증금.만원."], errors="coerce")
    df = df.dropna(subset=["위도", "경도"])
    return df

df = load_data()

# --- 4. 화면 분할 ---
col1, col2 = st.columns([2, 1])

# 🗺️ 지도
with col1:
    st.subheader("🗺️ 수원시 전세사기 위험 매물 지도")

    m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        popup_info = (
            f"단지명: {row['단지명']}<br>"
            f"보증금: {row['보증금.만원.']}만원<br>"
            f"전세가율: {row['전세가율']}%<br>"
            f"계약유형: {row['계약유형']}"
        )
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=popup_info
        ).add_to(marker_cluster)

    map_click = st_folium(m, width=750, height=600)

# 🤖 GPT 상담
with col2:
    st.subheader("🤖 GPT 위험 설명")

    # 사용자가 마커를 클릭했을 때
    if map_click and map_click.get("last_object_clicked_popup"):
        popup_text = map_click["last_object_clicked_popup"]

        # 매칭되는 데이터 추출
        clicked = None
        for _, row in df.iterrows():
            if row["단지명"] in popup_text:
                clicked = row
                break

        if clicked is not None:
            st.markdown(f"### 🏠 선택된 매물: {clicked['단지명']}")
            st.markdown(
                f"- 보증금: {clicked['보증금.만원.']}만원\n"
                f"- 전세가율: {clicked['전세가율']}%\n"
                f"- 계약유형: {clicked['계약유형']}"
            )

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "당신은 부동산 전세사기 위험 분석 전문가입니다."},
                        {"role": "system", "content": "매물 정보를 바탕으로 위험 요인을 설명하고, 주의해야 할 사항을 간단히 조언하세요."},
                        {"role": "user", "content": f"단지명: {clicked['단지명']}, "
                                                    f"보증금: {clicked['보증금.만원.']}만원, "
                                                    f"전세가율: {clicked['전세가율']}%, "
                                                    f"계약유형: {clicked['계약유형']} "
                                                    f"이 매물의 전세사기 위험을 설명해줘."}
                    ]
                )
                gpt_reply = response.choices[0].message.content.strip()
                st.markdown("### 💬 GPT 분석 결과")
                st.write(gpt_reply)

            except Exception as e:
                st.error(f"❌ GPT 호출 실패: {e}")
        else:
            st.info("지도에서 매물을 클릭하면 상세 위험 설명이 표시됩니다.")
    else:
        st.info("👉 왼쪽 지도에서 매물을 클릭하세요.")
