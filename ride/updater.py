from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_ride_location


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_ride_location, 'interval', seconds=25)
    scheduler.start()
