# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import config

__log_name = f"logs/{datetime.now().strftime("%d-%m-%Y_%H-%M")}.log"
logging.basicConfig(
    filename=__log_name,
    format="[%(asctime)s] [%(name)s:%(levelname)s]: %(message)s",
    level=logging.DEBUG if config.debug else logging.INFO,
    encoding="utf-8"
)

logger = logging.getLogger()
