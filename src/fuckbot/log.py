import logging
import logging.handlers
import sys

std_format = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
syslog_format = logging.Formatter(fmt='fuckbot %(levelname)s %(message)s')

def log_init(logfile=None, syslog=False, debug=False):
    if debug:
        loglvl = logging.DEBUG
    else:
        loglvl = logging.INFO

    handlers = []

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(std_format)
    handlers.append(ch)

    if logfile:
        fh = logging.FileHandler(logfile)
        fh.setFormatter(std_format)
        handlers.append(fh)

    if syslog:
        sh = logging.handlers.SysLogHandler(address="/dev/log", facility=logging.handlers.SysLogHandler.LOG_DAEMON)
        sh.setFormatter(syslog_format)
        handlers.append(sh)

    logging.basicConfig(handlers=handlers, level=loglvl, force=True)
