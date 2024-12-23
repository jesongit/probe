import time
import threading
from .config import CONFIG
from .utils import get_network_usage, parse
from .wechat import notify


def check_rate(pre, cur):
    return cur > 85 and int(pre) < int(cur)


def send_info(title, need_notify=False):
    total_send, total_received = get_network_usage()
    month_limit = parse(CONFIG["total"])
    soffset = CONFIG["send_offset"]
    roffset = CONFIG["received_offset"]
    month_used = total_send - soffset + total_received - roffset
    print(month_used, total_send, total_received, soffset, roffset)
    pre_rate = CONFIG["rate"]
    CONFIG["rate"] = rate = month_used / month_limit * 100

    notify_str = (
        f"send: {format(total_send)} received: {format(total_received)}\n"
        f"used: {format(month_used)} remain: {format(month_limit - month_used)} {rate :.2f}%"
    )
    if need_notify or check_rate(pre_rate, rate):
        notify(title, notify_str)


def loop():
    send_info("流量进程启动", True)
    while True:
        time.sleep(1)
        send_info("流量阈值告警", False)


def start_worker():
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    print("监控进程已启动")
