"""
Logger Module

Provides a very simple logging interface to use in GeneVA
"""
import os
import time
import datetime


# Constants
DEST_STDOUT = 0
DEST_FILE = 1
LEVEL_DEBUG = 0
LEVEL_INFO = 1
LEVEL_WARN = 2
LEVEL_ERROR = 3

OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "out.log")

def message_prefix():
    return "{0} ".format(datetime.datetime.fromtimestamp(time.time())
                              .strftime('%Y-%m-%d %H:%M:%S'))


class LogSettings:
    def __init__(self):
        self.level = LEVEL_DEBUG
        self.destination = DEST_STDOUT
        self.output_file = OUT_FILE
        self.enabled = True

log_settings = LogSettings()

# Create the log file if it doesn't exist
if not os.path.exists(OUT_FILE):
    f = open(OUT_FILE, "w+")
    f.close()

def enable(settings=log_settings):
    settings.enabled = True

def disable(settings=log_settings):
    settings.enabled = False

def set_log_level(level, settings=log_settings):
    levels = {
        "debug": LEVEL_DEBUG,
        "info": LEVEL_INFO,
        "warn": LEVEL_WARN,
        "error": LEVEL_ERROR
    }
    if level not in levels.keys():
        info("Invalid command. Log level unchanged.")
        return False
    settings.level = levels[level]
    info("Log level set to " + level)
    return True

def set_destination(dest, settings=log_settings):
    destinations = {
        "stdout": DEST_STDOUT,
        "file": DEST_FILE
    }
    if dest not in destinations.keys():
        return False
    settings.destination = destinations[dest]
    return True

def set_file(log_file, settings=log_settings):
    if not os.path.exists(log_file):
        new_file = open(log_file, "w+")
        new_file.close()
    settings.output_file = log_file
    return True


def debug(message, settings=log_settings):
    if settings.level == LEVEL_DEBUG and settings.enabled:
        log_message = message_prefix() + "[DEBUG]: " + message
        if settings.destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(settings.output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def info(message, settings=log_settings):
    if settings.level <= LEVEL_INFO and settings.enabled:
        log_message = message_prefix() + "[INFO]: " + message
        if settings.destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(settings.output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def warn(message, settings=log_settings):
    if settings.level <= LEVEL_WARN and settings.enabled:
        log_message = message_prefix() + "[WARN]: " + message
        if settings.destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(settings.output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def error(message, settings=log_settings):
    if settings.level <= LEVEL_ERROR and settings.enabled:
        log_message = message_prefix() + "[ERROR]: " + message
        if settings.destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(settings.output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()