import os
from enum import Enum


class Constants(Enum):
    LOGGER_FILE_NAME = "app.log"

    LOGGING_FORMAT = "%(process)d-%(levelname)s-%(message)s"

    DATA_PATH = os.path.join("config", "car_price.csv")
