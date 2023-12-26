
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