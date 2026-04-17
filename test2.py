import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # 함수 내부 들여쓰기
    df = pd.read_csv('./data/sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()


df['date'] = pd.to_datetime(df['date'])

# KPI 카드 4개
col1, col2, col3, col4 = st.columns(4)
col1.metric('총 매출', f'₩{df["sales"].sum():,}', '+8.3%')

# col2, col3, col4 에 주문수 / 평균 주문액 / 최다 판매 제품 추가
# 탭 구성
tab1, tab2 = st.tabs([' 매출 추이', ' 제품별 매출'])

with tab1:
	monthly = df.groupby('date')['sales'].sum().reset_index()
	fig = px.line(monthly, x='date', y='sales', title='일별 매출 추이')
	st.plotly_chart(fig, use_container_width=True)

with tab2:
	# 제품별 막대 차트 추가
	pass

# 원본 데이터 expander
with st.expander('원본 데이터'):
	st.dataframe(df, use_container_width=True)



# 사이드바 필터
with st.sidebar:
    # with 문 내부 들여쓰기
    st.title('필터')
    selected_regions = st.multiselect('지역', df['region'].unique(), default=df['region'].unique())
    date_range = st.date_input('기간', value=[df['date'].min(), df['date'].max()])

# 필터 적용
# date_range가 시작일과 종료일을 모두 포함하고 있는지 확인하는 로직이 있으면 더 안전합니다.
if len(date_range) == 2:
    df_f = df[
        df['region'].isin(selected_regions) &
        (df['date'] >= pd.Timestamp(date_range[0])) &
        (df['date'] <= pd.Timestamp(date_range[1]))
    ]

    # KPI + 차트
    col1, col2 = st.columns(2)
    col1.metric('필터 적용 후 총 매출', f'₩{df_f["sales"].sum():,}')
    col2.metric('주문 건수', f'{len(df_f):,}건')
else:
    st.warning("기간을 선택해 주세요.")