
@app.route('/manage_home', methods=['GET'])
@login_required
@runtime_logger
def home():
    try:
        return render_template('manage_home.html')
    except Exception as e:
        print("exception while login : "+ str(e))
        return render_template('login.html')

@app.route('/manage_home_data', methods=['GET', 'POST'])
def manage_home_data():
    response = {
        "status": False,
        "message": "",
        "total": 0,
        "total_present": 0,
        "total_absent": 0,
        "total_leave": 0
    }
    
    connection =  app._engine.connect()
    transaction = connection.begin()
    try:
        data = request.get_json()
        date = data.get('date')
        date = datetime.strptime(date, "%d-%B-%Y").strftime("%Y-%m-%d")
        if not date:
            response["message"] = "Date not provided in the request."
            return jsonify(response)
        total_all = total_employee(connection)
        total_l = total_leave(date,connection)
        total_p = total_present(date, connection)
        response["total"] = total_all
        response["total_present"] = total_p
        response["total_absent"] = response["total"] - response["total_present"]
        response['total_leave'] = total_l
        response["status"] = True
        transaction.commit()
        connection.close()
        return jsonify(response)
    
    except Exception as e:
        transaction.rollback()
        connection.close()
        response["message"] = f"Error while retrieving total count: {str(e)}"
        return jsonify(response)