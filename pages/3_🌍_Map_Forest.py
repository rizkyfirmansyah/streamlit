import streamlit as st
import leafmap.kepler as leafmap

st.set_page_config(layout="wide", page_title="Forest Papua Map", page_icon="🌍")

def forest_papua():
    """
    GeoJsonLayer
    ===========
    """
    BATAS_ADMIN = "https://raw.githubusercontent.com/rizkyfirmansyah/streamlit/papua_forest/data/batas_provinsi_pulau_papua.geojson"

    m = leafmap.Map(center=[-4, 133], zoom=5)
    m.add_geojson(BATAS_ADMIN, layer_name='Batas Admin Papua')

    m.to_streamlit(height=900)

forest_papua()