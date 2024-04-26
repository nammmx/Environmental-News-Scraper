import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from transformers import pipeline
import io
from stability_sdk import client
import cloudinary
import cloudinary.uploader
import openai

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

@st.cache_data(ttl=1800)
def execute_query(query):
    with engine.connect() as connection:
        result = pd.read_sql_query(query, connection)
    return result

# Retrieve full dataframe with necessary columns
full_df = execute_query("""SELECT news_id, date_created, title, topic, summary, link, image, topic_2
                           FROM news WHERE article != '' AND image != '';""")

# Setup date filters for sidebar
min_date = datetime.date(2024, 4, 25)  # Adjust as necessary
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
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown(
    '<div style="text-align: center;">'
    '<a href="https://github.com/nammmx/Environmental-News-Scraper" '
    'style="text-decoration: none; color: inherit;">'
    '<img src="https://res.cloudinary.com/drwsupfyj/image/upload/v1714026198/environmentalnewsscraper/vbbpbt86no6rmbue5xs5.png" '
    'style="width: 28%;" /><br>'
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

############################################################################################
# Database setup using SQLAlchemy
def create_session(user, password, host, port, db):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    Session = sessionmaker(bind=engine)
    return Session()

# Cloudinary configuration
def configure_cloudinary():
    cloudinary.config(
        cloud_name=st.secrets['cloudinary_cloud_name'], 
        api_key=st.secrets['cloudinary_api_key'], 
        api_secret=st.secrets['cloudinary_api_secret']
    )

# AI tools setup
def setup_ai_tools():
    openai.api_key = st.secrets['openai_api_key']
    stability_api = client.StabilityInference(
        key=st.secrets['stability_api_key'], 
        verbose=True, 
        engine="stable-diffusion-xl-1024-v1-0"
    )
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")
    return summarizer, stability_api

# Process articles
def process_articles(session, summarizer):
    source_url = "https://www.theguardian.com/environment/all"
    response = requests.get(source_url)
    soup = BeautifulSoup(response.text, "lxml")
    date_guardian = datetime.datetime.now().strftime('%#d-%B-%Y').lower()
    section_guardian = soup.find("section", {"id": date_guardian})
    
    existing_links = {link[0] for link in session.execute(text("SELECT link FROM news")).fetchall()}

    for article in section_guardian.find_all("a", class_="u-faux-block-link__overlay js-headline-text"):
        href = article.get("href")
        if href not in existing_links:
            content, summary, topics = fetch_and_summarize_article(href, summarizer)
            if content:
                topic1, topic2 = topics.split('-')
                insert_article(session, article.text, href, content, summary, topic1, topic2)

# Fetch and summarize articles
def fetch_and_summarize_article(href, summarizer):
    response = requests.get(href)
    soup = BeautifulSoup(response.text, "lxml")
    content = ' '.join(p.text for p in soup.find_all("p"))
    summary = summarizer(content, min_length=150, max_length=300, truncation=True)[0]['summary_text']
    topics = chatgpt_topic(content)
    return content, summary, topics

def chatgpt_topic(article):
    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Determine the 2 topic that best fits the news article below. topic1 is the topic that fits the article the best. topic2 is the topic that fits the article 2nd best. Pick only from these topics and dont make up new topics: "Business & Innovation", "Climate Change", "Crisis", "Energy", "Politics & Law", "Fossil Fuel", "Lifestyle", "Pollution", "Society", "Water", "Wildlife & Conservation" Return your answer in the following format: topic1-topic2
                News article: {article} 
            """,
            }
        ],
        model="gpt-3.5-turbo"
    )
    return response.choices[0].message.content

def insert_article(session, title, href, content, summary, topic1, topic2):
    session.execute(text("""
        INSERT INTO news (source, title, link, article, summary, topic, topic_2)
        VALUES (:source, :title, :link, :article, :summary, :topic1, :topic2)
        ON CONFLICT (link) DO NOTHING;
    """), {'source': 'Guardian', 'title': title, 'link': href, 'article': content, 'summary': summary, 'topic1': topic1, 'topic2': topic2})
    session.commit()

# Image handling
def convert_to_jpeg(img):
    with io.BytesIO() as buffer:
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        return buffer.getvalue()

def upload_image(img_data, public_id):
    response = cloudinary.uploader.upload(img_data, folder="environmentalnewsscraper/news_photographs/", public_id=public_id, overwrite=True)
    return response['url']

def generate_and_upload_images(session, stability_api):
    articles = session.execute(text("SELECT news_id, title, summary FROM news WHERE image IS NULL")).fetchall()
    for article in articles:
        try:
            img_url = generate_image(stability_api, article.title, article.summary)
            session.execute(text("UPDATE news SET image = :image WHERE news_id = :id"), {'image': img_url, 'id': article.news_id})
            session.commit()
        except Exception as e:
            print(f"Error processing image for article {article.title}: {e}")

def generate_image(stability_api, title, summary):
    prompt = f"Create a single realistic image for an environmental news website. The title is: {title}. The content is: {summary}."
    response = stability_api.generate(prompt=prompt, steps=30, cfg_scale=8.0, width=1024, height=1024, style_preset="photographic")
    for resp in response:
        img = Image.open(io.BytesIO(resp.artifacts[0].binary))
        img_jpeg = convert_to_jpeg(img)
        public_id = ''.join(c for c in title if c not in '?&#%<>/+')
        public_id = public_id.strip()
        return upload_image(img_jpeg, public_id)

# Main function
def main():
    session = create_session(st.secrets['username'], st.secrets['pwd'], st.secrets['hostname'], st.secrets['port_id'], st.secrets['database'])
    configure_cloudinary()
    summarizer, stability_api = setup_ai_tools()
    process_articles(session, summarizer)
    generate_and_upload_images(session, stability_api)

if st.sidebar.button('Scrape'):
    main()  # This will run your script when the button is clicked

