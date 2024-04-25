import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, date
from PIL import Image

# Set page configuration and custom styles
st.set_page_config(layout="wide")
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css?family=Heebo');
@import url('https://fonts.googleapis.com/css?family=Heebo:400,600,800,900');

body * { 
    -webkit-font-smoothing: subpixel-antialiased !important; 
    text-rendering: optimizeLegibility !important;
}

body hr {
    border-bottom: 1.5px solid rgba(23, 48, 28, 0.5); 
}

div[data-testid="stToolbarActions"] {
    visibility: hidden;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div[data-baseweb="tab-panel"] {
    padding-top: 2rem;
}

div.stButton > button:first-child {
    width: 200px;
    background-color: rgba(23, 48, 28, 0.95);
    color: #F6F4F0;
}

div.stButton p {
    font-family: "Heebo";
    font-weight: 600;
    font-size: 15px;
    letter-spacing: 0.25px;
    padding-top: 1px;
}

div.stLinkButton > a:first-child {
    width: 125px;
    background-color: rgba(23, 48, 28, 0.95);
    font-family: "Heebo" !important;
    letter-spacing: 0.25px;
}

div.stLinkButton p {
    font-size: 15px !important;
    color: #F6F4F0;
    font-family: "Heebo" !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] {
    top: 5rem;
    width: 200px !important;
    background-color: #CDD4D0;
    background: #F6F4F0;
    border-right: 1.5px solid rgba(23, 48, 28, 0.5);
}

div[data-testid="collapsedControl"] {
    top: 5.15rem;
}

div[data-testid="stExpander"], div[data-testid="stExpander"] > details {
    background-color: rgba(247, 250, 248, 0.45);
    background: transparent;
    border: 0px solid black;
    border-radius: 0;
    border-color: rgba(255, 255, 255, 0.05);
}

div[data-testid="stExpander"] > details > summary:hover {
    color: rgb(23, 48, 28);
}

header[data-testid="stHeader"] {
    background: url('https://res.cloudinary.com/drwsupfyj/image/upload/v1700734920/environmentalnewsscraper/gaymiakzqtkjyafo5ov3.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-color: rgb(23, 48, 28);
    height: 5rem;
}

div[data-baseweb="select"], ul[data-testid="stVirtualDropdown"] li {
    font-family: "Heebo";
    font-weight: 600;
    font-size: 15px;
    letter-spacing: 0.25px;
    color: #F6F4F0;
    background-color: rgba(23, 48, 28, 0.95);
}

ul[data-testid="stVirtualDropdown"] li:hover {
    background-color: #B3BCB4;
}

div[data-baseweb="popover"] .st-dk, div[data-baseweb="popover"] li, div[data-baseweb="popover"] .st-emotion-cache-35i14j {
    background-color: rgba(23, 48, 28, 0.95);
    color: #F6F4F0;
}

div[data-baseweb="select"] svg {
    color: #F6F4F0;
}

div[data-testid="stForm"] .st-dk {
    background-color: #DFE3E0;
}

div[data-testid="stCaptionContainer"] {
    margin-bottom: -1.75rem;
}

.st-emotion-cache-z5fcl4, .appview-container {
    padding: 5rem 0.5rem 0rem 1rem;
    background: radial-gradient(rgba(23, 48, 28, 0.7), transparent);
    background: #F6F4F0;
}

</style>
''', unsafe_allow_html=True)


# Database connection setup with SQLAlchemy
@st.experimental_singleton
def get_engine():
    user = st.secrets["username"]
    password = st.secrets["pwd"]
    host = st.secrets["hostname"]
    port = st.secrets["port_id"]
    db = st.secrets["database"]
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

# Query execution with memoization
@st.experimental_memo(ttl=1800)
def load_data():
    query = """
    SELECT news_id, date_created, title, topic, summary, link, image, topic_2
    FROM news
    WHERE article != '' AND image != '';
    """
    with get_engine().connect() as conn:
        df = pd.read_sql(query, conn)
    df['date_created'] = pd.to_datetime(df['date_created'])
    return df

full_df = load_data()

# Session state initialization
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = date.today().strftime("%Y-%m-%d")
if 'keyword' not in st.session_state:
    st.session_state['keyword'] = ""

# Sidebar for date and keyword filters
st.sidebar.header("Date Filter")
today = date.today()
date_options = pd.date_range(start=date(2024, 1, 19), end=today, freq='D').to_list()
date_str_options = [d.strftime("%Y-%m-%d") for d in date_options]

selected_date = st.sidebar.selectbox("Select Date", options=date_str_options, index=len(date_str_options)-1)
st.sidebar.button("Today", on_click=lambda: st.session_state.update({'selected_date': today.strftime("%Y-%m-%d")}))
st.sidebar.button("All Time", on_click=lambda: st.session_state.update({'selected_date': None}))

st.sidebar.header("Keyword Filter")
keyword = st.sidebar.text_input("Enter keyword", value=st.session_state['keyword'])

# Display function for articles
def display_articles(df):
    for _, row in df.iterrows():
        with st.expander(f"{row['title']} ({row['date_created'].date()} - {row['topic']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['image'], width=300, caption=row['date_created'].strftime('%b %d, %Y'))
            with col2:
                st.markdown(f"**Summary**: {row['summary']}")
                st.markdown(f"[Read More]({row['link']})", unsafe_allow_html=True)

# Filter data based on date and keyword
def filter_data(df, date, keyword):
    if date:
        df = df[df['date_created'].dt.date == datetime.strptime(date, "%Y-%m-%d").date()]
    if keyword:
        df = df[df.apply(lambda x: keyword.lower() in x['title'].lower() or keyword.lower() in x['summary'].lower(), axis=1)]
    return df

# Apply filters and display articles
filtered_df = filter_data(full_df, st.session_state['selected_date'], st.session_state['keyword'])
if filtered_df.empty:
    st.write("No articles found.")
else:
    display_articles(filtered_df)

# Tabs for topics
topics = ["All", "Business & Innovation", "Climate Change", "Crisis", "Energy", "Environmental Law", "Fossil Fuel", "Lifestyle", "Pollution", "Society", "Water", "Wildlife & Conservation"]
tabs = st.tabs(topics)

for tab, topic in zip(tabs, topics):
    with tab:
        if topic == "All":
            topic_df = filtered_df
        else:
            topic_df = filtered_df[(filtered_df['topic'] == topic) | (filtered_df['topic_2'] == topic)]
        if topic_df.empty:
            st.write(f"No news for {topic}.")
        else:
            display_articles(topic_df)
