#!/usr/bin/python
from time import sleep


def read_config():
    pass


def start_async_keyboard_input():
    pass


def start_async_keylogger():
    pass


def start_async_updater():
    pass


def start_async_screen_capture():
    pass


if __name__ == '__main__':
    read_config()
    start_async_keylogger()
    start_async_screen_capture()
    start_async_updater()
    start_async_keyboard_input()
    while "queue is running":
        sleep(3600) #one hour

