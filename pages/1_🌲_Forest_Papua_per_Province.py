import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from pandasql import sqldf

st.set_page_config(layout="wide", page_title="Forest per Province", page_icon="🌲")

forest_klhk = pd.read_csv("https://raw.githubusercontent.com/rizkyfirmansyah/streamlit/papua_forest/data/forest_klhk_papua_1990_2000.csv")
province = forest_klhk['provinsi'].drop_duplicates().sort_values(ascending=False)
province_choice = st.sidebar.selectbox('Filter by province:', province, key="province_" + str(province))
years = forest_klhk['year'].drop_duplicates().sort_values(ascending=False)
year_choice = st.sidebar.selectbox('Filter by year:', years)
query_forest = """
    select round(cast(sum(pct_to_boundary) as numeric), 2) as percentage, sum(hectare) as hectare
    from forest_klhk
    where year = """+ str(year_choice) +""" and provinsi = '"""+ str(province_choice) +"""'
    and forest_type <> 'Non Hutan'
"""
forest_quantity = sqldf(query_forest)

def overview_pie_forest():
    """
    Get percentage of forest stock & non forest on each year
    41228227.5 is total area of boundary papua islands based on calculate geometry World Cylindrical Equal Area
    """
    st.title("Overview of Percentage Forest Stock & Non Forest in "+ province_choice +", "+ str(year_choice))
    forest_classes = ['Forest vs Non Forest', '6 classes of forest vs Non Forest']
    forest_choices = st.selectbox('Simplify forest classes:', forest_classes)

    st.header("In "+ str(year_choice) +", "+ province_choice +" had "+f'{int(forest_quantity.hectare):,}'+" hectares of forest*, extending over "+str(float(forest_quantity.percentage))+"% of its land area." )
    st.markdown("""<h5>*forest derived from <a href="https://nfms.menlhk.go.id/metode">MoEF's land use land cover (LULC)</a> 23 classes, omitting Plantation Forest (Hutan Tanaman)</h5>""", unsafe_allow_html=True)

    if forest_choices == 'Forest vs Non Forest':
        query = """
            select round(cast(sum(percentage) as numeric), 2) as percentage, forest as forest_type
            from (select sum(pct_to_boundary) as percentage, forest_type,
                case when forest_type like 'Hutan%' then 'Hutan'
                  else 'Non Hutan'
                end as forest
            from forest_klhk
            where year = """+ str(year_choice) +""" and provinsi = '"""+ str(province_choice) +"""'
            group by forest_type) as forest_non
            group by forest
        """
    elif forest_choices == '6 classes of forest vs Non Forest':
        query = """
            select round(cast(sum(pct_to_boundary) as numeric), 2) as percentage, forest_type from forest_klhk
            where year = """+ str(year_choice) +""" and provinsi = '"""+ str(province_choice) +"""'
            group by forest_type
        """
    forest_pct = sqldf(query)

    if forest_choices == 'Forest vs Non Forest':
        options = {
          "title": {
              "text": "Forest vs Non Forest in "+ str(province_choice) +" on " + str(year_choice),
              "left": "center",
              "top": 20,
              "textStyle": {
                  "color": "#2A2529"
              }
          },
          "backgroundColor": '#c3c3c3',
          "tooltip": {
              "trigger": 'item',
          },
          "legend": {
              "orient": 'vertical',
              "left": 'left',
              "shadowColor": 'rgba(0, 0, 0, 0.5)',
              "shadowBlur": 10
          },
          "series": [
              {
                  "name": "Percentage to "+ str(province_choice) +" Administrative Boundary",
                  "type": "pie",
                  "center": ['50%', '50%'],
                  "data": [
                      { "value": forest_pct[forest_pct['forest_type'] == 'Hutan'].iloc[-1]['percentage'], "name": 'Hutan' },
                      { "value": forest_pct[forest_pct['forest_type'] == 'Non Hutan'].iloc[-1]['percentage'], "name": 'Non Hutan' },
                  ],
                  "labelLine": {
                      "lineStyle": {
                        "color": 'rgba(255, 255, 255, 0.3)'
                      },
                      "smooth": 0.2,
                      "length": 10,
                      "length2": 15
                  },
                  "color": ['#00b04f', '#978594'],
                  "itemStyle": {
                      "emphasis": {
                          "shadowBlur": 10,
                          "shadowOffsetX": 0,
                          "shadowColor": 'rgba(0, 0, 0, 0.5)'
                      }
                  },
                  "animationType": 'scale',
                  "animationEasing": 'elasticOut'
              }
          ]
        }
    elif forest_choices == '6 classes of forest vs Non Forest':
        options = {
            "title": {
                "text": "Forest Classes  vs Non Forest in "+ str(province_choice) +" on " + str(year_choice),
                "left": "center",
                "top": 20,
                "textStyle": {
                    "color": "#2A2529"
                }
            },
            "backgroundColor": '#c3c3c3',
            "tooltip": {
                "trigger": 'item',
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                "shadowColor": 'rgba(0, 0, 0, 0.5)',
                "shadowBlur": 10
            },
            "series": [
                {
                    "name": "Percentage to "+ str(province_choice) +" Administrative Boundary",
                    "type": "pie",
                    "radius": '55%',
                    "center": ['50%', '50%'],
                    "data": [
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Lahan Kering Primer'].iloc[-1]['percentage'], "name": 'Hutan Lahan Kering Primer' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Lahan Kering Sekunder'].iloc[-1]['percentage'], "name": 'Hutan Lahan Kering Sekunder' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Mangrove Primer'].iloc[-1]['percentage'], "name": 'Hutan Mangrove Primer' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Mangrove Sekunder'].iloc[-1]['percentage'], "name": 'Hutan Mangrove Sekunder' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Rawa Primer'].iloc[-1]['percentage'], "name": 'Hutan Rawa Primer' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Hutan Rawa Sekunder'].iloc[-1]['percentage'], "name": 'Hutan Rawa Sekunder' },
                        { "value": forest_pct[forest_pct['forest_type'] == 'Non Hutan'].iloc[-1]['percentage'], "name": 'Non Hutan' },
                    ],
                    "roseType": 'radius',
                    "labelLine": {
                        "lineStyle": {
                          "color": 'rgba(255, 255, 255, 0.3)'
                        },
                        "smooth": 0.2,
                        "length": 10,
                        "length2": 15
                    },
                    "color": ['#00b04f', '#7BE32F', '#2F70E3', '#2FE3D2', '#ffbf00', '#E3D52F', '#978594'],
                    "itemStyle": {
                        "emphasis": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    "animationType": 'scale',
                    "animationEasing": 'elasticOut'
                }
            ]
        }
    st_echarts(options=options, height="700px")

