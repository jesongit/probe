from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

from .work import send_info
from .config import update_offset
from .utils import get_network_usage


def task():
    day = datetime.today().day
    send_offset, received_offset = get_network_usage()
    if day == 1:
        update_offset(send_offset, received_offset)
        send_info("流量重置", True)
    else:
        send_info("每日流量推送", True)


def start_task():
    scheduler = BlockingScheduler()
    trigger = CronTrigger(hour=0, minute=0, second=0)
    scheduler.add_job(task, trigger)
    scheduler.start()
    print("主进程已经启动")
