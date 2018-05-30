import os


# each website we crawl is a seperate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('creating project ' + directory)
        os.makedirs(directory)


# create queue and crawled files directories (if not exists)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'

    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, base_url)


# creates a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# add data to existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# delete teh contents of a file
def remove_from_file(path):
    with open(path, 'w'):
        pass


# how to convert links in file to set
def read_file_to_set(filename):
    results = set()
    with open(filename, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# how to save set to file
def save_set_to_file(filename, links):
    remove_from_file(filename)
    for link in sorted(links):
        append_to_file(filename, link)
