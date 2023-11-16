import streamlit as st
import psycopg2
import pandas as pd
from PIL import Image
import datetime

st.set_page_config(layout="wide")

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css?family=Yeseva One'); 
div.stButton > button:first-child {
    width: 200px;
    background-color: rgba(23, 48, 28, 0.95) ;
    color: #f5e1d5; 
}
div.stButton p {
    font-family: "Georgia";
    font-size: 15px;
}

div.stLinkButton > a:first-child {
    width: 105px;
    background-color: rgba(23, 48, 28, 0.95) ;

}
div.stLinkButton p {
    font-size: 13px;
    color: #f5e1d5;
    font-family: "Georgia";
}
section[data-testid="stSidebar"] {
    top: 5rem;
    width: 250px !important; 
    background-color:#B3BCB4;
}
div[data-testid="collapsedControl"] {
    top:5.15rem;
}
div[data-testid="stExpander"] {
    background-color: rgba(247, 250, 248, 0.275) ;
    border: 0px solid black;
}
.st-emotion-cache-yf5hy5 p:nth-child(1){
    font-size: 16px;
    color: green;
    font-family: "Georgia";
}
.st-emotion-cache-yf5hy5 p:nth-child(2) {
    font-size: 25px;
    font-weight: 700;
    font-family: 'Yeseva One';
    line-height:1.5;
}
header[data-testid="stHeader"] {
    background: url('https://res.cloudinary.com/drwsupfyj/image/upload/v1699990104/environmentalnewsscraper/l9uf62gwcqaa5edfoe39.png');
    background-size: contain ;
    background-repeat: no-repeat;
    background-color:rgb(23, 48, 28);
    height: 5rem;
}
.st-emotion-cache-z5fcl4 {
    padding: 5rem 0.5rem 0rem 1rem;
}
.st-emotion--16txtl3 {
    padding: 1.5rem 1.5rem;
}
.st-dn {
    background-color: transparent;
}
div[data-testid="textInputRootElement"] {
    border: 1px solid rgba(23, 48, 28, 0.95);
}
.st-emotion--1aqpwna {
    border: 0px;
    padding:0;
}
.st-emotion--1qmf6ar {
    font-family:'Georgia';
}
.st-emotion--zt5igj {
    font-weight: 600;
    font-family:'Yeseva One';
}
div[data-testid="stMarkdownContainer"] h2 {
    font-family:'Yeseva One';
    font-weight: 600;
}
.st-emotion--1wrcr25 {
    background: radial-gradient(rgba(23, 48, 28, 0.5), transparent);
}
.st-emotion-cache-1hhivay {
    bordder-radius: 0;
    border-color: rgba(255, 255, 255, 0.05);
}
.st-emotion-cache-1kzf7z {
    gap: 2rem;
}
.st-emotion-cache-sbovo5 {
    gap: 2rem;
}
.st-emotion-cache-rq8rg6:hover {
    color: rgb(23, 48, 28);
}
 
div[data-baseweb="select"] {
    font-family: "Georgia";
}

ul[data-testid="stVirtualDropdown"] li {
    text-align: center;
    font-family: "Georgia";
}
ul[data-testid="stVirtualDropdown"] li:hover {
    color: rgba(23, 48, 28, 0.95);
    background-color:#B3BCB4;
}

div[data-baseweb="select"] > div:first-child > div > div:first-child {
    padding-left: 45px;
    color: #f5e1d5;
}

div[data-baseweb="select"] div {
    background-color: rgba(23, 48, 28, 0.95);
    color: #f5e1d5;
    border: 0px;
}
div[data-baseweb="popover"] .st-dk {
    background-color: rgba(23, 48, 28, 0.95);
}
div[data-baseweb="popover"] li {
    color: #f5e1d5;
    background-color: rgba(23, 48, 28, 0.95);
}
div[data-baseweb="popover"]  .st-emotion-cache-35i14j {
    background: #B3BCB4;
    color: rgba(23, 48, 28, 0.95) !important;
}

