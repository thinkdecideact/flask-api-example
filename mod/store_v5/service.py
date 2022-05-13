import MySQLdb as mdb
from datetime import datetime


def get_count(conn, **kwargs):
    count_cursor = conn.cursor(mdb.cursors.DictCursor)
    count_cursor.execute("SELECT COUNT(*) as row_count FROM tdar_store WHERE is_active=1 AND is_del=0")
    count_result = count_cursor.fetchone()
    return count_result['row_count']


def get_many(conn, **kwargs):
    limit_cursor = conn.cursor(mdb.cursors.DictCursor)
    # use prepared statements to bind data in order to prevent SQL injection
    limit_cursor.execute(
        "SELECT id, name, address, ctime, mtime FROM tdar_store WHERE is_active=1 AND is_del=0 ORDER BY mtime DESC, id DESC LIMIT %s,%s",
        (kwargs['offset'], kwargs['row_count_per_page'])
    )
    return limit_cursor.fetchall()


def get_one(conn, **kwargs):
    cursor = conn.cursor(mdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id, name, address, ctime, mtime FROM tdar_store WHERE is_active=1 AND is_del=0 AND id=%s",
        (kwargs['pk'],)
    )
    row = cursor.fetchone()
    if not row:
        raise Exception('No record found')
    return row


def insert(conn, **kwargs):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tdar_store (name, address, ctime, mtime) VALUES (%s, %s, %s, %s)",
        (kwargs['name'], kwargs['address'], datetime.now(), datetime.now())
    )
    return cursor.rowcount, cursor.lastrowid


def soft_delete(conn, **kwargs):
    update_cursor = conn.cursor()
    update_cursor.execute(
        "UPDATE tdar_store SET is_del=%s, mtime=%s WHERE id=%s AND is_active=1 AND is_del=0",
        (1, datetime.now(), kwargs['pk'])
    )
    return update_cursor.rowcount


def update(conn, **kwargs):
    update_cursor = conn.cursor()
    update_cursor.execute(
        "UPDATE tdar_store SET name=%s, address=%s, mtime=%s WHERE id=%s AND is_active=1 AND is_del=0",
        (kwargs['name'], kwargs['address'], datetime.now(), kwargs['pk'])
    )
    return update_cursor.rowcount


