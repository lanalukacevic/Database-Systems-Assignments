# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 5 - Tables, Views and Meta-data
# Lana Lukacevic
# Collaborated with class

import sys

import Assignment3 as as3
import OutputUtil as ou


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_number(x):
    return isinstance(x, int) or isinstance(x, float) or (isinstance(x, str) and is_float(x))


def process_queries(comments, queries, db, assignment):
    tables = []
    for i in range(len(queries)):
        query = queries[i]
        comment = comments[i]
        try:
            headers, data = as3.run_query(query, comment, db, assignment)
            if len(headers) == 0:
                continue
            # check if data returned is a numeric column or not
            numeric = [all([is_number(data[i][j]) for i in range(len(data))]) for j in range(len(data[0]))]
            types = ["N" if numeric[j] else "S" for j in range(len(numeric))]
            alignments = ["r" if numeric[j] else "l" for j in range(len(numeric))]
            table = [comment, headers, types, alignments, data]
            tables.append(table)
        except Exception as e:
            print(f"Error processing query: {query}\nError: {e}\n\n")
    output_file = assignment.replace(" ", "") + ".html"
    title = f"All queries for '{assignment}'"
    ou.write_html_file_new(output_file, title, tables, True, None, True)


def read_queries(file_name):
    with open(file_name, "r") as file:
        comments = []
        sqls = []
        text = file.read()
        queries = text.strip().split(";")
        for query in queries:
            if len(query.strip()) == 0:
                continue
            if "*/" in query:
                comment, sql = query.split("*/", 1)
                comment = comment.replace("/*", "").strip()
            else:
                comment = f"Query from: '{file_name}'"
                sql = query
            sql = sql.strip()
            if "CREATE FUNCTION" in sql.upper() or "CREATE PROCEDURE" in sql.upper():
                sql = sql.replace("##", ";")
            comments.append(comment)
            sqls.append(sql)
    return comments, sqls


def retrieve_query_log(assignments, db):
    global assignment
    tables = []
    for assignment in assignments:
        sql = f"SELECT * FROM query WHERE query_assn ='{assignment}'"
        desc = f"Retrieve all queries executed for {assignment}"
        headers, data = as3.run_query(sql, desc, db, assignment[-1])
        alignments = ["l"] * len(headers)
        types = ["S"] * len(headers)
        table = [desc, headers, types, alignments, data]
        tables.append(table)
    output_file = assignment.replace(" ", "") + "-query-history.html"
    title = "All queries for assignments to date"
    ou.write_html_file_new(output_file, title, tables, True, None, True)


def main():
    comments, queries = read_queries("Assignment4.sql")
    process_queries(comments, queries, "udb", "Assignment 4")

    comments, queries = read_queries("Assignment5.sql")
    process_queries(comments, queries, "udb", "Assignment 5")

    comments, queries = read_queries("Analytics.sql")
    process_queries(comments, queries, "udb", "Assignment 5 (Analytics)")

    # assignments = [f"Assignment {i}" for i in range(3, 6)]
    # retrieve_query_log(assignments, "udb")


if __name__ == "__main__":
    main()