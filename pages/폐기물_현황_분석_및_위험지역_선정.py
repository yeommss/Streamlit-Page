from time import time
import streamlit as st
import pandas as pd
import numpy as np
import webbrowser
import json
import folium as f
from streamlit_folium import st_folium
from folium.features import CustomIcon


# 페이지 타이틀
st.title('대한민국 폐기물 현황 분석 및 위험지역 선정')

# 소개글 쓰기
# st.write('안녕하세요')


# 데이터 프레임 가져오기
DATA_URL = 'data/danger_zone_final.csv'


# 데이터 로드 함수
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data


# 헤더 쓰는 함수
def write_header(text):
    html = f"""
        <br/>
        <div style="border: 2px solid #e43f3f">
            <center>
                <h3 style="color:#e43f3f">{text}</h3>
            </center>
        </div>
    """
    return st.markdown(html, unsafe_allow_html=True)


# 한 줄 띄우기
def write_br():
    return st.markdown('<br/>', unsafe_allow_html=True)


# Notion 으로 이동
write_header('🌎 Notion 으로 이동')
write_br()
if st.button("Notion 으로 이동하기"):
    url = "https://www.notion.so/cc567db8514c459b91ccd74253985f09"
    webbrowser.open_new_tab(url)
write_br()
write_br()


# Github 으로 이동
write_header('Github Page')
write_br()
if st.button("📌 yeommss's Github로 이동하기"):
    url = "https://github.com/yeommss/Mini-Project/tree/main/5%EC%A3%BC%EC%B0%A8/2%EC%B0%A8"
    webbrowser.open_new_tab(url)
write_br()
write_br()


# 결과 데이터 확인하기
write_header('결과 데이터')
data_load_state = st.text('Loading data...')
danger = load_data(1000)
danger = danger.set_index('시도명')
data_load_state.text("")

with st.expander("폐기물 위험지역 선정 결과 데이터 보기 🔍"):
    st.write(danger)


# folium 시각화 가져오기
GEO_URL = 'data/TL_SCCO_CTPRVN.json'
with open(GEO_URL, encoding='utf-8') as file:
    sido_map = json.load(file)


# folium map 그리기
def load_f_map(danger):
    danger_color = {
        'bad': '#ef553b',
        '5': '#ef553b',
        '4': '#ff7f0f',
        '3': '#fecb52',
        '2': '#00cc96',
        '1': '#18becf',
        'good': '#18becf'
    }

    locs_center = {
        '경기도': (37.3604316949031, 127.51196478764179),
        '서울특별시': (37.56682335885089, 126.97440761286845),
        '부산광역시': (35.164982877010615, 128.99259593632902),
        '경상북도':  (36.289410550148375, 128.8584036201457),
        '경상남도': (35.34828424736677, 128.17368422952208),
        '인천광역시':  (37.47607428669355, 126.56636154800225),
        '대구광역시': (35.814911654999804, 128.56688361070604),
        '충청남도': (36.41802248658698, 126.81484684263197),
        '전라남도':  (34.65474179520874, 126.64859883223278),
        '전라북도':  (35.6762685099596, 127.09661909170836),
        '대전광역시':   (36.36207178164381, 127.38269664482169),
        '강원도': (37.68388172540258, 128.32967660739357),
        '광주광역시': (35.099725344140575, 126.83742531770025),
        '울산광역시': (35.57337156074819, 129.25113145401787),
        '충청북도': (36.7478780111142, 127.75152203320138),
        '세종특별자치시':    (36.639265087573854, 127.24666087561296),
        '제주특별자치도':   (33.39538246551929, 126.52717583906214),
    }

    m = f.Map(location=[36.3, 128.071503],
              zoom_start=7, tiles='cartodbpositron',)

    f.Choropleth(
        geo_data=sido_map,
        name="폐기물 위험 수치",
        data=danger.reset_index(),
        columns=['시도명', '폐기물위험수치'],
        key_on="feature.properties.CTP_KOR_NM",
        fill_color="Spectral_r",
        fill_opacity=0.8,
        line_opacity=0.3,
        legend_name="폐기물 위험 수치",
        highlight=True
    ).add_to(m)

    for k, v in locs_center.items():
        icon_image = 'data/icon/waste/' + \
            str(danger.loc[k, '폐기물위험지역등급']) + '.png'

        icon = CustomIcon(
            icon_image,
            icon_size=(30, 30),
            icon_anchor=(15, 15),
            popup_anchor=(30/2, 0)
        )
        marker = f.map.Marker(
            location=[v[0], v[1]],
            icon=icon,
            tooltip='<div>'
            + '<center style="font-size: 1.5rem;color:'
            + str(danger_color[danger.loc[k, '폐기물위험지역등급']])
            + '"><b>'
            + k
            + '</b></center>'
            + '<div style="border:1px solid black;\
                            background-color:#e2e2e2;\
                            padding:3px;\
                            color:black;\
                            ">'
            + '폐기물위험지역등급: '
            + str(danger.loc[k, '폐기물위험지역등급'])
            + '등급'
            + '<br/>'
            + '폐기물위험수치: '
            + str(round(danger.loc[k, '폐기물위험수치'], 3))
            + '<br/>'
            + '순위: '
            + str(danger.loc[k, '폐기물위험지역순위'])
            + '위'
            + '</div>'
            + '</center>'
            + '</div>'
        )
        m.add_child(marker)

    f.LayerControl().add_to(m)
    return m


load_f_map_state = st.text('안녕 Loading data...')
danger_m = load_f_map(danger)
load_f_map_state.text("")
st_folium(danger_m)
