import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import datetime

# Set up Streamlit page configuration
st.set_page_config(layout="wide")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Roboto Condensed', sans-serif;
    color: #333;
}

hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(23, 48, 28, 0), rgba(23, 48, 28, 0.75), rgba(23, 48, 28, 0));
}

div[data-testid="stToolbarActions"], #MainMenu, footer {
    display: none;
}

section[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #e0e0e0;
}

div.stButton > button {
    border: 1px solid rgba(23, 48, 28, 0.95);
    background-color: #28a745;
    color: white;
    border-radius: 4px;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 24px;
    margin: 5px 0;
}

header[data-testid="stHeader"] {
    background-color: #20232a;
    color: #61dafb;
}

div[data-testid="stAppViewContainer"] {
    background-color: #fff;
    padding: 2rem;
}

div.stMarkdown, div.streamlit-expanderHeader {
    border-radius: 4px;
    border: 1px solid #e0e0e0;
    padding: 20px;
    margin-bottom: 25px;
    background-color: #f8f9fa;
}

div[data-testid="stMarkdownContainer"] h2, h3 {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 10px;
    margin-top: 30px;
    margin-bottom: 20px;
}

img {
    max-width: 100%;
    height: auto;
}

div[data-testid="stImage"] img {
    border-radius: 4px;
}

div[data-testid="stForm"] {
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
    margin-bottom: 25px;
}

div[data-testid="stExpander"] > details > summary {
    font-weight: bold;
    color: #28a745;
}

.st-emotion {
    overflow-x: hidden;
}

.st-dn {
    background-color: transparent;
}

.st-ee, .st-cx, .st-bx {
    border-radius: 4px;
    background-color: #f8f9fa;
    padding: 1em;
}

.st-cj {
    background-color: #f8f9fa;
}

.st-dt {
    border: 1px solid #e0e0e0;
}

</style>
''', unsafe_allow_html=True)

# Database connection setup using SQLAlchemy
db_url = f"postgresql://{st.secrets['username']}:{st.secrets['pwd']}@{st.secrets['hostname']}:{st.secrets['port_id']}/{st.secrets['database']}"
engine = create_engine(db_url)

@st.experimental_memo(ttl=1800)
def execute_query(query):
    with engine.connect() as connection:
        result = pd.read_sql_query(query, connection)
    return result

# Retrieve full dataframe with necessary columns
full_df = execute_query("""SELECT news_id, date_created, title, topic, summary, link, image, topic_2
                           FROM news WHERE article != '' AND image != '';""")

# Setup date filters for sidebar
min_date = datetime.date(2022, 1, 1)  # Adjust as necessary
max_date = datetime.date.today()

date_list = pd.date_range(min_date, max_date, freq='d').tolist()
date_list_filter = [date.strftime("%Y-%m-%d") for date in date_list]
date_list_filter.reverse()  # Display dates in descending order

def format_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime('%b %d, %Y')

def update_date(option):
    if isinstance(option, list):
        st.session_state.selected_dates = [datetime.datetime.strptime(date, "%Y-%m-%d").date() for date in option]
    else:
        st.session_state.selected_dates = [datetime.datetime.strptime(option, "%Y-%m-%d").date()]

# Initialize session state variables
if 'selected_dates' not in st.session_state:
    st.session_state['selected_dates'] = [max_date]
if 'keyword' not in st.session_state:
    st.session_state['keyword'] = ''
if 'date_select' not in st.session_state:
    st.session_state['date_select'] = date_list_filter[0]

st.sidebar.header("Date Filter")
selected_date = st.sidebar.selectbox(
    "Select Date",
    label_visibility= "collapsed",
    options=date_list_filter,
    index=0,
    format_func=format_date,
    on_change=lambda: update_date(st.session_state['date_select']),
    key='date_select'
)

st.sidebar.button("Today", on_click=lambda: update_date(date_list_filter[0]))
st.sidebar.button("All Time", on_click=lambda: update_date(date_list_filter))

# Keyword filter in sidebar
st.sidebar.header("Keyword Filter")
def on_search():
    st.session_state.keyword = st.session_state.keyword_input

keyword_input = st.sidebar.text_input(
    "Search Keyword",
    placeholder='Search Keyword',
    label_visibility= "collapsed",
    key='keyword_input',
    on_change=on_search
)

def on_reset():
    st.session_state.keyword = ''
    st.session_state.keyword_input = ''

search_button = st.sidebar.button("Search", on_click=on_search)
reset_button = st.sidebar.button("Reset", on_click=on_reset)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown(
    '<div style="text-align: center;">'
    '<a href="https://github.com/nammmx/Environmental-News-Scraper" '
    'style="text-decoration: none; color: inherit;">'
    '<img src="https://res.cloudinary.com/drwsupfyj/image/upload/v1714026198/environmentalnewsscraper/vbbpbt86no6rmbue5xs5.png" '
    'style="width: 30%;" /><br>'
    '<span style="color: rgba(23, 48, 28, 0.95);">View on GitHub</span>'
    '</a>'
    '</div>',
    unsafe_allow_html=True
)






def display_articles(df):
    if not df.empty:
        df.sort_values("date_created", ascending=False, inplace=True)
        for index, row in df.iterrows():
            with st.expander(f"{row['topic']} | {row['topic_2']}\n\n{row['title']}", expanded=True):
                col1, col2 = st.columns([1, 2.25])
                with col1:
                    st.image(row['image'], width=300)
                with col2:
                    st.caption(row['date_created'].strftime('%B %d, %Y'))
                    st.markdown(f"**Summary**: {row['summary']}")
                    st.link_button("Read Article", row['link'])
                st.divider()

# Filter data based on selected dates and keyword and display in tabs
selected_date_df = full_df[full_df['date_created'].dt.date.isin(st.session_state.selected_dates)]

if st.session_state.keyword:
    selected_date_df = selected_date_df[selected_date_df['title'].str.contains(st.session_state.keyword, case=False) |
                                         selected_date_df['summary'].str.contains(st.session_state.keyword, case=False) |
                                         selected_date_df['topic'].str.contains(st.session_state.keyword, case=False) |
                                         selected_date_df['topic_2'].str.contains(st.session_state.keyword, case=False)]

topics = ["All", "Business & Innovation", "Climate Change", "Crisis", "Energy", "Environmental Law", "Fossil Fuel",
          "Lifestyle", "Pollution", "Society", "Water", "Wildlife & Conservation"]




selected_dates = st.session_state.get('selected_dates', [])
if not selected_dates:
    result_display = "Today"
elif selected_dates == [max_date]:
    result_display = "Today"
elif len(selected_dates) == len(date_list_filter):
    result_display = "All Time"
else:
    result_display = format_date(st.session_state['date_select'])
st.header(f"News from {result_display}")




tabs = st.tabs(topics)


for tab, topic in zip(tabs, topics):
    with tab:
        if topic != "All":
            topic_df = selected_date_df[(selected_date_df['topic'] == topic) | (selected_date_df['topic_2'] == topic)]
        else:
            topic_df = selected_date_df
        display_articles(topic_df)
