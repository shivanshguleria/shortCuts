from datetime import datetime
from app.orarin.delete_job import del_link
from apscheduler.schedulers.background import BackgroundScheduler
from app.danych.get_cred import Credentials


# import logging
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url=Credentials.postgres
)


def add_new_job(uid: str, timestamp: datetime):
    if timestamp.utctimetuple() >= datetime.utcnow().utctimetuple(): 
        scheduler.add_job(del_link, trigger='date',run_date=timestamp, args=[uid])
        return True
    else: 
        print("[INFO] scheduler_delete routine is returning false")
        return False
