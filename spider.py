from urllib.request import urlopen
from find_link import LinkFinder
from general import *


class Spider:

    # class variables(shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First Spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue_set = read_file_to_set(Spider.queue_file)
        Spider.crawled_set = read_file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print('Spider' + thread_name + ' now crawling ' + page_url)
            print('Queue:' + str(len(Spider.queue_set)) + ' and Crawled:' + str(len(Spider.crawled_set)))

            Spider.add_links_to_queue(Spider.gather_link(page_url))

            Spider.crawled_set.add(page_url)
            if page_url in Spider.queue_set:
                Spider.queue_set.remove(page_url)
            Spider.update_files()

    @staticmethod
    def gather_link(page_url):
        print('gather')

        html_string = ''
        try:
            response = urlopen(page_url)
            # this if statement breaks the app. won't queue up any websites
            # I'm sure having it commented will break the program,
            # but I'm currently looking for a fix

            #if response.getheader("Content-Type") == 'text/html; charset=UTF-8':
            print('good html')
            html_bytes = response.read()
            html_string = html_bytes.decode('utf-8')

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
            print(finder.feed(html_string))
        except IOError:
            print('Error: cannot crawl')
            return set()
        return finder.page_links()

    @staticmethod
    def update_files():
        save_set_to_file(Spider.queue_file, sorted(Spider.queue_set))
        save_set_to_file(Spider.crawled_file, sorted(Spider.crawled_set))

    @staticmethod
    def add_links_to_queue(links):
        print(links)
        for url in links:
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue_set.add(url)
