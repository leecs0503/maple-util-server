import abc


class BaseDB(abc.ABC):
    def __init__(*args, **kwargs):
        pass

    @abc.abstractmethod
    def insert_query(
        self,
        sql: str,
        args: dict,
    ):
        pass

    @abc.abstractmethod
    def select_query(
        self,
        sql: str,
        args: dict,
    ):
        pass

    @abc.abstractmethod
    def update_query(
        self,
        sql: str,
        args: dict,
    ):
        pass

    @abc.abstractmethod
    def delete_query(
        self,
        sql: str,
        args: dict,
    ):
        pass