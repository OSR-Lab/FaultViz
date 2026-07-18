# Copyright(c)  2023. Open Security Research, Inc. - All Rights Reserved

# Open Security Research, Inc. remains the sole owner of this source code copyrights,
# trademark and any applicable intellectual property.

import logging.handlers

# Create a common logger for the whole package
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# formatter: how the log will be formatted:
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Write logs on stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


from .view import (
    start_view_service,
    ViewWidget,
    csvplot,
    csvview
)
