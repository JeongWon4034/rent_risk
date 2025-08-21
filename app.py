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
    df["위도_6"] = df["위도"].round(6)
    df["경도_6"] = df["경도"].round(6)
    return df

with st.spinner("📥 매물 데이터를 불러오는 중입니다..."):
    df = load_data()

# --- 4. 화면 분할 ---
col1, col2 = st.columns([2, 1])

# 🗺️ 지도 (좌표 그룹핑 + 샘플링)
with col1:
    st.subheader("🗺️ 수원시 전세사기 위험 매물 지도")

    if len(df) > 2000:
        df_plot = df.sample(2000, random_state=42)  # 성능 위해 샘플링
    else:
        df_plot = df.copy()

    m = folium.Map(location=[37.2636, 127.0286], zoom_start=12, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    grouped = df_plot.groupby(["위도_6", "경도_6"])
    for (lat, lon), group in grouped:
        if pd.isna(lat) or pd.isna(lon):
            continue

        info = "<br>".join(
            f"<b>{row['단지명']}</b> | 보증금: {row['보증금.만원.']}만원 "
            f"| 전세가율: {row['전세가율']}% | 계약유형: {row['계약유형']}"
            for _, row in group.iterrows()
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="red",
            fill=True,
            fill_opacity=0.6,
            popup=info
        ).add_to(marker_cluster)

    map_click = st_folium(m, width=750, height=600)

# 🤖 GPT 위험 설명
with col2:
    st.subheader("🤖 GPT 위험 설명")

    if "gpt_cache" not in st.session_state:
        st.session_state["gpt_cache"] = {}

    if map_click and map_click.get("last_object_clicked_popup"):
        popup_text = map_click["last_object_clicked_popup"]

        # 단지명 추출 (팝업에서 첫 번째 단지명 기준)
        clicked_name = popup_text.split("<br>")[0].replace("<b>", "").replace("</b>", "")
        key = clicked_name.strip()

        if key not in st.session_state["gpt_cache"]:
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 부동산 전세사기 위험 분석 전문가입니다."},
                        {"role": "system", "content": "매물 정보를 바탕으로 위험 요인을 두세 문장으로 간단히 설명하세요."},
                        {"role": "user", "content": popup_text.replace("<br>", " ")}
                    ]
                )
                gpt_reply = response.choices[0].message.content.strip()
                st.session_state["gpt_cache"][key] = gpt_reply
            except Exception as e:
                st.session_state["gpt_cache"][key] = f"❌ GPT 호출 실패: {e}"

        st.markdown(f"### 🏠 선택된 매물: {clicked_name}")
        st.markdown("### 💬 GPT 분석 결과")
        st.write(st.session_state["gpt_cache"][key])

    else:
        st.info("👉 왼쪽 지도에서 매물을 클릭하세요.")
