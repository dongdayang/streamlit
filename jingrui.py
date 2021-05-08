import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATA_URL = (
    "https://github.com/dongdayang/streamlit/blob/main/Q1.xlsx?raw=true"
)


@st.cache(persist=True)

def load_data(lat, lon, district, state):
    df0 = pd.read_excel(DATA_URL,
                        sheet_name=state)
    count = df0['组织区域'][df0['组织区域'] == district].count()

    df1 = pd.DataFrame(
        np.array([[lat, lon]] * count),
        columns=['lat', 'lon'])
    return df1


df = pd.concat([
    load_data(31.181915, 121.589851, '上海一区', '入职'),
    load_data(31.191915, 121.589851, '上海二区', '入职'),
    load_data(31.22114, 121.54409, '上海三区', '入职'),
    load_data(31.107929, 121.581902, '上海四区', '入职'),
    load_data(31.171915, 121.589851, '上海五区', '入职'),
])


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


st.write("各区域招聘数据分布图")
map(df, 31.23035, 121.473717, 10)
