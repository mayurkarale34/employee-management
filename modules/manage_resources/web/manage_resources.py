

@app.route('/resource', methods=['GET', 'POST'])
@login_required
@runtime_logger
def resource():
   try:
        role_options = retrive_metadata_by_type("role")
        return render_template('resource.html', role_options=role_options)
   except Exception as e:
        print("Error while fetching role options: " + str(e))
        # Handle the error gracefully, perhaps redirect to an error page or return an appropriate response
        return render_template('error.html', error_message="An error occurred.")  

@app.route('/retrive_user_master', methods=["GET"])
@login_required
@runtime_logger
def retrive_user_master():
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

        result_tluser = get_all_tluser_info(request_data, connection)
        if result_tluser['status']:
            response['status'] = True
            response['message'] = 'user details retrived successfully.'
            response['rows'] = result_tluser['rows']
            response['total'] = result_tluser['total']
            return jsonify(response)
        else:
            response['message'] = result_tluser['message']
            return jsonify(response)

    except Exception as e:
        print("Error while retrieving user data: " + str(e))
        return jsonify(response)
    
@app.route('/update_user', methods=["GET", "POST"])
@login_required
@runtime_logger
def update_user():
    connection =  app._engine.connect()
    transaction = connection.begin()
    try:
        data = dict(request.form)
        query = text(f"update tluser set first_name = '{data['edit_first_name']}', last_name = '{data['edit_last_name']}', contact_no = '{data['edit_contact_no']}', email_id = '{data['edit_email_id']}', role = '{data['edit_role']}', status = '{data['edit_status']}'  where id = '{data['id']}';")
        connection.execute(query)
        transaction.commit()
        connection.close()
        return redirect('/resource')
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("Error while updating user : "+ str(e))
        return redirect('/resource')             