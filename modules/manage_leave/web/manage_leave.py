

@app.route('/manage_leave')
@login_required
@runtime_logger
def manage_leave(): 
    try:
        employees = retrive_employee ()
        return render_template('manage_leave.html', employees=employees)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

# Retrive all leave records
@app.route('/retrive_tb_leave', methods=["GET"])
@login_required
@runtime_logger
def retrive_tb_leave():
    response = {
        "rows": [],
        "total": 0,
        "message": ""
    }
    try:

        request_data = {}
        request_data['search'] = request.args.get('search')
        request_data['status'] = request.args.get('status')
        request_data['limit'] = request.args.get('limit', type=int)
        request_data['offset'] = request.args.get('offset', type=int)

        result_leaves = get_all_leave_info(request_data, app._engine.connect())
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
        print("Error while retrieving leave data: " + str(e))
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

@app.route('/apply_leave', methods=["GET", "POST"])
@login_required
@runtime_logger
def apply_leave():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.form)
        data['applied_by'] = session.get('logged_user_name', 'Default')
        data['applied_on']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['from_date'] = datetime.strptime(data['from_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        data['to_date'] = datetime.strptime(data['to_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        
        application_response = apply_for_leave_info(data, connection)
        if not application_response['status']:
            transaction.rollback()
            connection.close()
            response['message'] = application_response['message']
            return jsonify(response)
        
        leave_deduction_response = deduct_leave_balances(data['employee_id'], data['leave_type'], data['no_of_days'],connection)
        if not leave_deduction_response['status']:
            connection.close()
            response['message'] = leave_deduction_response['message']
            return jsonify(response)
        
        transaction.commit()
        connection.close()
        response['status'] = True
        response['message'] = "Leave Applied Successfully."
        return jsonify(response)
    
    except Exception as e:
        transaction.rollback()
        connection.close()
        message = "Error while adding user, Please contact administrator. : "+ str(e)
        print(message)
        response['message'] = message
        return jsonify(response)   
    