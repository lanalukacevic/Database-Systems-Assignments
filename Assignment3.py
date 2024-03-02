# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 3 - SQL and Programming Languages
# Lana
# Collaborated with class

import pymysql
import time
import texttable


# creates a function to read our password
def get_password():
    with open('password.txt', 'r') as file:
        return file.read().strip()


password = get_password()
user = "Lana"


def list_db_data(cursor, sql, desc):
    cursor.execute(sql)
    results = [row[0] for row in cursor]
    print(desc + ":", results)
    return results


def log_query(query_text, query_desc, query_db, query_rows, query_user, query_assn, query_dur, conn=None):
    query_text = query_text.replace("'", "\\'")
    query_desc = query_desc.replace("'", "\\'")
    # f string enables you to format nicely
    query = f"INSERT into query (query_text, query_desc, query_db, query_rows, query_user, query_assn, query_dur) \nvalues ('{query_text} ',' {query_desc}','{query_db}',{query_rows},'{query_user}','{query_assn}',{query_dur})"
    new_conn = False
    if conn is None:
        new_conn = True
        conn = pymysql.connect(host="localhost", user="root", passwd=password, db="udb")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    if new_conn:
        conn.close()


def run_query(query_text, query_desc, query_db, assignment):
    query_src = assignment
    conn = pymysql.connect(host="localhost", user="root", passwd=password, db=query_db)
    start = time.time()
    cursor = conn.cursor()
    cursor.execute(query_text)
    end = time.time()
    duration = end - start
    rows = cursor.fetchall()
    conn.commit()
    log_query(query_text, query_desc, query_db, len(rows), user, query_src, duration)
    conn.close()
    query_upper = query_text.upper()
    if query_upper.startswith("SELECT") or query_upper.startswith("SHOW") or query_upper.startswith("DESC"):
        headers = [desc[0] for desc in cursor.description]
        if len(rows) == 0:
            data = [[None for _ in headers]]
        else:
            data = [[col for col in row] for row in rows]
        return headers, data
    else:
        return [], []


def print_table(title, headers, data, alignments=None):
    if alignments is None:
        alignments = ['l'] * len(headers)
    tt = texttable.Texttable(0)
    tt.set_cols_align(alignments)
    tt.add_rows([headers] + data, header=True)
    print(title)
    print(tt.draw())
    print()


def preliminary(password):
    conn = pymysql.connect(host="localhost", user="root", passwd=password)
    cursor = conn.cursor()
    # gives us a list of  all the databases that we have
    databases = list_db_data(cursor, "SHOW DATABASES", "Databases")
    cursor.execute("USE udb")
    tables = list_db_data(cursor, "SHOW TABLES", "Tables in udb")
    for table in tables:
        columns = list_db_data(cursor, "DESC " + table, "Columns in table " + table)
    conn.close()
    return tables


def main():
    assignment = "Assignment 3"
    tables = preliminary(password)
    for table in tables:
        query = "SELECT * FROM " + table
        desc = "Retrieve all rows from table " + table
        db = "udb"
        headers, data = run_query(query, desc, db, assignment)
        print_table("table " + table, headers, data)


if __name__ == "__main__":
    main()