</style>
''', unsafe_allow_html=True)



hostname = st.secrets["hostname"]
database = st.secrets["database"]
username = st.secrets["username"]
port_id = st.secrets["port_id"]
pwd = st.secrets["pwd"]


@st.cache_data(ttl=3600, show_spinner=False)
def execute_query(query, hostname, database, username, port_id, pwd, result = None):
        
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )

        cur = conn.cursor()
        cur.execute(query)
        if cur.pgresult_ptr is not None:
            result = pd.read_sql_query(query, conn)
        conn.commit()
        return result
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

full_df = execute_query(query=f"""SELECT news_id, date_created, title, topic, summary, link FROM news;""", hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
####################################################################################################### date filters
min_date = datetime.date(2023,11,10)
max_date = datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)

dates = pd.date_range(min_date,max_date + datetime.timedelta(days=1)-datetime.timedelta(days=1),freq='d').to_list()
date_list = [date_obj.strftime("%Y-%m-%d %H:%M:%S") for date_obj in dates]
date_list_filter = [date_obj.strftime("%Y-%m-%d") for date_obj in dates]

lst1 = []
lst1.append(date_list)
for i in range(0,len(date_list)):
    lst1.append(date_list[i])

if 'list' not in st.session_state:
    st.session_state.list = []
if 'date' not in st.session_state:
    st.session_state.date = [date_list_filter[len(date_list_filter)-1]]

if 'show_date' not in st.session_state:
    st.session_state.show_date = date_list_filter[len(date_list_filter)-1]

def select_date():
    st.session_state.list.append(st.session_state.option)
    st.session_state.date = st.session_state.list[-1:]
    st.session_state.show_date = st.session_state.list[-1]

def today():
    st.session_state.date = [date_list_filter[len(date_list_filter)-1]]
    st.session_state.show_date = date_list_filter[len(date_list_filter)-1]

def all_dates():
    st.session_state.date = lst1[0]
    st.session_state.show_date = "All"

def clear_text():
    st.session_state["text"] = ""


st.sidebar.header("Date Filter")

option = [st.sidebar.selectbox(
    label="select", label_visibility= "collapsed",
    options=(date_list_filter), index=len(date_list_filter)-1, on_change=select_date, key="option")]

if st.sidebar.button("Today", on_click=today):
    pass

if st.sidebar.button("All Time", on_click=all_dates):
    pass


if st.session_state.show_date == "All":
    result_display = "All Time"
else:
    result_display = datetime.datetime.strptime(st.session_state.show_date, "%Y-%m-%d").strftime('%b. %d, %Y')
st.header(f"News from {result_display}")

####################################################################################################### keyword filter
st.sidebar.header("Keyword Filter")
with st.sidebar.form("my-form"):
   st.session_state.keyword = st.text_input(label="",placeholder='Search Keyword', label_visibility="collapsed", key="text")
   submit_button = st.form_submit_button("Search")
   if st.form_submit_button('Reset', on_click=clear_text):
    st.session_state.keyword = ""



####################################################################################################### display articles
st.cache_data(ttl=3600, show_spinner=False)
def display(df):
    df = df.sort_values("date_created", ascending=False)
    for index, row in df.iterrows():
        display_date = row[1]
        display_title = row[2]
        display_topic = row[3]
        display_summary = row[4]
        display_link = row[5]
        with st.expander(f"""{display_topic}\n\n{display_title}""", expanded=True):
            st.write("")
            st.markdown(f"**Summary**: {display_summary}")
            st.link_button("Read Article", display_link)
            st.caption(display_date.strftime('%B %d, %Y')) 



####################################################################################################### tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["All", "Air", "Water", "Energy", "Pollution", "Wildlife", "Greener Living", "Environmental Law", "Climate Change"])
with tab1:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)
    
with tab2:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Air"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab3:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Water"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab4:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Energy"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab5:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Pollution"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab6:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Wildlife"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab7:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Greener Living"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab8:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Environmental Law"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

with tab9:
    date_filter = full_df["date_created"].dt.floor("D").isin(st.session_state.date)
    df = full_df[date_filter]
    df["date_created"] = pd.to_datetime(df['date_created']).dt.date 
    df = df[df["topic"]=="Climate Change"]
    df = df[(df["title"].str.contains(st.session_state.keyword, case=False)) | (df["summary"].str.contains(st.session_state.keyword, case=False))]
    display(df)

