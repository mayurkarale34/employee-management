
@app.route('/api/v2/add-attendance', methods=["POST"])
@runtime_logger
def api_add_attendance():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin()
    try:
        data = request.form.to_dict()
        data['attendance_date'] = datetime.strptime(data['clock_in_date_time'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d')
        data['clock_in_date_time'] = datetime.strptime(data['clock_in_date_time'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        add_attendance_response = add_attendance_info(data, connection)
        
        if not add_attendance_response['status']:
            response['message'] = add_attendance_response['message']
            transaction.rollback()
            connection.close()
            return jsonify(response)
        
        response['status'] = True
        response['message'] = "Attendance Marked Successfully."
        transaction.commit()
        connection.close()

        return jsonify(response)
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        transaction.rollback()
        connection.close()
        return jsonify(response)          
