import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import datetime

# Set up Streamlit page configuration
st.set_page_config(layout="wide")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');

body {
    font-family: 'Nunito', sans-serif;
}

h1 {
    font-size: 3rem;
    font-weight: 800;
}

h2, h3, h4, h5, h6 {
    font-weight: 700;
}

/* Sidebar styles */
section[data-testid="stSidebar"] {
    background-color: #fff;
    border-right: 2px solid #e1e4e8;
    padding: 2rem;
}

/* Button styles */
button {
    border: 2px solid transparent;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: all 300ms;
    color: #fff;
    background-color: #1E88E5;
    font-weight: 700;
}

button:hover {
    background-color: #0D47A1;
    transform: translateY(-2px);
}

/* Header styles */
header[data-testid="stHeader"] {
    background-color: #fff;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.1);
    padding: 1rem 2rem;
}

/* Main area styles */
div[data-testid="stAppViewContainer"] {
    padding: 2rem;
    background-color: #F5F5F5;
}

/* Expander styles */
div[data-testid="stExpander"] {
    transition: all 300ms;
    margin-bottom: 1rem;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}

div[data-testid="stExpander"] summary {
    font-weight: 700;
}

div[data-testid="stExpander"] summary:hover {
    color: #1E88E5;
}

/* Image styles */
div[data-testid="stImage"] img {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}

/* Markdown container styles */
div[data-testid="stMarkdownContainer"] {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    margin: 1rem 0;
    padding: 2rem;
}

/* Input styles */
input {
    border-radius: 5px;
    border: 2px solid #ddd;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    transition: all 300ms;
}

input:focus {
    outline: none;
    border-color: #1E88E5;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.3);
}

/* Dropdown styles */
select {
    border-radius: 5px;
    padding: 0.5rem 1rem;
    transition: all 300ms;
}

select:hover {
    background-color: #EBF1F5;
}

/* Animation for button clicks */
@keyframes click-wave {
    0% {
        height: 40px;
        width: 40px;
        opacity: 0.35;
        position: relative;
    }
    100% {
        height: 50px;
        width: 50px;
        margin-left: -10px;
        margin-top: -10px;
        opacity: 0;
    }
}

button:active:after {
    content: '';
    display: block;
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 100%;
    width: 0;
    height: 0;
    margin-top: -20px;
    margin-left: -20px;
    background: rgba(0, 0, 0, 0.15);
    animation: click-wave 1s;
}

/* Override Streamlit's default styles */
.css-1d391kg {
    padding: 0;
}

.st-bq {
    background-color: #fff;
}

/* Responsive design */
@media (max-width: 768px) {
    .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
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
