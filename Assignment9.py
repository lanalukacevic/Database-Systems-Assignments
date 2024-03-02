# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 9 - "Pivot Tables In and Outside MySQL"
# Lana Lukacevic
# Collaborated w/ class

import OutputUtil as ou
import Assignment3 as as3
import Assignment5 as as5

# SELECT product_name,
# SUM(CASE WHEN store_location = 'North' THEN num_sales ELSE 0 END) AS north,
# SUM(CASE WHEN store_location = 'Central' THEN num_sales ELSE 0 END) AS central,
# SUM(CASE WHEN store_location = 'South' THEN num_sales ELSE 0 END) AS south,
# SUM(CASE WHEN store_location = 'West' THEN num_sales ELSE 0 END) AS west
# FROM product_sales
# GROUP BY product_name;
def pivot_table(table, column_x, column_y, column_val):
    query = f"SELECT DISTINCT {column_x} FROM {table}"
    comment = f"Get all distinct values of {column_x} from {table} for pivot table"
    headers, data = as3.run_query(query, comment, db, assn)

    query_a = f"SELECT {column_y}, "
    query_b = ",\n".join([f"SUM(CASE WHEN {column_x} = '{row[0]}' THEN {column_val} ELSE 0 END) AS {row[0].replace('.','_').replace(' ','_')}" for row in data])
    query_c = f" FROM {table} GROUP BY {column_y}"

    query = query_a + query_b + query_c
    comment = f"Build a pivot table for {column_x} vs {column_y} for {table}"
    headers, data = as3.run_query(query, comment, db, assn)

    numeric = [all([as5.is_number(data[i][j]) for i in range(len(data))]) for j in range(len(data[0]))]
    types = ["N" if numeric[j] else "S" for j in range(len(numeric))]
    alignments = ["r" if numeric[j] else "l" for j in range(len(numeric))]
    table = [comment, headers, types, alignments, data]
    return table


assn = "Assignment9"
db = "udb"
def main():
    # comments, queries = as5.read_queries(assn + ".sql")
    # as5.process_queries(comments, queries, db, assn)
    examples = [["product_sales", "store_location", "product_name", "num_sales"],
                ["instructor", "dept_name", "name", "salary"]]
    html_tables = []
    for example in examples:
        html_tables += [pivot_table(example[0], example[1], example[2], example[3])]
    output_file = assn.replace(" ", "") + "-pivot-tables.html"
    title = "Pivot Tables for select examples"
    ou.write_html_file_new(output_file, title, html_tables, True, None, True)

    # comments, queries = as5.read_queries("Analytics.sql")
    # as5.process_queries(comments, queries, db, assn + "a")



if __name__ == "__main__":
    main()