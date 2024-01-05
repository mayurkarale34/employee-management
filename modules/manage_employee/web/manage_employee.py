
@app.route('/add_user', methods=['POST'])
@login_required
@runtime_logger
def add_user():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.form)
        request_data = {
            "first_name" : data['first_name'],
            "last_name" : data['last_name']
        }
        data['employee_id'] = generate_employee_id(request_data)
        
        connection.execute(text(f"INSERT INTO tb_manage_employee(`employee_id`, `first_name`, `middle_name`, `last_name`, `email_id`, `contact`, `gender`, `city`, `Country`, `aadhar_number`, `birth_date`, `blood_group`, `pan_number`, `total_experience`, `designation`, `employee_type`, `joining_date`, `current_address`, `permanent_address`) VALUES ('{data['employee_id']}', '{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['email_id']}', '{data['contact']}', '{data['gender']}', '{data['city']}', '{data['Country']}', '{data['aadhar_number']}', '{data['birth_date']}', '{data['blood_group']}', '{data['pan_number']}','{data['total_experience']}','{data['designation']}', '{data['employee_type']}', '{data['joining_date']}', '{data['current_address']}', '{data['permanent_address']}');"))
        transaction.commit()
        connection.close()

        response['status'] = True
        response['message'] = "You have successfully added user!"
        return jsonify(response)
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        return jsonify(response)
    
@app.route('/employee_management')
@login_required
@runtime_logger
def employee_management():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('employee_management.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))
    
@app.route('/retrive_tb_manage_employee', methods=["GET"])
@login_required
@runtime_logger
def retrive_tb_manage_employee():
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

        result_manage_employee = get_all_employee_info(request_data, connection)
        if result_manage_employee['status']:
            response['status'] = True
            response['message'] = 'employee details retrived successfully.'
            response['rows'] = result_manage_employee['rows']
            response['total'] = result_manage_employee['total']
            return jsonify(response)
        else:
            response['message'] = result_manage_employee['message']
            return jsonify(response)

    except Exception as e:
        print("Error while retrieving employee data: " + str(e))
        return jsonify(response)

# Get teh employee details as per the feature filter for select2
@app.route('/get_employees', methods = ["GET"])
@runtime_logger
def get_employees():
	response = {"total": 0, "data":[]}
	employee_list = []
	try:
		search_val = request.args.get('search')
		page_no = request.args.get('page_no')
		limit = request.args.get('page_size')
		offset = int(page_no) * int(limit)

		data = {}
		data['limit'] = limit
		data['offset'] = offset
		data['search_val'] = search_val
		data['employee_status'] = "All"

		employee_data = get_all_employees(data)
		
		for employee in employee_data['rows']:
			employee_list.append({
                        "id":employee['employee_id'],
                        "text": '(' + employee['employee_id'] + ') ' + employee['employee_name']
                    })
		response['total'] = employee_data['total']
		response['data'] = employee_list
		return jsonify(response)
	except Exception as e:
		print(str(e))
		return jsonify(response)
     
@app.route('/update_employee', methods=["GET", "POST"])
def update_employee():
    connection =  app._engine.connect()
    transaction = connection.begin()
    try:
        data = dict(request.form)
        query = text(f"update tb_manage_employee set first_name = '{data['edit_first_name']}', middle_name = '{data['edit_middle_name']}', last_name = '{data['edit_last_name']}', contact = '{data['edit_contact']}', email_id = '{data['edit_email_id']}', gender = '{data['edit_gender']}', birth_date = '{data['edit_birth_date']}', blood_group = '{data['edit_blood_group']}', pan_number = '{data['edit_pan_number']}', aadhar_number = '{data['edit_aadhar_number']}', total_experience = '{data['edit_total_experience']}', designation = '{data['edit_designation']}', employee_type = '{data['edit_employee_type']}', joining_date = '{data['edit_joining_date']}', city = '{data['edit_city']}', Country = '{data['edit_Country']}', current_address = '{data['edit_current_address']}', permanent_address = '{data['edit_permanent_address']}', status = '{data['edit_status']}'  where id = '{data['id']}';")
        connection.execute(query)
        transaction.commit()
        connection.close()
        return redirect('/employee_management')
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("Error while updating user : "+ str(e))
        return redirect('/employee_management')             
