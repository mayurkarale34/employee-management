
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



@app.route('/add_attendance', methods=["GET", "POST"])
@login_required
@runtime_logger
def add_attendance():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin()
    try:
        data = dict(request.form)
        attendance_date = datetime.strptime(data['date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        existing_data = connection.execute(
            text(f"SELECT * FROM tb_attendance WHERE employee_id = '{data['employee_name']}' AND date = '{attendance_date}'")).fetchone()

        if existing_data:
            # Duplicate entry found
            transaction.rollback()
            connection.close()
            response['message'] = "Attendance entry already exists for this employee on the given date."
            flash("Attendance entry already exists for this employee on the given date.", "error")
            return redirect('/manage_attendance' )
            
        connection.execute(text(f"INSERT INTO tb_attendance(`employee_id`,`date`) VALUES ('{data['employee_name']}', '{attendance_date}');"))
        transaction.commit()
        connection.close()

        response['status'] = True
        response['message'] = "You have successfully mark attendance!"
        flash(response['message'], 'success')
        return redirect('/manage_attendance' )
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        flash("Error while adding user. Please contact the administrator.", 'error')
        return jsonify(response)          