def overview_forest_area():
    """
    Get latest of forest stock & non forest at the year of 2000
    """
    st.title("Overview of Forest Stock & Non Forest in "+ province_choice +", "+ str(year_choice))
    query_forest_area = """
        select round(cast(sum(hectare) as numeric), 2) as hectare, forest_type 
        from forest_klhk 
        where year = """+ str(year_choice) +""" and provinsi = '"""+ str(province_choice) +"""'
        group by forest_type 
        order by 2 asc
    """
    forest_area_overview = sqldf(query_forest_area)
    st.markdown("""<h4>Of """+f'{int(forest_quantity.hectare):,}'+""" ha of forest*, <i>"""+forest_area_overview.forest_type[0]+"""</i> was the largest forest cover, covering a total of """+f'{int(forest_area_overview.hectare[0]):,}'+"""ha</h4>""", unsafe_allow_html=True)

    options = {
        "title": {
            "text": "Forest area in "+ province_choice +" on " + str(year_choice),
            "left": "center",
            "top": 10,
            "textStyle": {
                "color": "#2A2529"
            }
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },
        "toolbox": {
            "show": True,
            "feature": {
              "magicType": { "show": True, "type": ['line'] },
              "restore": { "show": True },
              # "saveAsImage": { "show": True }
            }
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '5%',
            "containLabel": True
        },
        "yAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": forest_area_overview['forest_type'].to_list()
        },
        "xAxis": {"type": "value"},
        "series": [
            {
                "data": forest_area_overview['hectare'].round(1).to_list(),
                "type": "bar",
                "showBackground": True,
                "backgroundStyle": {
                    "color": 'rgba(180, 180, 180, 0.2)'
                },
                "color": ['#00b04f'],
            }
        ]
    }
    st_echarts(options=options, height="400px")

