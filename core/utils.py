import psutil
from datetime import datetime


def format(bytes_size):
    """
    将字节数转换为适当的单位（KB, MB, GB, TB）
    :param bytes_size: 字节数
    :return: 格式化后的字符串（例如 "10.5 MB"）
    """
    # 定义流量单位的列表
    units = ["Bytes", "KB", "MB", "GB", "TB"]

    # 找到合适的单位
    for unit in units:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024


def parse(size_str):
    """
    将带单位的字符串（如 '10 KB', '3.5 MB'）转换为字节数
    :param size_str: 带单位的流量字符串（如 '10 KB', '3.5 MB'）
    :return: 对应的字节数
    """
    # 定义单位与换算值的字典
    unit_mapping = {"Bytes": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}

    # 去除字符串两端的空白字符并转换为大写
    size_str = size_str.strip().upper()

    # 提取数字和单位
    for unit in unit_mapping:
        if unit in size_str:
            # 提取数字部分
            number_str = size_str.replace(unit, "").strip()
            try:
                number = float(number_str)  # 转换为数字
                return number * unit_mapping[unit]  # 转换为字节数
            except ValueError:
                raise ValueError("无效的数字格式")

    # 如果没有找到单位
    raise ValueError("未知的单位")


def get_network_usage(interface="eth0"):
    net_io = psutil.net_io_counters(pernic=True)
    interface_io = net_io[interface]
    send = interface_io.bytes_sent  # B
    received = interface_io.bytes_recv  # B
    return send, received


def now():
    return int(datetime.now().timestamp())
