import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/add', methods=['POST'])
def add_user():

    try:

        json = request.json
        name = json['name']
        task = json['task']

        if name and task and request.method == 'POST':

            #Initialize sql query and data
            sql = "INSERT INTO todo (name, task) VALUES (%s, %s)"
            data = (name, task)

            #Connect to db
            con = mysql.connect()
            cur = con.cursor()
            cur.execute(sql, data)
            con.commit()

            #JSON response
            resp = jsonify('Task added succesfully!')
            resp.status_code = 200
            print (resp)
            return resp
        else:

            return not_found()
            
    except Exception as e:

		print (e)
        
@app.route('/todo', methods=['GET'])
def todo():

	try:
        
		con = mysql.connect()
		cur = con.cursor()
		cur.execute("SELECT * FROM todo.todo")
		rows = cur.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp

	except Exception as e:

		return not_found(e)

@app.errorhandler(404)
def not_found(error):

    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
        'error': error
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    
    app.debug = True
    app.run(port=5001)