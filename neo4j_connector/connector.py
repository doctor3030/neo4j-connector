import enum
import logging
import sys
from typing import Dict, Any, Callable, Optional, Tuple, List
from neo4j import GraphDatabase
from neo4j import AsyncGraphDatabase
from neo4j.work.summary import ResultSummary


class TransactionType(enum.Enum):
    READ = 'read'
    WRITE = 'write'


class ConnectorNeo4j:

    def __init__(self, uri: str, user: str, pwd: str, logger: Optional[Any]):
        self._uri = uri
        self._user = user
        self._pwd = pwd
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger()
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._pwd))
        except Exception as e:
            self._logger.error('Exception: type: {} line#: {} msg: {}'.format(sys.exc_info()[0],
                                                                              sys.exc_info()[2].tb_lineno,
                                                                              str(e)))
            print("Failed to create the driver:", e)

    def close(self):
        if self._driver:
            self._driver.close()

    def run_tx(
            self,
            tx_function: Callable,
            tx_model: Any,
            tx_type: TransactionType,
            database: Optional[str] = None,
            **kwargs
    ) -> Tuple[List[Dict], ResultSummary]:
        try:
            session = self._driver.session(database=database) if database else self._driver.session()
            if tx_type is TransactionType.READ:
                data, info = session.read_transaction(tx_function, tx_model, **kwargs)
            elif tx_type is TransactionType.WRITE:
                data, info = session.write_transaction(tx_function, tx_model, **kwargs)
            else:
                raise ValueError('Invalid transaction type {}'.format(tx_type))
            session.close()
            return data, info
        except Exception as e:
            self._logger.error('Exception: type: {} line#: {} msg: {}'.format(sys.exc_info()[0],
                                                                              sys.exc_info()[2].tb_lineno,
                                                                              str(e)))


class ConnectorNeo4jAsync:

    def __init__(self, uri: str, user: str, pwd: str, logger: Optional[Any]):
        self._uri = uri
        self._user = user
        self._pwd = pwd
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger()
        try:
            self._driver = AsyncGraphDatabase.driver(self._uri, auth=(self._user, self._pwd))
        except Exception as e:
            self._logger.error('Exception: type: {} line#: {} msg: {}'.format(sys.exc_info()[0],
                                                                              sys.exc_info()[2].tb_lineno,
                                                                              str(e)))
            print("Failed to create the driver:", e)

    async def close(self):
        if self._driver:
            await self._driver.close()

    async def run_tx(
            self,
            tx_function: Callable,
            tx_model: Any,
            tx_type: TransactionType,
            database: Optional[str] = None,
            **kwargs
    ) -> Tuple[List[Dict], ResultSummary]:
        try:
            session = self._driver.session(database=database) if database else self._driver.session()
            if tx_type is TransactionType.READ:
                data, info = await session.read_transaction(tx_function, tx_model, **kwargs)
            elif tx_type is TransactionType.WRITE:
                data, info = await session.write_transaction(tx_function, tx_model, **kwargs)
            else:
                raise ValueError('Invalid transaction type {}'.format(tx_type))
            await session.close()
            return data, info
        except Exception as e:
            self._logger.error('Exception: type: {} line#: {} msg: {}'.format(sys.exc_info()[0],
                                                                              sys.exc_info()[2].tb_lineno,
                                                                              str(e)))