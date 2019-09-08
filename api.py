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

            return resp
        else:

            return not_found()
            
    except Exception as e:

		print (e)

@app.route('/update', methods=['POST'])
def update_user():

    try:

        json = request.json
        id = json['id']
        name = json['name']
        task = json['task']

        if id and name and task and request.method == 'POST':

            #Connect to db
            con = mysql.connect()
            cur = con.cursor()

            sql = "SELECT * FROM todo.todo where id="+str(id)
            cur.execute(sql)
            rec = cur.fetchall()

            if len(rec) > 0:

                #Initialize sql query and data
                sql = "UPDATE todo.todo SET name=%s, task=%s WHERE id=%s"
                data = (name, task, id)

                cur.execute(sql, data)
                con.commit()

                #JSON response
                resp = jsonify('Task updated succesfully!')
                resp.status_code = 200

            
            else:
                resp = jsonify('Id does not exist!')
                resp.status_code = 404

            return resp

        else:

            return not_found()
            
    except Exception as e:

		return not_found(e)
        
@app.route('/todos', methods=['GET'])
def todos():

	try:
        
		con = mysql.connect()
		cur = con.cursor(pymysql.cursors.DictCursor)
		cur.execute("SELECT * FROM todo.todo")
		rows = cur.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200

		return resp

	except Exception as e:

		return not_found(e)

@app.route('/todo/<id>', methods=['GET'])
def todo(id):

    try:

        con = mysql.connect()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM todo.todo WHERE id= %s", id)
        row = cur.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        
        return resp
        
    except Exception as e:

        return not_found(e)

@app.route('/delete/<id>', methods=['GET'])
def delete_todo(id):

	try:

		con = mysql.connect()
		cur = con.cursor()
		cur.execute("DELETE FROM todo.todo WHERE id = %s", id)
		con.commit()
		resp = jsonify('Task deleted successfully!')
		resp.status_code = 200

		return resp

	except Exception as e:

		 return not_found(e)
		
	
@app.errorhandler(404)
def not_found(error):

    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
        'error': str(error),
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':

    app.debug = True
    app.run(port=5000)