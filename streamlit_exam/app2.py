import streamlit as st

# layout 요소
col1, col2 = st.columns(2)
# with col1:
#   st.write('hello')

# with col2:
#   st.write('pass')
  
# with col1:
#   st.metric(
#     '오늘의 날씨',
#     value='35도',
#     delta='+3',
#   )
  
# with col2:
#   st.metric(
#     '오늘의 미세먼지',
#     value='좋음',
#     delta='-30',
#     delta_color='inverse'
#   )
  
# 바이브코딩을 위한 프롬프트
# Streamlit을 활용해 환경 상태 미니 대시보드를 구현하세요.
# 가로로 나란한 두 개의 metric 카드를 만들고
# 각각 온도와 공기질 수치를 보여주며
# 변화량에 따라 색상이 자동으로 달라지도록 설정하세요.
# 전체 코드 형태로 제공하세요.

# “UI 설명 + 사용 함수 이름”을 같이 주면
# 코드 생성 정확도가 급격히 올라간다.


import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="환경 상태 미니 대시보드", layout="wide")

st.title("🌿 환경 상태 미니 대시보드")

# 예시 데이터 (실제 환경에서는 센서 데이터 등으로 대체 가능)
current_temp = 24.5
previous_temp = 22.0

current_air = 42
previous_air = 55

# 변화량 계산
temp_delta = current_temp - previous_temp
air_delta = current_air - previous_air

# 가로 컬럼 생성
col1, col2 = st.columns(2)

# 온도 카드 (온도는 증가하면 보통 긍정으로 간주)
with col1:
    st.metric(
        label="🌡️ 현재 온도 (°C)",
        value=f"{current_temp} °C",
        delta=f"{temp_delta:.1f} °C",
        delta_color="normal"  # 증가: 초록, 감소: 빨강
    )

# 공기질 카드 (공기질 지수는 낮아질수록 좋다고 가정)
with col2:
    st.metric(
        label="🌫️ 공기질 지수 (AQI)",
        value=current_air,
        delta=f"{air_delta}",
        delta_color="inverse"  # 감소: 초록, 증가: 빨강
    )

st.caption("※ 색상은 변화 방향에 따라 자동으로 표시됩니다.")