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
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vbhwwdnnenfqpi:ff9bfe31416ce143706328316533d8198f12c702e6a4a11a92d6be4b91bda964@ec2-52-205-3-3.compute-1.amazonaws.com:5432/d2ipca0idtfmuo"

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


now = datetime.now()
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

# sched = BackgroundScheduler(daemon=True)
# sched.add_jobstore('sqlalchemy', url='postgres://vbhwwdnnenfqpi:ff9bfe31416ce143706328316533d8198f12c702e6a4a11a92d6be4b91bda964@ec2-52-205-3-3.compute-1.amazonaws.com:5432/d2ipca0idtfmuo')
# sched.add_job(scrape,'interval',seconds=30)
# sched.start()

#run app
if __name__ == "__main__":
  app.run()