
@app.route('/manage_attendance')
@login_required
@runtime_logger
def manage_attendance(): 
    try:
        employees = retrive_employee ()
        return render_template('manage_attendance.html', employees=employees)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))  
    
@app.route('/retrive_tb_attendance', methods=["GET"])
@login_required
@runtime_logger
def retrive_tb_attendance():
    connection =  app._engine.connect()
    transaction = connection.begin()
    response = {
        "rows" : [],
        "total" : 0,
        "message" : ""
    }
    try:
        request_data = {}
        request_data['search'] = request.args.get('search')
        request_data['limit'] = request.args.get('limit', type=int)
        request_data['offset'] = request.args.get('offset', type=int)
        request_data['date_filter'] = request.args.get('date_filter')
        request_data['attendance_date'] = datetime.strptime(request_data['date_filter'], '%d-%B-%Y').strftime('%Y-%m-%d')
        result_attendance = get_all_attendance_info(request_data, connection)
        if result_attendance['status']:
            response['status'] = True
            response['message'] = 'attendance details retrived successfully.'
            response['rows'] = result_attendance['rows']
            response['total'] = result_attendance['total']
            return jsonify(response)
        else:
            response['message'] = result_attendance['message']
            return jsonify(response)

    except Exception as e:
        print("Error while retrieving attendance data: " + str(e))
        return jsonify(response)



@app.route('/add_attendance', methods=["POST"])
@login_required
@runtime_logger
def add_attendance():
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
            return response
        
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
