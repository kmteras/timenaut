import logging

import PySide2.QtSql as QtSql

from core.models.process_heartbeat import ProcessHeartbeat
from timewire.core.models.process import Process
from timewire.core.models.window import Window
from timewire.util.database_error import DatabaseError
from timewire.util.util import get_data_file_location


def connect() -> None:
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(get_data_file_location())

    if not db.open():
        raise DatabaseError("Could not open database!")

    logging.info(f"Connected to database {get_data_file_location()}")
    try:
        create_tables()
    except DatabaseError as e:
        logging.error(e)
        raise DatabaseError("Error creating tables")


def create_tables() -> None:
    query = QtSql.QSqlQuery()
    if not query.exec_("PRAGMA foreign_keys = ON;"):
        raise DatabaseError(query.lastError())

    if not query.exec_("CREATE TABLE IF NOT EXISTS processes("
                       "id INTEGER PRIMARY KEY, "
                       "path TEXT NOT NULL);"):
        raise DatabaseError(query.lastError())

    if not query.exec_("CREATE TABLE IF NOT EXISTS windows("
                       "id INTEGER PRIMARY KEY, "
                       "process_id INTEGER NOT NULL, "
                       "title TEXT NOT NULL,"
                       "FOREIGN KEY (process_id) REFERENCES processes(id));"):
        raise DatabaseError(query.lastError())

    if not query.exec_("CREATE TABLE IF NOT EXISTS heartbeats("
                       "process_id INTEGER NOT NULL,"
                       "window_id INTEGER NOT NULL,"
                       "datetime INTEGER NOT NULL,"
                       "FOREIGN KEY (process_id) REFERENCES processes(id), "
                       "FOREIGN KEY (window_id) REFERENCES windows(id));"):
        raise DatabaseError(query.lastError())
    logging.info("Created database tables")


def add_process(process: Process) -> int:
    query = QtSql.QSqlQuery()

    # Check if the process already exists in the database
    query.prepare("SELECT * FROM processes WHERE path = :path")
    query.bindValue(":path", process.path)
    if not query.exec_():
        raise DatabaseError(query.lastError())
    else:
        # If the process already exists
        if query.next():
            return query.value(0)

    query.prepare("INSERT INTO processes (path) VALUES (:path)")
    query.bindValue(":path", process.path)
    if not query.exec_():
        raise DatabaseError(query.lastError())
    else:
        return query.lastInsertId()


def add_window(window: Window, process_id: int) -> int:
    query = QtSql.QSqlQuery()

    # Check if the window already exists in the database
    query.prepare("SELECT * FROM windows WHERE title = :title")
    query.bindValue(":title", window.title)
    if not query.exec_():
        raise DatabaseError(query.lastError())
    else:
        # If the window already exists
        if query.next():
            return query.value(0)

    query.prepare("INSERT INTO windows (title, process_id) VALUES (:title, :process_id)")
    query.bindValue(":title", window.title)
    query.bindValue(":process_id", process_id)
    if not query.exec_():
        raise DatabaseError(query.lastError())
    else:
        return query.lastInsertId()


def add_heartbeat(heartbeat: ProcessHeartbeat) -> None:
    process_id = add_process(heartbeat.process)
    window_id = add_window(heartbeat.window, process_id)

    query = QtSql.QSqlQuery()

    query.prepare(
        "INSERT INTO heartbeats (process_id, window_id, datetime) VALUES (:process_id, :window_id, :datetime)")
    query.bindValue(":process_id", process_id)
    query.bindValue(":window_id", window_id)
    query.bindValue(":datetime", int(heartbeat.time))
    if not query.exec_():
        raise DatabaseError(query.lastError())
