from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

ENV = "prod"
if ENV =="dev":
  app.debug = True
  #development database
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Truongnam97@localhost/news"
else:
  app.debug = False
  #production database
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://agxmaeqprxtasv:5941d7a3ce78aac46b857f313d969ff71bac653f15a44d5e0c5cf3d2437f9626@ec2-54-162-119-125.compute-1.amazonaws.com:5432/debhgpl225jvm4"

#warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#delete cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#database object
db = SQLAlchemy(app)


  #create model
class News(db.Model):
  __tablename__ = "news"
  id = db.Column(db.Integer, primary_key=True)
  source = db.Column(db.String(200))
  date = db.Column(db.String(200))
  headline = db.Column(db.String(200))
  link = db.Column(db.String(200))

  #initializer/constructor
  def __init__(self, source, date, headline, link):
    self.source = source
    self.date = date
    self.headline = headline
    self.link = link

def scrape():
  now = datetime.now()

  ########################################### GUARDIAN ##################################################
  source_guardian = requests.get("https://www.theguardian.com/environment/all").text
  soup_guardian = BeautifulSoup(source_guardian, "lxml")

  #todays date - guardian
  date_guardian = now.strftime("%#d-%B-%Y").lower()

  print("---------- GUARDIAN ----------")
  section_guardian = soup_guardian.find("section", {"id": date_guardian})
  #header_guardian = section_guardian.a.text
  #print(header_guardian)
  try:
    for section_row in section_guardian.find_all("div", class_="fc-slice-wrapper"):
      for links in section_row.find_all("div", class_="fc-item__container"):
        for links_link in links.find_all("a", class_="u-faux-block-link__overlay js-headline-text"):
          title_guardian = links_link.text
          href_guardian = links_link.get("href")
          #insert in database
          if not db.session.query(News).filter(News.link == href_guardian).count():
            new_articles_guardian = News("guardian", now.strftime("%d %b %Y"), title_guardian, href_guardian)
            db.session.add(new_articles_guardian)
            db.session.commit()    
  except Exception as e:
    pass  
  ########################################### BBC ##################################################
  source_bbc = requests.get("https://www.bbc.com/news/topics/c4y3wxdx24nt/our-planet-now").text
  soup_bbc = BeautifulSoup(source_bbc, "lxml")

  #todays date - bbc
  date_bbc = now.strftime("%d %b")

  print("---------- BBC ----------")
  list_bbc = soup_bbc.find("ol", class_="gs-u-m0 gs-u-p0 lx-stream__feed qa-stream")
  for list_items in list_bbc.find_all("li"):
    for articles in list_items.find_all("article"):
      try:
        title_bbc = articles.find("a", class_="qa-heading-link lx-stream-post__header-link").text
        posted_bbc = articles.find("span", class_="qa-post-auto-meta").text
        href_bbc = f"https://www.bbc.com{articles.a.get('href')}"
        if len(posted_bbc) < 6: #identifies todays posts
          posted_bbc = date_bbc
        else:
          posted_bbc = ' '.join( posted_bbc.split(" ")[1:])
        if posted_bbc == date_bbc: #only retrieves todays posts
          #insert in database
          if not db.session.query(News).filter(News.link == href_bbc).count():
            new_articles_bbc = News("bbc", now.strftime("%d %b %Y"), title_bbc, href_bbc)
            db.session.add(new_articles_bbc)
            db.session.commit()
      except Exception as e:
        pass

  # ########################################### NYT ##################################################

  # #todays date - nyt
  # date_nyt = now.strftime("%b. %#d, %Y")
  # print("---------- NYT ----------")

  # from selenium import webdriver
  # url = "https://www.nytimes.com/section/climate"
  # driver = webdriver.Chrome()
  # driver.get(url)

  # c = driver.page_source
  # soup_nyt = BeautifulSoup(c, "lxml")

  # list_nyt = soup_nyt.find("div", class_="css-13mho3u")
  # try:
  #   for list_items in list_nyt.find_all("li"):
  #     title_nyt = list_items.a.h2.text
  #     posted_nyt = list_items.find("div", class_='css-n1vcs8 e1xfvim33').text
  #     href_nyt = f"https://www.nytimes.com{list_items.a.get('href')}"
  #     if posted_nyt == date_nyt: #only todays posts
  #       #insert in database
  #       #if not db.session.query(News).filter(News.link == href_nyt).count():
  #       new_articles_nyt = News("nytimes", now.strftime("%d %b %Y"), title_nyt, href_nyt)
  #       db.session.add(new_articles_nyt)
  #       db.session.commit()
  #   driver.close()
  # except Exception as e:
  #   pass  

  ########################################### CNBC ##################################################

  source_cnbc = requests.get("https://www.cnbc.com/environment/").text
  soup_cnbc = BeautifulSoup(source_cnbc, "lxml")

  #todays date - cnbc
  def suffix(d):
      return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
  def custom_strftime(format, t):
      return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))
  date_cnbc = custom_strftime('%a, %b {S} %Y', datetime.now())


  print("---------- CNBC ----------")
  section_cnbc = soup_cnbc.find("div", class_="PageBuilder-col-9 PageBuilder-col")

  try:
    for links in section_cnbc.find_all("div", class_="Layout-layout"):
      for links_links in links.find_all("div", class_="Card-textContent"):
        posted_cnbc = links_links.find("span", class_="Card-time").text
        for links_title in links_links.find_all("a", class_="Card-title"):
          title_cnbc = links_title.text
          href_cnbc = links_title.get("href")
          if len(posted_cnbc) < 15 or posted_cnbc == date_cnbc:
            posted_cnbc = date_cnbc
            #insert in database
            if not db.session.query(News).filter(News.link == href_cnbc).count():
              new_articles_cnbc = News("cnbc", now.strftime("%d %b %Y"), title_cnbc, href_cnbc)
              db.session.add(new_articles_cnbc)
              db.session.commit()
  except Exception as e:
    pass

  ########################################### ABC ##################################################

  source_abc = requests.get("https://www.abc.net.au/news/environment/").text
  soup_abc = BeautifulSoup(source_abc, "lxml")

  date_abc = now.strftime("%d %b %Y")

  print("---------- ABC ----------")
  section_abc = soup_abc.find("div", class_="_3OXQ1 _26IxR _2kxNB i69js")
  try:
    for links in section_abc.find_all("div", class_="c8CgC"):
      title_abc = links.find("h3", class_="_3mduI _2t6_4 _1deB8 jwLlj _19NQB _1GKnS _2o9MN _1-RZJ _3Kbnj _3WPmc").text
      href_part = links.find("a", class_="_3T9Id _2f8qj FQVx7 _2tPjN _1QHxY _3OwCD").get('href')
      href_abc = f"https://www.abc.net.au{href_part}"
      posted_abc = links.find("time", class_="_21SmZ _3_Aqg _1hGzz _1-RZJ P8HGV").get("datetime")
      date_time_abc = datetime.strptime(posted_abc, "%Y-%m-%dT%H:%M:%S.%fZ")
      posted_abc = date_time_abc.strftime("%d %b %Y")
      if posted_abc == date_abc:
        #insert in database
        if not db.session.query(News).filter(News.link == href_abc).count():
          new_articles_abc = News("abc", now.strftime("%d %b %Y"), title_abc, href_abc)
          db.session.add(new_articles_abc)
          db.session.commit()
  except Exception as e:
    pass 

@app.route('/')
def home():
  days = []
  news_dates = db.session.query(News).distinct(News.date)
  for dates in news_dates:
    days.append(dates.date)
  news_now = {}
  for day in days:
    news_now[day] = db.session.query(News).filter(News.date == day).all()
  #news_now = db.session.query(News).filter(News.date == day).all()
  return render_template("index.html", news_now=news_now, days=days)

#THIS WORKS!!!! NOW WHY GUARDIAN IS NOT WORKING
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
  sched = BackgroundScheduler(daemon=True)
  sched.add_jobstore('sqlalchemy', url='postgres://agxmaeqprxtasv:5941d7a3ce78aac46b857f313d969ff71bac653f15a44d5e0c5cf3d2437f9626@ec2-54-162-119-125.compute-1.amazonaws.com:5432/debhgpl225jvm4')
  sched.add_job(scrape,'interval',seconds=900)
  sched.start()

#run app
if __name__ == "__main__":
  app.run()
