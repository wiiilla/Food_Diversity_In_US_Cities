import streamlit as st
import pandas as pd
import numpy as np
import re
import altair as alt
from vega_datasets import data
from scipy.stats import entropy


MD_FILE_PATH = 'Blog.md'
DATA_URL = (
    'https://raw.githubusercontent.com/wiiilla/Food_Diversity_In_US_Cities/main/food_diversity.csv')

# Functions for loading Markdown Context
@st.cache
def load_content(MD_FILE_PATH, clean_func):
    md_file = open(MD_FILE_PATH, "r")
    content = md_file.read()
    md_file.close()
    return clean_func(content)

def clean_content(content):
    # Delete line breaks and Note to myself
    content = re.sub('<br/>', '', content)
    content = re.sub('# Note to myself[\s\S]+', '', content)
    # Split by each placeholder image
    return re.split('!\[.+]\(.+\)', content)


# Functions for Interactive Visualization Setup
def set_style():
    alt.themes.enable('quartz')

def viz_nyc(df):
    NYC = df[df['city'] == 'New York, New York']\
        .groupby(['category_name'])[['city', 'category_name', 'total_business_count', 'sample_rating', 'sample_review_count']]\
        .mean()
    NYC['%_of_total'] = NYC['total_business_count'] / NYC['total_business_count'].sum()
    NYC.sort_values(by='%_of_total', ascending=False).head(10)

    viz_nyc = alt.Chart(NYC.reset_index()).mark_point().encode(
        y=alt.Y('%_of_total:Q', axis=alt.Axis(format='.2p', title='Percent of Total Businesses')),
        color=alt.Color('category_name:N', legend=None),
        tooltip=[alt.Tooltip('category_name:N', title='Ethnic Category'),
                 alt.Tooltip('%_of_total:Q', format='.2%',
                             title='Percentage of Total'),
                 alt.Tooltip('total_business_count:Q', title='Count')]
    ).interactive(bind_x=False)
    return viz_nyc

