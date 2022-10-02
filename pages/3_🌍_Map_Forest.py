import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Forest Papua Map", page_icon="🌍")

def forest_papua():
    """
    GeoJsonLayer
    ===========
    Property values in Vancouver, Canada, adapted from the deck.gl example pages. Input data is in a GeoJSON format.
    """
    BATAS_ADMIN = "https://raw.githubusercontent.com/rizkyfirmansyah/streamlit/papua_forest/data/batas_provinsi_pulau_papua.geojson"

    INITIAL_VIEW_STATE = pdk.ViewState(
        latitude=-4.0525, longitude=133.1609, zoom=5, max_zoom=16
    )

    batas_admin = pdk.Layer(
        "GeoJsonLayer",
        BATAS_ADMIN,
        opacity=0.4,
        stroked=True,
        filled=True,
        get_fill_color=[145, 145, 145],
        get_line_color=[60, 60, 60],
    )

    r = pdk.Deck(layers=[batas_admin], initial_view_state=INITIAL_VIEW_STATE)
    return r

st.pydeck_chart(forest_papua())