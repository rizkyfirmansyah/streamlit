import streamlit as st
import pandas as pd
from pandasql import sqldf
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide", page_title="Trajectory Forest", page_icon="📊")

lulc_klhk_papua = pd.read_csv("https://raw.githubusercontent.com/rizkyfirmansyah/streamlit/papua_forest/data/lulc_klhk_papua_1990_2000.csv")
forest_klhk = pd.read_csv("https://raw.githubusercontent.com/rizkyfirmansyah/streamlit/papua_forest/data/forest_klhk_papua_1990_2000.csv")

province = lulc_klhk_papua['provinsi'].drop_duplicates().sort_values(ascending=False)
province_choice = st.sidebar.selectbox('Filter by province:', province, key="province_" + str(province))
initial_year = forest_klhk['year'].drop_duplicates()
last_year = forest_klhk['year'].drop_duplicates().sort_values(ascending=False)
last_year = forest_klhk['year'].drop_duplicates().sort_values(ascending=False)
initial_year_choice = st.sidebar.selectbox('Select initial year:', initial_year, key="init_year_" + str(initial_year))
last_year_choice = st.sidebar.selectbox('Select last year:', last_year, key="last_year_" + str(initial_year))

expander_bar1 = st.sidebar.expander("What are Sankey diagrams?")
expander_bar1.markdown("""<p>A Sankey diagram is a graphical representation of flows. Several entities (nodes) are represented by rectangles and / or text. Their links/relationships are represented as ribbons that have a width proportional to the importance of the flow.</p>
<p>Sankey diagrams are named after Irish Captain Matthew Henry Phineas Riall Sankey, who used this type of diagram in 1898 in a classic figure showing the energy efficiency of a steam engine. The original charts in black and white displayed just one type of flow (e.g. steam); using colors for different types of flows lets the diagram express additional variables.</p>
<br><a href="https://upload.wikimedia.org/wikipedia/commons/1/10/JIE_Sankey_V5_Fig1.png" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/1/10/JIE_Sankey_V5_Fig1.png" style="width:280px; height:"auto";"></a><a href="https://en.wikipedia.org/wiki/Sankey_diagram" target="_blank" style="text-decoration:none;">Source: Wikipedia</a></p>""", unsafe_allow_html=True)

def sankey_chart():
    st.title("Trajectory (Sankey Diagram) of Forest in "+ province_choice +" ("+str(initial_year_choice)+" to "+str(last_year_choice)+")")
    st.caption("Measured in hectares")
    initial_year_id = str(initial_year_choice)[2:]
    last_year_id = str(last_year_choice)[2:]
    query = """
      select round(cast(sum(hectare) as numeric), 0) as hectare,
        case
          when pl"""+ str(initial_year_id) +"""_id not in (2001, 2002, 2004, 20041, 2005, 20051) then 'Non Hutan ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 2001 then 'Hutan Lahan Kering Primer ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 2002 then 'Hutan Lahan Kering Sekunder ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 2004 then 'Hutan Mangrove Primer ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 20041 then 'Hutan Mangrove Sekunder ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 2005 then 'Hutan Rawa Primer ("""+ str(initial_year_choice) +""")'
          when pl"""+ str(initial_year_id) +"""_id = 20051 then 'Hutan Rawa Sekunder ("""+ str(initial_year_choice) +""")'
        end as source,
        case
          when pl"""+ str(last_year_id) +"""_id not in (2001, 2002, 2004, 20041, 2005, 20051) then 'Non Hutan ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 2001 then 'Hutan Lahan Kering Primer ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 2002 then 'Hutan Lahan Kering Sekunder ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 2004 then 'Hutan Mangrove Primer ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 20041 then 'Hutan Mangrove Sekunder ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 2005 then 'Hutan Rawa Primer ("""+ str(last_year_choice) +""")'
          when pl"""+ str(last_year_id) +"""_id = 20051 then 'Hutan Rawa Sekunder ("""+ str(last_year_choice) +""")'
        end as target
      from lulc_klhk_papua lkp 
      where provinsi = '"""+ str(province_choice) +"""'
      group by 2,3
      order by 2
    """
    forest_sankey = sqldf(query)
    sankey_links = [dict({'source': r.source, 'target': r.target, 'value': r.hectare}) for i, r in forest_sankey.iterrows()]
    sankey_data = [dict({'name': f}) for f in forest_sankey['target'].drop_duplicates().to_list() + forest_sankey['source'].drop_duplicates().to_list()]
    options = {
        "tooltip": {
            "trigger": 'item',
            "triggerOn": 'mousemove',
            # "formatter": "{b}: <strong>{c}</strong> ha"
        },
        "series": {
            "type": 'sankey',
            "left": 0,
            "top": 20.0,
            "right": 200.0,
            "bottom": 25.0,
            "emphasis": {
                "focus": 'adjacency'
            },
            "data": sankey_data,
            "links": sankey_links,
            "lineStyle": {
                "color": 'gradient',
                "curveness": 0.5
            },
            "label": {
              "fontFamily": 'Arial',
              "fontSize": 12
            }
        }
    };
    st_echarts(options=options, height="900px")

sankey_chart()