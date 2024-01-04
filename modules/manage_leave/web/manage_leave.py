
# Retrive all leave records
@app.route('/retrive_tb_leave', methods=["GET"])
@login_required
@runtime_logger
def retrive_tb_leave():
    connection = app._engine.connect()
    transaction = connection.begin()
    response = {
        "rows": [],
        "total": 0,
        "message": ""
    }
    try:

        request_data = {}
        request_data['search'] = request.args.get('search')
        request_data['limit'] = request.args.get('limit', type=int)
        request_data['offset'] = request.args.get('offset', type=int)

        result_leaves = get_all_leave_info(request_data, connection)
        if result_leaves['status']:
            response['status'] = True
            response['message'] = 'Leave details retrived successfully.'
            response['rows'] = result_leaves['rows']
            response['total'] = result_leaves['total']
            return jsonify(response)
        else:
            response['message'] = result_leaves['message']
            return jsonify(response)

    except Exception as e:
        print("Error while retrieving attendance data: " + str(e))
        return jsonify(response)

# Route to approve the leave
@app.route('/approve_leave', methods=["POST"])
@login_required
@runtime_logger
def approve_leave():
    connection = app._engine.connect()
    transaction = connection.begin()
    response = {
        "status": False,
        "message": ""
    }
    try:
        request_data = request.get_json()
        request_data['approved_by'] = session['logged_user_name']
        request_data['approved_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        approve_response = approve_leave_info(request_data, connection)
        if approve_response['status'] == True:
            response['status'] = True
            response['message'] = 'Leave Approved Successfully.'
            transaction.commit()
            connection.close()
            return jsonify(response)
        else:
            response['message'] = approve_response['message']
            transaction.rollback()
            connection.close()
            return jsonify(response)
        
    except Exception as e:
        transaction.rollback()
        connection.close()
        response['message'] = "Error while approving the leave, Please contact to Admin"
        return jsonify(response)

@app.route('/manage_leave')
@login_required
@runtime_logger
def manage_leave(): 
    try:
        employees = retrive_employee ()
        return render_template('manage_leave.html', employees=employees)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/apply_leave', methods=["GET", "POST"])
@login_required
@runtime_logger
def apply_leave():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.form)
        employees = retrive_employee ()
        applied_by=employees[0]['name']
        applied_on=datetime.now().strftime('%H:%M:%S')
        from_date = datetime.strptime(data['from_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        to_date = datetime.strptime(data['to_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        existing_data = connection.execute(
            text(f"SELECT * FROM tb_leave WHERE employee_id = '{data['employee_id']}' AND from_date = '{from_date}'")).fetchone()
        
        if existing_data:
            # Duplicate entry found
            transaction.rollback()
            connection.close()
            response['message'] = "Attendance entry already exists for this employee on the given date."
            flash("Attendance entry already exists for this employee on the given date.", "error")
            return redirect('/manage_leave' )
            
        connection.execute(text(f"INSERT INTO tb_leave(`employee_id`,`from_date`,`from_shift`,`to_date`,`to_shift`,`no_of_days`,`leave_reason`,`status`,`applied_by`,`applied_on`) VALUES ('{data['employee_id']}', '{from_date}','{data['from_shift']}','{to_date}','{data['to_shift']}','{data['no_of_days']}','{data['leave_reason']}','pending','{applied_by}','{applied_on}');"))
        transaction.commit()
        connection.close()

        response['status'] = True
        response['message'] = "You have successfully mark attendance!"
        flash(response['message'], 'success')
        return redirect('/manage_leave' )
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        flash("Error while adding user. Please contact the administrator.", 'error')
        return jsonify(response)   