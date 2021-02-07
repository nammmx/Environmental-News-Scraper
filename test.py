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
          #if not db.session.query(News).filter(News.link == href_guardian).count():
          new_articles_guardian = News("guardian", now.strftime("%d %b %Y"), title_guardian, href_guardian)
          db.session.add(new_articles_guardian)
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

sched = BackgroundScheduler(daemon=True)
sched.add_jobstore('sqlalchemy', url='postgres://vbhwwdnnenfqpi:ff9bfe31416ce143706328316533d8198f12c702e6a4a11a92d6be4b91bda964@ec2-52-205-3-3.compute-1.amazonaws.com:5432/d2ipca0idtfmuo')
sched.add_job(scrape,'interval',seconds=30)
sched.start()

#run app
if __name__ == "__main__":
  app.run()