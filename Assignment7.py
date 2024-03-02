# Queens College
# Database Systems (CSCI 331)
# Winter 2024
# Assignment 7 - "Stored Functions and Procedures"
# Lana Lukacevic
# Collaborated with class

import Assignment5 as as5

def main():
    comments, queries = as5.read_queries("Assignment7.sql")
    as5.process_queries(comments, queries, "udb", "Assignment 7")

    comments, queries = as5.read_queries("Analytics.sql")
    as5.process_queries(comments, queries, "udb", "Assignment 7 (Analytics)")


if __name__ == "__main__":
    main()