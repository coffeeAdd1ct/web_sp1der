import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

#
PROJECT_NAME = 'python'
HOMEPAGE = "https://www.python.org/"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 6
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# check if there are items in todo_queue, if so, crawl
def crawl():
    queued_links = read_file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links remaining')
        create_jobs()


# each queued link is a new job
def create_jobs():
    for link in read_file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()


# create worker threads(will die when main exits)
def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# pull next job in queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

create_spiders()
crawl()
