import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import datetime

# Set up Streamlit page configuration
st.set_page_config(layout="wide")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css?family=Heebo'); 
@import url('https://fonts.googleapis.com/css?family=Heebo:400,600,800,900');  

body * { 
    -webkit-font-smoothing: subpixel-antialiased !important; 
    text-rendering:optimizeLegibility !important;
}

body hr {
    border-bottom: 1.5px solid rgba(23, 48, 28, 0.5); 
}

div[data-testid="stToolbarActions"] {
    visibility:hidden;
}
/*
#MainMenu {visibility: hidden;}
*/
footer {visibility: hidden;}

div[data-baseweb="tab-panel"] {
    padding-top: 2rem;
}

div.stButton > button:first-child {
    width: 200px;
    background-color: rgba(23, 48, 28, 0.95) ;
    color: #F6F4F0; 
}
div.stButton p {
    font-family: "Heebo";
    font-weight:600;
    font-size: 15px;
    letter-spacing: 0.25px;
    padding-top: 1px;
}

div.stLinkButton > a:first-child {
    width: 125px;
    background-color: rgba(23, 48, 28, 0.95) ;
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
    background-color:#CDD4D0;
    background: #F6F4F0;
    border-right: 1.5px solid rgba(23, 48, 28, 0.5);
}
div[data-testid="collapsedControl"] {
    top:5.15rem;
}
div[data-testid="stExpander"] {
    background-color: rgba(247, 250, 248, 0.45) ;
    background: transparent;
    border: 0px solid black;
}
.st-emotion-cache-yf5hy5 p:nth-child(1) {
    font-size: 16px;
    color: green;
    font-family: "Georgia";
}
.st-emotion-cache-yf5hy5 p:nth-child(2) {
    font-size: 2.25rem;
    font-weight: 800;
    font-family: 'Heebo';
    line-height:1.15;
    letter-spacing: 0.25px;
    margin: 10px 0 0 0;
}
header[data-testid="stHeader"] {
    background: url('https://res.cloudinary.com/drwsupfyj/image/upload/v1700734920/environmentalnewsscraper/gaymiakzqtkjyafo5ov3.png');
    background-size: contain ;
    background-repeat: no-repeat;
    background-color:rgb(23, 48, 28);
    height: 5rem;
}

div[data-testid="stAppViewContainer"] > section:nth-child(2) {
    overflow-x: hidden;
}
.st-emotion-cache-uf99v8 {
    overflow-x: hidden;
}

.appview-container > section:nth-child(2) > div:nth-child(1) {
    padding: 4.5rem 0.5rem 0rem 1rem;
}
.appview-container > section:nth-child(1) > div:nth-child(1) > div:nth-child(2) {
    padding: 1rem 1.5rem 1.5rem 1.5rem;
}
.st-dn {
    background-color: transparent;
}


div[data-testid="textInputRootElement"] {
    border: 1px solid rgba(23, 48, 28, 0.95);
}
div[data-testid="stForm"] {
    border: 0px;
    padding:0;
}
div[data-testid="stExpanderDetails"] p {
    font-family:'Georgia';
    font-size: 18px;
}
div[data-testid="StyledLinkIconContainer"] {
    font-weight: 900;
    font-family:'Heebo';
    font-size: 2.5rem;
    letter-spacing: 0.25px;
}
div[data-testid="stMarkdownContainer"] h2 {
    font-family:'Heebo';
    font-weight: 800;
    letter-spacing: 0.25px;
}

.st-emotion-cache-z5fcl4 {
    padding: 5rem 0.5rem 0rem 1rem;
}

.appview-container {
    background: radial-gradient(rgba(23, 48, 28, 0.7), transparent);
    background: #F6F4F0;
}
div[data-testid="stExpander"] > details {
    bordder-radius: 0;
    border-color: rgba(255, 255, 255, 0.05);
    max-width: 74rem;
}


div[data-baseweb="tab-panel"] > div:nth-child(1) > div:nth-child(1) {
    gap: 0.5rem;
}

div[data-testid="stExpander"] > details > summary:hover {
    color: rgb(23, 48, 28);
}
 
div[data-baseweb="select"] {
    font-family: "Heebo";
    font-weight:600;
    font-size: 15px;
    letter-spacing: 0.25px;
}

ul[data-testid="stVirtualDropdown"] li {
    text-align: center;
    font-family: "Heebo";
}
ul[data-testid="stVirtualDropdown"] li:hover {
    color: rgba(23, 48, 28, 0.95);
    background-color:#B3BCB4;
}

div[data-baseweb="select"] > div:first-child > div > div:first-child {
    padding-left: 48px;
    color: #F6F4F0;
    padding-top: 1px;
    
}

div[data-baseweb="select"] div {
    background-color: rgba(23, 48, 28, 0.95);
    color: #F6F4F0;
    border: 0px;
}
div[data-baseweb="popover"] .st-dk {
    background-color: rgba(23, 48, 28, 0.95);
}
div[data-baseweb="popover"] li {
    color: #F6F4F0;
    background-color: rgba(23, 48, 28, 0.95);
}
div[data-baseweb="popover"]  .st-emotion-cache-35i14j {
    background: #B3BCB4;
    color: rgba(23, 48, 28, 0.95) !important;
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
full_df['date_created'] = pd.to_datetime(full_df['date_created'])

# Setup date filters for sidebar
min_date = datetime.date(2024, 8, 20)  # Adjust as necessary
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

st.sidebar.markdown(
    '<div style="text-align: center;">'
    '<a href="https://github.com/nammmx/Environmental-News-Scraper" '
    'style="text-decoration: none; color: inherit;">'
    '<img src="https://res.cloudinary.com/drwsupfyj/image/upload/v1714026198/environmentalnewsscraper/vbbpbt86no6rmbue5xs5.png" '
    'style="width: 20%;" /><br>'
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
                    st.image(row['image'], use_column_width='always')
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

topics = ["All", "Business & Innovation", "Climate Change", "Crisis", "Energy", "Fossil Fuel",
          "Lifestyle", "Politics & Law", "Pollution", "Society", "Water", "Wildlife & Conservation"]




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
