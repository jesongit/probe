from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

from .work import send_info
from .config import update_offset
from .utils import get_network_usage


def task():
    send_offset, received_offset = get_network_usage()
    update_offset(send_offset, received_offset)
    send_info("流量重置", True)


def start_task():
    scheduler = BlockingScheduler()
    trigger = CronTrigger(day=1, hour=0, minute=0)
    scheduler.add_job(task, trigger)
    scheduler.start()
    print("主进程已经启动")
