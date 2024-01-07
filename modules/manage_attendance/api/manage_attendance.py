
@app.route('/api/v2/add-attendance', methods=["POST"])
@runtime_logger
def api_add_attendance():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin()
    try:
        data = dict(request.get_json())
        print(data)
        data['clock_time']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['attendance_date'] = datetime.now().strftime('%Y-%m-%d')

        add_attendance_response = add_attendance_info(data, connection)
        
        if not add_attendance_response['status']:
            response['message'] = add_attendance_response['message']
            transaction.rollback()
            connection.close()
            return jsonify(response)
        
        response['status'] = True
        response['message'] = add_attendance_response['message']
        transaction.commit()
        connection.close()

        return jsonify(response)
    except Exception as e:
        print("Error while Clock In, Please contact administrator. : "+ str(e))
        transaction.rollback()
        connection.close()
        return jsonify(response)          
