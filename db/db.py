# import mysql.connector
# from main import app
#

#
#
# @app.route('/fetch-data')
# def fetch_data():
#     connection = create_db_connection()
#     cursor = connection.cursor()
#
#     # Execute the SELECT query
#     cursor.execute('SELECT * FROM your_table')
#
#     # Fetch all rows
#     rows = cursor.fetchall()
#
#     # Process the fetched data
#     for row in rows:
#         # Access each column value using row[index]
#         column1_value = row[0]
#         column2_value = row[1]
#         # ...
#         print(column1_value, column2_value)
#
#     cursor.close()
#     connection.close()
#     return 'Data fetched successfully'
#
#
# @app.route('/update-data')
# def update_data():
#     connection = create_db_connection()
#     cursor = connection.cursor()
#
#     # Execute the UPDATE query
#     cursor.execute("UPDATE your_table SET column1 = 'new_value' WHERE id = 1")
#
#     # Commit the changes to the database
#     connection.commit()
#
#     cursor.close()
#     connection.close()
#     return 'Data updated successfully'
