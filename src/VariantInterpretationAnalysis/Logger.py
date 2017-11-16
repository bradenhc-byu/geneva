################################################################################
# Simple logger
#
# Logs information to stdout or to a file, depending on the source
#
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

MESSAGE_PREFIX = "{0} ".format(datetime.datetime.fromtimestamp(time.time())
                              .strftime('%Y-%m-%d %H:%M:%S'))

# Singleton variables
logger_level = LEVEL_DEBUG
logger_destination = DEST_STDOUT
logger_output_file = OUT_FILE

# Create the log file if it doesn't exist
if not os.path.exists(OUT_FILE):
    f = open(OUT_FILE, "w+")
    f.close()

def set_log_level(level):
    if level < LEVEL_DEBUG or level > LEVEL_ERROR:
        return False
    logger_level = level
    return True

def set_destination(dest):
    if dest != DEST_STDOUT \
       or dest != DEST_FILE:
        return False
    logger_destination = dest
    return True

def debug(message):
    if logger_level == LEVEL_DEBUG:
        log_message = MESSAGE_PREFIX + "[DEBUG]: " + message
        if logger_destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(logger_output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def info(message):
    if logger_level <= LEVEL_INFO:
        log_message = MESSAGE_PREFIX + "[INFO]: " + message
        if logger_destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(logger_output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def warn(message):
    if logger_level <= LEVEL_WARN:
        log_message = MESSAGE_PREFIX + "[WARN]: " + message
        if logger_destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(logger_output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()

def error(message):
    if logger_level <= LEVEL_ERROR:
        log_message = MESSAGE_PREFIX + "[ERROR]: " + message
        if logger_destination == DEST_STDOUT:
            print log_message
        else:
            outfile = open(logger_output_file, "a")
            outfile.write(log_message + "\n")
            outfile.close()
