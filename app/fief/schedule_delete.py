from datetime import datetime
from app.orarin.delete_job import del_link
from apscheduler.schedulers.background import BackgroundScheduler



import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url="postgresql://root:root@localhost/postgres"
)


def add_new_job(uid: str, timestamp: datetime):
    if scheduler.add_job(del_link, trigger='date',run_date=timestamp, args=[uid]):
        return True
    else: 
        return False
