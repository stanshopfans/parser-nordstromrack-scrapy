def make_proxy_generator(path_to_proxies_file):
    with open(path_to_proxies_file, 'r') as file:
        lines = file.read().split('\n')

    def convert_line(line):
        auth = line.split(':')[-2:]
        auth = ":".join(auth)
        host_port = line.split(':')[0:2]
        host_port = ":".join(host_port)

        return f'http://{auth}@{host_port}'

    proxies = list(map(convert_line, lines))
    while True:
        for proxy in proxies:
            yield proxy


proxies_generator = make_proxy_generator('Webshare 1000 proxies.txt')