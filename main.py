from core import work
from core import master

if __name__ == "__main__":
    work.start_worker()
    master.start_task()
