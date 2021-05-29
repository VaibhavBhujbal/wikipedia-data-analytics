import config
from flask import Flask, jsonify, request, Response
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
mysql = MySQL(app)


def _decode_byte_type(result: tuple) -> list:
    decoded_result = []
    res = list(result)
    for i in res:
        if isinstance(i, bytes):
            st = i.decode("utf-8")  # decoded bytes values
            decoded_result.append(st)
        else:
            decoded_result.append(i)
    return decoded_result


def _convert_tuple_to_json(cur: object) -> object:
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        decoded_result = _decode_byte_type(result)  # decoded bytes
        json_data.append(dict(zip(row_headers, decoded_result)))
    return jsonify(json_data)


@app.route('/', methods=['POST'])
def query_mysql() -> object:
    error_message = {"message": ""}
    data = request.get_json(force=True)
    body_query = data.get("query")

    for command in config.FORBIDDEN_DB_COMMANDS:
        if command in body_query.lower():
            return Response("Please use Select queries only", status=400)

    try:
        cur = mysql.connection.cursor()
        cur.execute(body_query)
        return _convert_tuple_to_json(cur)
    except Exception as e:
        error_message["message"] = str(e)
        return Response(str(error_message), status=500)


@app.route('/', methods=['GET'])
def get_outdated_page() -> object:
    error_message = {"message": ""}
    category = request.args.get("category")
    category_with_underscores = category.replace(" ", "_")
    query_string = "SELECT page_id FROM outdated_pages WHERE category=%s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query_string, (category_with_underscores, ))
        return _convert_tuple_to_json(cur)
    except Exception as e:
        error_message["message"] = str(e)
        return Response(str(error_message), status=500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
