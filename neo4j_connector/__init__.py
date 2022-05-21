from __future__ import absolute_import

__title__ = 'neo4j-connector'
__author__ = 'Dmitry Amanov'
__copyright__ = 'Copyright 2022 Dmitry Amanov'

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

from neo4j_connector.connector import ConnectorNeo4j, TransactionType

__all__ = [
    'ConnectorNeo4j', 'TransactionType'
]
