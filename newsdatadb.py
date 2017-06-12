#!/usr/bin/env python3
import psycopg2

# Question 1: What are the three most popular articles of all time?
SQLQuery1_Title = "What are the three most popular articles of all time?"

SQLQuery1 = (
    "select articles.title, count(*) as views"
    "from articles inner join log on log.path"
    "like concat('%', articles.slug, '%')"
    "where log.status like '%200 group by  "
    "articles.title, log path order by views desc limit 3"
    )

#Question 2: What are the three most popular article authors of all time?
SQLQuery2_Title = "Who are the most popular article authors of all time?"

SQLQuery2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') where "
    "log.status like '%200%' group "
    "by authors.name order by views desc")
    )

#Question 3: On which days did more than 1% of requests lead to errors?
SQLQuery3_Title = "On which days did more than 1% of requests lead to errors?"

SQLQuery3 =(
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1"
    )

#Connect to database, or return error
def connect(database_name="newsdata"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return = db, cursor
    except:
        print (Cannot connect to database... something has clearly gone terribly wrong!)

#Gather query results
def query_results(query):
    db, cursor = connect()
    cursor.execute(query)
    return cursor.fetchall()
    db close()

# Display query results
def display_results(query_results):
    print(query_results[1])
    for index, results in eneumerate(query_results[0]):
        print (
            "\t", results[0], "-",str(results[1]) + "% errors")

#Display errors
def print_errors(query_results):
    print (query_results[1])
    for results in query_results[0]:
        print ("\t", results[0], "-", str(results[1]) + "% errors")

#Store queries
if __name__ == '__main__':
    popular_articles_results = get_query_results(query_1), query_1_title
    popular_authors_results = get_query_results(query_2), query_2_title
    load_error_days = get_query_results(query_3), query_3_title

# Print query results
    print_query_results(popular_articles_results)
    print_query_results(popular_authors_results)
    print_error_results(load_error_days)