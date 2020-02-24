
from sys import stderr, stdout


def log_error(*args):
    for error in args:
        log("***ERROR***: " + error, out_stream=stderr)


def log_message(*args):
    for message in args:
        log("*Message*: " + message)


def log(string, out_stream=stdout):
    print(string, file=out_stream)

