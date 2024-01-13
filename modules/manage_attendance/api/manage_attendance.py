
@app.route('/api/v2/add-attendance', methods=["POST"])
@runtime_logger
def api_add_attendance():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin()
    try:
        data = dict(request.get_json())
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

@app.route('/api/v1/get-daily-attendance', methods=['POST'])
@runtime_logger
def api_get_daily_attendance():
    response = {"status" : False, "message" : ""}
    try:
        data = dict(request.get_json())
        
        attendance_date = datetime.now().strftime('%Y-%m-%d')

        existing_data = app._engine.connect().execute(text(f"SELECT id, date_format(clock_in, '%H:%i:%S') as clock_in, date_format(clock_out, '%H:%i:%S') as clock_out, date_format(working_hours, '%H:%i:%S') as working_hours, date_format(attendance_date,'%d-%m-%Y') as attendance_date FROM tb_attendance WHERE employee_id = '{data['employee_id']}' AND attendance_date = '{attendance_date}'"))

        if existing_data.rowcount:
            row = existing_data.fetchone()
            columns = existing_data.keys()
            row_dict = dict(zip(columns, row))

        else:
            row_dict = {
                "id" : "",
                "clock_in" : "",
                "clock_out" : "",
                "working_hours" : "",
                "attendance_date" : attendance_date
            }
        return jsonify(row_dict)
    except Exception as e:
        print("Error while Clock In, Please contact administrator. : "+ str(e))
        return jsonify({})      
    