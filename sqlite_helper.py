from abc import ABC, abstractmethod
import sqlite3
from sqlite3.dbapi2 import PARSE_DECLTYPES
from typing import ContextManager


class Model(ABC):
    __id: int = -1
    pk: str = "id"
    table = ""

    # @abstractmethod
    # def __init__(self, table, pk):
    #     self.pk = pk
    #     self.table = table

    @staticmethod
    def get_by_key(table, key, key_value, operator):
        with sqlite3.connect(DbManager.db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            key_criteria = key_value
            if operator.upper().strip() == "LIKE":
                key_criteria = f"'{key_value}'"
            stmt = f"SELECT * FROM {table} WHERE {key} {operator} {key_criteria}"
            print("get_by_key",stmt)
            res = cursor.execute(stmt)
            return res.fetchall()

    def get_by_pk(self, pk_value):
        with sqlite3.connect(DbManager.db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            stmt = f"SELECT * FROM {self.table} WHERE {self.pk} = {pk_value}"
            print(stmt)
            cursor.execute(stmt)
            conn.commit()
            return cursor.fetchone()

    # def get_or_create(self, name):
    #     """ only works for simple table defined with 2 columns, id & name"""
    #     with sqlite3.connect(DbManager.db) as conn:
    #         cursor = conn.cursor()
    #         stmt = f"SELECT {self.pk} FROM {self.table} WHERE name LIKE '{name}'"
    #         print(stmt)
    #         cursor.execute(stmt)
    #         conn.commit()
    #         res = cursor.fetchone()
    #         if res:
    #             self.set_id(res[0])
    #         else:
    #             self.name = name
    #             self.save()

    @abstractmethod
    def get_insert_statement(self):
        ...

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    @abstractmethod
    def get_update_statement(self):
        ...

    @abstractmethod
    def get_delete_statement(self):
        ...

    @abstractmethod
    def get_select_statement(self):
        ...

    def save(self):
        with sqlite3.connect(DbManager.db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            _id = self.get_id()
            print(_id)
            stmt = self.get_insert_statement() if _id == -1 else self.get_update_statement()
            print(stmt)
            cursor.execute(stmt)
            conn.commit()
            print(f"last id: {cursor.lastrowid}")
            self.set_id(cursor.lastrowid)


class DbManager:

    db = 'test.db'

    ###################
    # TABLE - METHODS #
    ###################

    @classmethod
    def create_table_version(cls):
        """ creates the table storing the data tables versions """
        stmt = "CREATE TABLE IF NOT EXISTS table_version ('name' TEXT, version INTEGER)"
        with sqlite3.connect(DbManager.db) as sql:
            cursor = sql.cursor()
            cursor.execute(stmt)
            sql.commit()

    @classmethod
    def update_table_version(cls, table, version):
        """ sets the version of a table to a new version """
        if cls.get_table_version(table) == 0:
            stmt = f"INSERT INTO table_version (name, version) VALUES ('{table}',{version})"
        else:
            stmt = f"UPDATE table_version SET version = {version} WHERE name = '{table}'"
        with sqlite3.connect(DbManager.db) as sql:
            cursor = sql.cursor()
            cursor.execute(stmt)
            sql.commit()

    @classmethod
    def get_table_version(cls, table):
        """ returns the current table version """
        stmt = f"SELECT version FROM table_version WHERE name = '{table}'"
        with sqlite3.connect(DbManager.db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            res = cursor.execute(stmt).fetchone()
            return res['version'] if res else 0

    @classmethod
    def init_tables(cls):
        """ creates and updates the tables in the database """
        # Ensures the table_version table exists
        cls.create_table_version()

        #############
        # PET TABLE #
        #############

        if cls.get_table_version("pet") == 0:
            print("CREATING TABLE : PET")
            stmt = "CREATE TABLE IF NOT EXISTS pet ('name' TEXT, 'id' INTEGER PRIMARY KEY AUTOINCREMENT, 'birthdate' TEXT, 'gender' INTEGER, 'breed' INTEGER)"
            with sqlite3.connect(DbManager.db) as sql:
                cursor = sql.cursor()
                cursor.execute(stmt)
                sql.commit()
                cls.update_table_version("pet", 1)

        if cls.get_table_version("pet") == 1:
            print("UPDATING TABLE PET TO VERSION 2")
            stmt = "ALTER TABLE pet ADD COLUMN 'PROUT' TEXT"
            with sqlite3.connect(cls.db) as conn:
                cursor = conn.cursor()
                cursor.execute(stmt)
                conn.commit()
                cls.update_table_version("pet", 2)

        ###############
        # BREED TABLE #
        ###############

        if cls.get_table_version("breed") == 0:
            print("CREATING TABLE : BREED")
            stmt = "CREATE TABLE IF NOT EXISTS breed ('name' TEXT, 'id' INTEGER PRIMARY KEY AUTOINCREMENT)"
            with sqlite3.connect(DbManager.db) as sql:
                cursor = sql.cursor()
                cursor.execute(stmt)
                sql.commit()
                cls.update_table_version("breed", 1)

        return True

    ###################
    # MODEL - METHODS #
    ###################

    @classmethod
    def save(cls, stmt: str):
        """ Executes the statement in the parameters. If "INSERT" returns the last row id"""
        with sqlite3.connect(DbManager.db) as conn:
            cursor = conn.cursor()
            res = cursor.execute(stmt)
            print("committing save")
            conn.commit()

        if stmt.strip().upper().startswith("INSERT"):
            return res.lastrowid

    @classmethod
    def exec(cls, stmt: str):
        """ Execute the statement and returns the recordset if it's a select statement"""
        print(stmt)
        with sqlite3.connect(DbManager.db) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(stmt)
            if stmt.upper().strip().startswith('SELECT'):
                res = cursor.fetchall()
                return res
            else:
                conn.commit()
