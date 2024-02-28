# from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.orarin.delete_job import del_link
from app.danych.database import engine
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
 
# # jobstores = {
# #     'default': SQLAlchemyJobStore(url="postgresql://root:root@localhost/postgres")
# # }

# scheduler = BackgroundScheduler({
#         'apscheduler.jobstores.default': {
#         'type': 'sqlalchemy',
#         'url': 'sqlite:///jobs.sqlite'
#     }
# })


from apscheduler.schedulers.background import BackgroundScheduler

# from apscheduler.jobstores import SQLAlchemyJobStore

# jobstore = {
#     'default': SQLAlchemyJobStore(engine=engine, tablename="apscheduler_jobs", tableschema="public" )
# }
scheduler = BackgroundScheduler()


# import logging
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler.add_jobstore('sqlalchemy', url="postgresql://root:root@localhost/postgres")
def hell():
    print("hello")
def add_new_job(uid: str, timestamp: datetime, sess):
    print(uid,  timestamp)
    scheduler.print_jobs()
    if scheduler.add_job(del_link, trigger='date',run_date=timestamp, args=[uid, sess]):
        return True
    else: 
        return False
    
# add_new_job("jhgfuj", "02/27/2024 22:42:00")