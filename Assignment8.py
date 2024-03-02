# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 8 - "Complex Data Types"
# Lana Lukacevic
# Collaborated w/ class

import OutputUtil as ou
import Assignment3 as as3
import Assignment5 as as5
import json



# [2c] Create a Python function to_json(headers, data) that converts the headers and data into JSON format
def to_json(title, headers, data):
    rows = []
    for i in range(len(data)):
        s = '{' + ', '.join(['"' + headers[j] + '":"' + str(data[i][j]) + '"' for j in range(len(headers))]) + '}'
        rows.append(s)
    return '{' + '"' + title + '":[\n' + ",\n".join(rows) + ']}'


# [2b] Create a Python function to_xml(headers, data) that converts the headers and data into XML format
def xml_clean(item):
    return str(item).replace("&", "&amp;")


def to_xml(title, headers, data):
    nl = "\n"
    headers = [header.replace(" ", "") for header in headers]
    x_header = '<?xml version="1.0" encoding="UTF-8"' + '?>'
    x_title = nl + ou.create_element("title", xml_clean(title))
    content = ""
    for row in data:
        x_items = nl + "".join([ou.create_element(headers[i], xml_clean(row[i])) for i in range(len(row))])
        x_row = ou.create_element("row", x_items)
        content += x_row
    x_body = nl + ou.create_element("root", x_title + content)
    xml = x_header + x_body
    return xml



# [2a] Create a Python function to_csv(headers, data) that converts the headers and data into CSV format
def to_csv(headers, data):
    s_headers = ','.join(headers)
    s_data = '\n'.join([",".join([str(col) for col in row]) for row in data])
    return s_headers + "\n" + s_data





# [4] Create a Python function backup_table(name) that will
#
# read the contents of the table using run_query
# determine the number of rows, i.e. len(data)
# determine the number of columns, i.e. len(headers)
# use to_csv() to convert the data to CSV
# use to_xml() to convert the data to XML
# use to_json() to convert the data to JSON
# insert this information into the new backup table.
#
# Note: due to space constraints, there may be issues with logging huge inserts into the existing query table.
def backup_table(name):
    query = f"Select * from {name}"
    desc = f"Retrieve rows from {name} for backup"
    headers, data = as3.run_query(query, desc, db, assn)
    csv_data = to_csv(headers, data)
    xml_data = to_xml(name, headers, data)
    json_data = to_json(name, headers, data)
    query2 = (f"INSERT into backup (relation, num_rows, num_cols, csv_length, xml_length, json_length, csv_data, xml_data, json_data) "
              f"values ('{name}',{len(data)},{len(headers)},{len(csv_data)},{len(xml_data)},{len(json_data)},'{csv_data}','{xml_data}','{json_data}')")
    desc2 = f"Save copy of table {name} in different formats"
    headers2, data2 = as3.run_query(query2, desc2, db, assn)


# [5] Create a Python function restore_data(name, format) that will
#
# read the row of the latest backup of the table/relation name
# get the request format of that backup
# use from_csv() to convert the data from CSV back to headers and data
# use from_xml() to convert the data from XML back to headers and data
# use from_json() to convert the data from JSON back to headers and data
# makes an HTML page with the headers, and data for each of three format, each appropriately labeled (They should look similar as they were originally formed from the same data)
#
# A query to get the latest backup row for a given relation r is:
#
# SELECT * FROM backup where dtm = (SELECT MAX(dtm) FROM backup where relation = r);
def restore_data(name):
    query = f"SELECT * FROM backup where lower(relation) = '{name.lower()}' and dtm = (SELECT MAX(dtm) FROM backup where lower(relation) = '{name.lower()}')"
    desc = f"Retrieve the latest backup row for the table {name}"
    headers, data = as3.run_query(query, desc, db, assn)
    headers_csv, data_csv = from_csv(data[0][7])
    headers_xml, data_xml = from_xml(data[0][8])
    headers_json, data_json = from_json(data[0][9], name)
    tables = []
    for pair in [(headers_csv, data_csv, "CSV"), (headers_xml, data_xml, "XML"), (headers_json, data_json, "JSON")]:
        headers, data, format = pair
        title = f"Restoration of data for table {name} in {format} format"
        numeric = [all([as5.is_number(data[i][j]) for i in range(len(data))]) for j in range(len(data[0]))]
        types = ["N" if numeric[j] else "S" for j in range(len(numeric))]
        alignments = ["r" if numeric[j] else "l" for j in range(len(numeric))]
        table = [title, headers, types, alignments, data]
        tables.append(table)
    return tables

# [3a] Create a Python function from_csv(csv) that converts the csv into headers (1D) and data (2D)
def from_csv(csv):
    lines = csv.split("\n")
    headers = lines[0].split(",")
    data = [lines[1:][i-1].split(",") for i in range(1, len(lines))]
    return headers, data

# [3b] Create a Python function from_xml(xml) that converts the xml into headers (1D) and data (2D)
def from_xml(xml):
    headers = []
    data = []
    idx_row = xml.find("<row>")
    while idx_row > 0:
        idx_endrow = xml.find("</row>", idx_row)
        row = xml[idx_row+5:idx_endrow]
        elements = row.strip().split("\n")
        datum = []
        for element in elements:
            idx_begin_content = element.find(">") + 1
            idx_end_content = element.find("</")
            content = element[idx_begin_content: idx_end_content]
            datum.append(content)
            if len(headers) < len(elements):
                header = element[1:idx_begin_content-1]
                headers.append(header)
        data.append(datum)
        idx_row = xml.find("<row>", idx_endrow)
    return headers, data
# [3c] Create a Python function from_json(json) that converts the json into headers (1D) and data (2D)
def from_json(json_text, name):
    json_data = json.loads(json_text)
    headers = []
    data = []
    do_headers = True
    for items in json_data[name]:
        row = []
        for item in items:
            row.append(items[item])
            if do_headers:
                headers.append(item)
        do_headers = False
        data.append(row)
    return headers, data


assn = "Assignment 8"
db = "udb"
def main():
    # comments, queries = as5.read_queries("Assignment8.sql")
    # as5.process_queries(comments, queries, db, assn)

    udb_tables = ["advisor", "classroom", "course", "department", "instructor", "prereq", "section", "student", "takes", "teaches", "time_slot"]
    for table in udb_tables:
        backup_table(table)


    html_tables = []
    for table in udb_tables:
        html_tables += restore_data(table)
    output_file = assn.replace(" ", "") + "-restoration.html"
    title = "Restoration of all original University Database tables"
    ou.write_html_file_new(output_file, title, html_tables, True, None, True)

    comments, queries = as5.read_queries("Analytics.sql")
    as5.process_queries(comments, queries, db, assn +"a")


if __name__ == "__main__":
    main()