def viz_paired(df, input_city):
    # Data Transform
    cities = df.groupby(['city', 'category_name'])[['city', 'category_name',
                                                    'total_business_count', 'sample_rating', 'sample_review_count']].mean()
    cities = cities.join(df.groupby(['city'])[['city', 'total_business_count']].sum(),
                         on='city', 
                         rsuffix='_by_city')
    cities['%_of_total'] = cities['total_business_count'] / cities['total_business_count_by_city']

    ## Input city
    selected_cities = ['New York, New York', input_city]

    cities_pair = cities.reset_index()
    cities_pair = cities_pair[cities_pair['city'].isin(selected_cities)]
    
    # Create layered visualization
    viz_cities_slope_circles = alt.Chart(cities_pair).mark_point(size=40, filled=True, opacity=1).encode(
        x=alt.X('city:N', sort=alt.Sort(selected_cities),
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('%_of_total:Q', axis=alt.Axis(
            format='.2p', title='Percent of Total Businesses')),
        color=alt.Color('category_name:N', legend=None),
        tooltip=[alt.Tooltip('category_name:N', title='Ethnic Category'),
                 alt.Tooltip('%_of_total:Q', format='.2%',
                             title='Percentage of Total'),
                 alt.Tooltip('total_business_count:Q', title='Count')
                 ]
    ).interactive(bind_x=False)

    selection_opacity = alt.selection_single(
        encodings=['y'], on='mouseover', clear="click", empty='none')

    condition_opacity = alt.condition(selection_opacity, alt.value(1), alt.value(0.2))
    condition_size = alt.condition(selection_opacity, alt.value(3), alt.value(2))

    viz_cities_slope_line = alt.Chart(cities_pair).mark_line().add_selection(
        selection_opacity
    ).encode(
        x=alt.X('city:N', 
                sort=alt.Sort(selected_cities),
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('%_of_total:Q', 
                axis=alt.Axis(format='.2p', title='Percent of Total Businesses')),
        color=alt.Color('category_name:N', legend=None),
        opacity=condition_opacity,
        size=condition_size,
        tooltip=[alt.Tooltip('category_name:N', title='Ethnic Category'),
                alt.Tooltip('%_of_total:Q', format='.2%',
                            title='Percentage of Total'),
                alt.Tooltip('total_business_count:Q', title='Count')
                ]
    ).interactive(bind_x=False)

    viz_cities_slope = (viz_cities_slope_line +
                        viz_cities_slope_circles).properties(height = 600)

    return viz_cities_slope

def viz_map(df):
    # Data Transformations
    world = data.world_110m.url

    cities = df.groupby(['city', 'category_name'])[['city', 'category_name',
                                                    'total_business_count', 'sample_rating', 'sample_review_count']].mean()
    cities = cities.join(df.groupby(['city'])[['city', 'total_business_count']].sum(),
                         on='city',
                         rsuffix='_by_city')
    cities['%_of_total'] = cities['total_business_count'] / \
        cities['total_business_count_by_city']

    categories_li = list(df['category_name'].unique())
    cities_li = list(df['city'].unique())
    filler = []
    for x in cities_li:
        for y in categories_li:
            filler.append({'city': x, 'category_name': y})
    filler = pd.DataFrame(filler)
    filler.head()

    cities_filled = pd.merge(filler, cities.reset_index()[['city', 'category_name', '%_of_total']],
                             how='outer',
                             left_on=['city', 'category_name'],
                             right_on=['city', 'category_name'])\
        .fillna(0)

    heatmap = cities_filled.groupby('category_name')['%_of_total'].mean()\
        .reset_index()\
        .rename(columns={'%_of_total': 'Avg_%_of_total'})
    heatmap = pd.merge(heatmap, df[['M49_country_code', 'category_name', 'country']],
        how='left', left_on='category_name', right_on='category_name')\
        .drop_duplicates().reset_index().drop(columns=['index'])

    # Viz
    viz_mapbase = alt.Chart(alt.topo_feature(world, 'countries')).mark_geoshape(
        fill='#eee',
        stroke='#fff'
    ).project(
        type='mercator', scale=120
    ).properties(
        height=400
    )

    viz_choropleth = viz_mapbase.mark_geoshape(
        stroke='#fff', strokeWidth=0.25
    ).transform_lookup(
        lookup='id', from_=alt.LookupData(data=heatmap, key='M49_country_code', fields=['Avg_%_of_total', 'category_name', 'country'])
    ).encode(
        alt.Color('Avg_%_of_total:Q',
                  scale=alt.Scale(clamp=True, scheme='tealblues'),
                  legend=alt.Legend(title='Average Percentage Per City',
                                    direction='horizontal',
                                    orient='bottom-right',
                                    gradientLength=200,
                                    titleAnchor='end',
                                    tickMinStep=0.05,
                                    format='.0%'
                                    )),
        tooltip=[alt.Tooltip('country:N', title='Country'),
                 alt.Tooltip('category_name:N', title='Ethnic Category'),
                 alt.Tooltip('Avg_%_of_total:Q',
                             title='Average Percentage Per City', format='.2%')
                 ]
    )
    return (viz_mapbase + viz_choropleth).configure_view(stroke='#fff')
    
@st.cache
def load_data():
    data = pd.read_csv(DATA_URL).rename(
        columns={'Unnamed: 0': 'index'})

    set_style()
    visualizations = {'nyc': viz_nyc(data), 
                      'map': viz_map(data)
                      }

    city_dropdown_list = list(data['city'].unique())
    city_dropdown_list.remove('New York, New York')

    return data, visualizations, city_dropdown_list

# Function that puts together markdown blocks and interactivity
def display_content(content_blocks):
    # [Markdown] Includes:
    # Popularity and Diversity of Food in Major US Cities
    ## An analysis of ethnic cuisines based on Yelp data
    ## Overview
    ## Data Collection and Preparation
    st.markdown(content_blocks[0])

    # [Interactive] Show data loading status
    data_load_state = st.text('Loading data...')
    data, viz, city_list = load_data()
    data_load_state.text("Data loaded.")

    # [Interactive] Toggle to show raw data
    if st.checkbox('Show raw data'):
        st.write(
            'Raw data available at [my Github page](https://github.com/wiiilla/Food_Diversity_In_US_Cities).')
        st.write(data.drop(columns = ['index']))


    # [Markdown] Includes:
    #### Table: Underlying data sources
    #### *Caveats*
    #### Table: Top 10 most popular categories
    ### Intuitive measure: the case of NYC
    split_content = re.split('\s(### Intuitive measure: the case of NYC)',content_blocks[1])
    st.markdown(split_content[0])

    col1, col2 = st.beta_columns([1, 3])
    with col1:        
        # [Interactive] Food Popularity in NYC by Ethnic Cuisine Categories
        st.altair_chart(viz['nyc'], use_container_width=True)
    with col2:
        st.markdown(split_content[1])
        st.markdown(split_content[2])

    # [Markdown] Includes:
    ### How about my city? You asked.
    st.write(content_blocks[2])
    # [Interactive] Let user select the city they're interested in
    city_dropdown = st.selectbox(label='Select City',
                            options=city_list, index = 49)

    # [Interactive] Paired Food Popularity of NYC and your City of Choice
    paired = viz_paired(data, city_dropdown)
    st.altair_chart(paired, use_container_width=True)


    # [Markdown] Includes:
    ### Popular ethnic cuisines in the US, mapped!
    st.write(content_blocks[3])
    # [Interactive] Paired Food Popularity of NYC and your City of Choice
    st.altair_chart(viz['map'], use_container_width=True)


    # [Markdown] Includes:
    #### *Caveats*
    ## Diversity of US City Food Landscape
    ## ...
    ## Discussion
    st.write(content_blocks[4])



content_blocks = load_content(MD_FILE_PATH, clean_content)
display_content(content_blocks)
