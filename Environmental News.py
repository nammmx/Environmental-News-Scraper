import streamlit as st
import psycopg2
import pandas as pd
from PIL import Image
import datetime

st.set_page_config(layout="wide")

st.markdown('''
<style>
div.stButton > button:first-child {
    width: 200px;
    background-color: rgba(23, 48, 28, 0.95) ;
    color: #f5e1d5;
}

div.stLinkButton > a:first-child {
    width: 105px;
    background-color: rgba(23, 48, 28, 0.95) ;

}
div.stLinkButton p {
    font-size: 14px;
    color: #f5e1d5;
}
section[data-testid="stSidebar"] {
    top: 6rem;
    width: 250px !important; 
    background-color: rgb(247, 250, 248) ;
}
div[data-testid="collapsedControl"] {
    top:6.5rem;
}
div[data-testid="stExpander"] {
    background-color: rgb(247, 250, 248) ;
    border: 0px solid black;
}
.st-emotion-cache-yf5hy5 p:nth-child(1){
    font-size: 16px;
    color: green;
}
.st-emotion-cache-yf5hy5 p:nth-child(2) {
    font-size: 25px;
    font-weight: 700;
}
header[data-testid="stHeader"] {
    background: url('https://res.cloudinary.com/drwsupfyj/image/upload/v1699907190/dailysql/vzhlmqtme1lx09jab4rt.png');
    background-size: contain, cover;
    height: 6rem;
}
.st-emotion-cache-z5fcl4 {
    padding: 5.5rem 1rem 0rem;
}
.st-emotion-cache-16txtl3 {
    padding: 1.5rem 1.5rem;
}
.st-dn {
    background-color: whitesmoke;
}
div[data-testid="textInputRootElement"] {
    border: 1px solid rgba(23, 48, 28, 0.95);
}
.st-emotion-cache-1aqpwna {
    border: 0px;
    padding:0;
}
.css-pxxe24 {
visibility: hidden;
}

</style>
''', unsafe_allow_html=True)



hostname = 'localhost'
database = 'environmentalnewsscraper'
username = 'environmentalnewsscraper_admin'
port_id = '5432'
pwd = 'environmentalnewsscraper1997'

#st.title('Environmental News')

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


####################################################################################################### date filters
min_date = datetime.date(2023,11,6)
max_date = datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)

date_list = pd.date_range(min_date,max_date + datetime.timedelta(days=1)-datetime.timedelta(days=1),freq='d').to_list()
date_list = [date_obj.strftime("%Y-%m-%d %H:%M:%S") for date_obj in date_list]

lst1 = []
lst1.append(date_list)
for i in range(0,len(date_list)):
    lst1.append(date_list[i])


if 'count' not in st.session_state:
    st.session_state.count = len(date_list)

def display_date():
    lst = []
    if st.session_state.count == 0:
        for i in range(0, len(lst1[0])):
            lst.append(lst1[0][i])
        lst = tuple(lst)
        show_date = "All"
    else:
        date = lst1[st.session_state.count]
        #st.write(date)
        lst.append(date)
        lst.append( date_list[0])
        lst = tuple(lst)
        show_date = lst[0]
    return lst, show_date
    
def next_date():
    if st.session_state.count == 0:
        st.session_state.count += len(date_list)
    elif st.session_state.count + 1 >= len(date_list)+1:
        pass
    else:
        st.session_state.count += 1

def previous_date():
    if st.session_state.count == 0:
        st.session_state.count += len(date_list)
    elif st.session_state.count > 1:
        st.session_state.count -= 1

def all_date():
    st.session_state.count = 0

def today():
    st.session_state.count = len(date_list)


result = display_date()
if result[1] == "All":
    result_display = "All Time"
else:
    result_display = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S").strftime('%B %d, %Y')

st.title(f"Environmental News from {result_display}")
st.sidebar.header("Date Filter")
if st.sidebar.button("Today", on_click=today):
    pass
if st.sidebar.button("All Time", on_click=all_date):
    pass
if st.sidebar.button("Previous Day", on_click=previous_date):
    pass
if st.sidebar.button("Next Day", on_click=next_date):
    pass

####################################################################################################### keyword filter
st.sidebar.header("Keyword Filter")
with st.sidebar.form("my-form"):
   keyword = st.text_input(label="",placeholder='Search Keyword', label_visibility="collapsed")
   submit_button = st.form_submit_button("Search")
   if st.form_submit_button('Reset'):
    keyword = ""



####################################################################################################### display articles
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
    df = execute_query(query = f"""
                SELECT news_id,  date_created::date, title, topic, summary, link FROM news WHERE DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    #st.dataframe(df)
    display(df)
    
with tab2:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Air' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab3:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Water' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab4:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Energy' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab5:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Pollution' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab6:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Wildlife' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab7:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Greener Living' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab8:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Environmental Law' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

with tab9:
    df = execute_query(query = f"""
                SELECT news_id, date_created::date, title, topic, summary, link FROM news WHERE topic = 'Climate Change' AND DATE_TRUNC('day', date_created) IN {result[0]} AND (title ILIKE '%{keyword}%' OR summary ILIKE '%{keyword}%');
                """, hostname=hostname, database=database, username=username, port_id=port_id, pwd=pwd)
    display(df)