def overview_forest_per_year():
    """
    Get forest stock & non forest on each year
    """
    st.title("Overview of Forest Stock in "+ province_choice +" from 1990 to 2020")
    forest_overview_1990 = forest_klhk[(forest_klhk["year"] == 1990) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_1996 = forest_klhk[(forest_klhk["year"] == 1996) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2000 = forest_klhk[(forest_klhk["year"] == 2000) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2003 = forest_klhk[(forest_klhk["year"] == 2003) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2006 = forest_klhk[(forest_klhk["year"] == 2006) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2009 = forest_klhk[(forest_klhk["year"] == 2009) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2011 = forest_klhk[(forest_klhk["year"] == 2011) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2012 = forest_klhk[(forest_klhk["year"] == 2012) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2013 = forest_klhk[(forest_klhk["year"] == 2013) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2014 = forest_klhk[(forest_klhk["year"] == 2014) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2015 = forest_klhk[(forest_klhk["year"] == 2015) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2016 = forest_klhk[(forest_klhk["year"] == 2016) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2017 = forest_klhk[(forest_klhk["year"] == 2017) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2018 = forest_klhk[(forest_klhk["year"] == 2018) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2019 = forest_klhk[(forest_klhk["year"] == 2019) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    forest_overview_2020 = forest_klhk[(forest_klhk["year"] == 2020) & (forest_klhk["provinsi"] == str(province_choice))].drop(columns=['year', 'pct_to_boundary'], axis=1).groupby('forest_type', as_index=False).sum()
    query_earliest_forest = """
        select sum(hectare) as hectare from forest_overview_1990 where forest_type <> 'Non Hutan'
    """
    query_latest_forest = """
        select sum(hectare) as hectare from forest_overview_2020 where forest_type <> 'Non Hutan'
    """
    earliest_forest = sqldf(query_earliest_forest)
    latest_forest = sqldf(query_latest_forest)
    st.markdown("""<h4>From 1990 to 2020, """+province_choice+""" lost <i>"""+f'{int(abs((latest_forest.hectare - earliest_forest.hectare))):,}'+"""</i> ha of forests</h4>""", unsafe_allow_html=True)


    options = {
        "tooltip": {
            "trigger": 'axis',
            "position": 'inside',
            "axisPointer": {
                "shadowStyle": {
                    "color": "#000",
                    "shadowBlur": 0,
                    "opacity": 0.08
                },
                "type": "shadow"
            },
            "extraCssText": "padding: 8px 15px; font-size: 13px;"
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "top": '20%',
            # "bottom": '15%',
            "containLabel": True
        },
        "yAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": forest_overview_2020['forest_type'].to_list()
        },
        "xAxis": {"type": "value"},
        "legend": {
            "shadowColor": 'rgba(0, 0, 0, 0.5)',
            "shadowBlur": 10,
            "selected": {
                "Forest & Non Forest 1996": False,
                "Forest & Non Forest 2000": False,
                "Forest & Non Forest 2003": False,
                "Forest & Non Forest 2006": False,
                "Forest & Non Forest 2009": False,
                "Forest & Non Forest 2011": False,
                "Forest & Non Forest 2012": False,
                "Forest & Non Forest 2013": False,
                "Forest & Non Forest 2014": False,
                "Forest & Non Forest 2015": False,
                "Forest & Non Forest 2016": False,
                "Forest & Non Forest 2017": False,
                "Forest & Non Forest 2018": False,
                "Forest & Non Forest 2019": False
            }
        },
        "series": [
            {
                "name": 'Forest & Non Forest 1990',
                "data": forest_overview_1990['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 1996',
                "data": forest_overview_1996['hectare'].round(1).to_list(),
                "type": "bar",
                "render": False
            },
            {
                "name": 'Forest & Non Forest 2000',
                "data": forest_overview_2000['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2003',
                "data": forest_overview_2003['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2006',
                "data": forest_overview_2006['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2009',
                "data": forest_overview_2009['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2011',
                "data": forest_overview_2011['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2012',
                "data": forest_overview_2012['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2013',
                "data": forest_overview_2013['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2014',
                "data": forest_overview_2014['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2015',
                "data": forest_overview_2015['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2016',
                "data": forest_overview_2016['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2017',
                "data": forest_overview_2017['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2018',
                "data": forest_overview_2018['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2019',
                "data": forest_overview_2019['hectare'].round(1).to_list(),
                "type": "bar",
            },
            {
                "name": 'Forest & Non Forest 2020',
                "data": forest_overview_2020['hectare'].round(1).to_list(),
                "type": "bar",
            },
        ]
    }
    st_echarts(options=options, height='600px')


overview_pie_forest()
overview_forest_area()
overview_forest_per_year()