from os import environ

IDLE_time_s = int(environ.get("CONFIG_IDLE_TIME", "3"))
BIDABLE_time_s = int(environ.get("CONFIG_BIDABLE_TIME", "30"))
WAITING_time_s = int(environ.get("CONFIG_WAITING_TIME", "3"))
RESULTS_time_s = int(environ.get("CONFIG_RESULTS_TIME", "12"))
