import pymysql

DB_HOST = "211.103.136.244"
DB_PORT = 7068
DB_USER = "student"
DB_PASSWORD = "your_db_password"
DB_NAME = "huike"
DB_CHARSET = "utf8"


def get_conn():
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    return conn


def query_one(sql, params=None):
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, params)
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def query_all(sql, params=None):
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute(sql, params=None):
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        rows = cursor.execute(sql, params)
        conn.commit()
        return rows
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    result = query_one("SELECT * FROM sys_user WHERE user_name=%s LIMIT 1", ("admin",))
    print(result)