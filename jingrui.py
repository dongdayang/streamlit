import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import xldr
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATA_URL = (
    "https://github.com/dongdayang/streamlit/blob/main/Q1.xlsx?raw=true"
)


@st.cache(persist=True)
def load_mapdata(lat, lon, district, state):
    df0 = pd.read_excel(DATA_URL,
                        sheet_name=state, )
    count = df0['组织区域'][df0['组织区域'] == district].count()

    df1 = pd.DataFrame(
        np.array([[lat, lon]] * count),
        columns=['lat', 'lon'])
    return df1


def load_data(district, state):
    df0 = pd.read_excel(DATA_URL,
                        sheet_name=state, )
    count = df0['组织区域'][df0['组织区域'] == district].value_counts()
    return count


df = pd.concat([
    load_mapdata(31.181915, 121.589851, '上海一区', '入职'),
    load_mapdata(31.191915, 121.589851, '上海二区', '入职'),
    load_mapdata(31.22114, 121.54409, '上海三区', '入职'),
    load_mapdata(31.107929, 121.581902, '上海四区', '入职'),
    load_mapdata(31.171915, 121.589851, '上海五区', '入职'),
])

df2 = pd.concat([
    load_data('上海三区', '入职'),
    load_data('上海四区', '入职'),
    load_data('上海五区', '入职'),
    load_data('上海六区', '入职'),
])
df3 = pd.concat([
    load_data('上海三区', '离职'),
    load_data('上海四区', '离职'),
    load_data('上海五区', '离职'),
    load_data('上海六区', '离职'),
])
print(df2)
# df2.columns = ['入职', '离职']

df4 = pd.DataFrame(df2)
df4.columns = ['入职']
df5 = pd.DataFrame(df3)
df5.columns = ['离职']
df4['离职'] = df5['离职']


# print(df4)


# print(df4)


# CREATING FUNCTION FOR MAPS
def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
            "width": 1000,
            # "height": 200,

        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=2,
                elevation_range=[0, 1000],
                pickable=False,
                extruded=True,
            ),
        ],
    ))


st.write("各区域招聘分布图")

row1_1, row1_2, row1_3 = st.beta_columns((2, 1, 1))

with row1_1:
    map(df, 31.23035, 121.473717, 10)

with row1_2:
    st.write("")

with row1_3:
    st.write("各大区招聘直方图")

    chart_data = df4

    st.bar_chart(chart_data)
