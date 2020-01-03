#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

import itchat


def send_text_msgs(text_msg_list):
    for text_msg in text_msg_list[0]:
        print("sending text message: {}".format(text_msg))

        itchat.send(text_msg, toUserName="filehelper")

        print("done")

    logout()


def send_files(src_file_path_list):
    for src_file_path in src_file_path_list[0]:
        # checks if the file exists
        if not os.path.exists(src_file_path):
            print("wechat_file_helper.py: error: file {} does not exist".format(src_file_path))
            continue
        if not os.path.isfile(src_file_path):
            print("wechat_file_helper.py: error: {} is not a file".format(src_file_path))
            continue

        print("sending file: {}".format(src_file_path))

        itchat.send_file(src_file_path, toUserName="filehelper")

        print("done")

    logout()


def receive_text_msgs():
    print("receiving text messages")

    @itchat.msg_register(itchat.content.TEXT)
    def print_content(msg):
        content = msg["Text"]

        if content == "#":  # "#" stops receiving and logs out wechat
            logout()
        else:
            print(msg["Text"])

    itchat.run()


def receive_files(dest_file_path):
    print("receiving files")

    @itchat.msg_register(["Text", "Picture", "Recording", "Attachment", "Video"])
    def download_files(msg):
        content = msg["Text"]

        if content == "#":  # "#" stops receiving and logs out wechat
            logout()
        else:
            content(os.path.join(dest_file_path, msg["FileName"]))
            print("received {}".format(msg["FileName"]))

    itchat.run()


def login():
    itchat.auto_login(enableCmdQR=2)


def logout():
    itchat.logout()


def wechat_file_helper():
    parser = argparse.ArgumentParser(description="wechat_file_helper.py - a tool for sending and receiving "
                                                 + "text messages and files from wechat file helper")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--send", "-s", action="append", nargs="+", dest="send_list",
                        help="send text messages or files")
    group.add_argument("--receive", "-r", action="store_true", help="receive text messages or files")

    parser.add_argument("--text", "-t", action="store_true", help="text messages to be sent")
    parser.add_argument("--file", "-f", action="store_true", help="files to be sent")
    parser.add_argument("--path", "-p", action="store", dest="path", default="/home/neko/Downloads/",
                        help="path for storing downloaded files")

    args = parser.parse_args()

    if args.send_list:
        # logs in wechat
        login()

        if args.text:
            # sends text messages to file helper
            send_text_msgs(args.send_list)
        elif args.file:
            # sends files to file helper
            send_files(args.send_list)
    elif args.receive:
        if args.text:
            # logs in wechat
            login()

            # receives text messages from file helper
            receive_text_msgs()
        elif args.file:
            # checks if the path exists
            if not os.path.exists(args.path):
                print("wechat_file_helper.py: error: path not exists")
                exit(1)

            # logs in wechat
            login()

            # receives files from file helper
            receive_files(args.path)


if __name__ == '__main__':
    wechat_file_helper()
