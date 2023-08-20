from expert.main_expert import *
from flask import Flask
import mysql.connector
from flask import Flask, jsonify, request, Blueprint
from expert.main_expert import *

app = Flask(__name__)


def create_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='maintenance'
    )


def insert_to_db(cursor, connection, user_id, question_id, fact):
    values = (user_id, question_id, fact)
    cursor.execute("INSERT INTO user_questions (user_id, question_id, fact) VALUES (%s, %s, %s)", values)
    connection.commit()


def get_facts(cursor, user_id):
    query = "SELECT * FROM user_questions WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append({
            "fact": row[3]
        })
    return data


@app.route('/match', methods=['POST'])
def diagnose():
    data = request.json
    # Get the Content-Type header from the request
    content_type = request.headers.get('Content-Type')

    # Check if the Content-Type is "application/json"
    if content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    # Get the JSON data from the request
    symptoms = data.get('bugs')
    expert = RobotCrossStreet()
    expert.reset()

    for symptom in symptoms:
        print(symptom)
        expert.declare(Symptom(symptom))
    expert.run()
    matched_rules = expert.matched_rules
    return jsonify({"rules:": matched_rules})


@app.route('/question/first', methods=["GET"])
def db():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM questions WHERE id=1')
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    data = []
    row_data = {}
    for row in rows:
        for i in range(len(columns)):
            row_data[columns[i]] = row[i]
        data.append(row_data)
    return jsonify({"first_question:": data[0]})


@app.route('/users/apply/<int:user_id>//<int:question_id>', methods=['POST'])
def get_user(user_id, question_id):
    answer = request.args.get('answer')
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM questions WHERE id = %s"
    cursor.execute(query, (question_id,))
    row = cursor.fetchall()

    key = 0
    if answer == "1":
        key = 1

    insert_to_db(cursor, connection, user_id, question_id, row[0][5])
    facts = get_facts(cursor, user_id)
    cursor.close()
    connection.close()

    if key == 1:
        if row[0][2] == 0:
            return jsonify({
                "is_done": 1,
                "message": "done, you can call the rule matcher",
                "data": {
                    "facts": facts
                }
            })
        else:
            return jsonify({
                "is_done": 0,
                "message": "go to another, yes",
                "data": {
                    "question_id": row[0][2]
                }
            })
    else:
        if row[0][3] == 0:
            return jsonify({
                "is_done": 1,
                "message": "done, you can call the rule matcher",
                "data": {
                    "facts": facts
                }
            })
        else:
            return jsonify({
                "is_done": 0,
                "message": "go to another, no",
                "data": {
                    "question_id": row[0][3]
                }
            })

    data = []
    if row:
        data.append({
            "id": row[0]
        })
    return jsonify({"Try another one: ": [user_id, question_id, row[0][5]]})


if __name__ == '__main__':
    app.run(port=8000)
