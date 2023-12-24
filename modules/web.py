
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            print("login required called")
            if 'logged_user_name' in session:
                return func(*args, **kwargs)
            else:
                return redirect('/login_page')
        except Exception as e:
            print(e)
            # You might want to handle exceptions more appropriately, log them, or customize the behavior.
            return Response("Internal Server Error", status=500)
    return wrap

def runtime_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        app.logger.info('*** Start monitoring ' + func.__name__ + '()')
        result = func(*args, **kwargs)
        app.logger.info('*** Stop monitoring ' + func.__name__ + '()')

        return result
    return wrapper

@app.route('/')
@cache.cached(timeout=60)
def index():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('index.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/clear_cache')
def clear_cache():
    cache.clear()
    print("clear cache")
    return 'Cache cleared'

@app.route('/home')
def home():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('manage_resources.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/manage_metadata')
@login_required
@runtime_logger
def manage_metadata():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('metadata.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))           

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
        """import pdb
        pdb.set_trace()"""
        duery = text(f"SELECT id,first_name,last_name,contact_no,email_id, role, status FROM tluser;")
        result = connection.execute(duery)
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "first_name" : row[1],
                    "last_name" : row[2],
                    "contact_no" : row[3],
                    "email_id" : row[4],
                    "role" : row[5],
                    "status" : row[6]
                })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
        return jsonify(response)
    
@app.route('/add_employee_page', methods=['GET', 'POST'])
@login_required
@runtime_logger
def add_employee_page():
    try:
        cities = retrive_metadata_by_type("City")
        countries = retrive_metadata_by_type("Country")
        roles = retrive_metadata_by_type("Role")
        bloodgroups = retrive_metadata_by_type("Blood Group")
        return render_template('add_employee.html', cities = cities, countries = countries, roles = roles, bloodgroups = bloodgroups)
    except Exception as e:
        print("exception while rendering add_employee page : "+ str(e))
        return redirect('/')
  
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
        duery = text(f"select * from tb_manage_employee;")
        result = connection.execute(duery)
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "first_name" : row[1],
                    "middle_name" : row[2],
                    "last_name" : row[3],
                    "contact" : row[4],
                    "email_id" : row[5],
                    "gender" : row[6],
                    "city" : row[7],
                    "Country" : row[8],
                    "aadhar_number" : row[9],
                    "birth_date" : row[10],
                    "blood_group" : row[11],
                    "pan_number" : row[12],
                    "total_experience" : row[13],
                    "designation" : row[14],
                    "employee_type" : row[15],
                    "joining_date" : row[16],
                    "current_address" : row[17],
                    "permanent_address" : row[18],
                    "employee_id" : row[19] 
                    })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
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

@app.route('/add_metadata', methods=["POST"])
@login_required
@runtime_logger
def add_metadata():
    connection = app._engine.connect()
    transaction = connection.begin()
    response = {
        "status": False,
        "message": ""
    }
    try:
        data = request.get_json()
        # Check for existing data
        existing_data = connection.execute(text("SELECT element, type FROM tb_metadata WHERE element = :element AND type = :type"),{"element": data['element'], "type": data['type']}).fetchone()
        if existing_data:
            transaction.rollback()
            response['message'] = "Metadata already exists!"
        else:
            # Insert new metadata
            connection.execute(text("INSERT INTO tb_metadata (`element`, `type`) VALUES (:element, :type)"),{"element": data['element'], "type": data['type']})
            transaction.commit()
            response['status'] = True
            response['message'] = "Metadata added successfully"
    except Exception as e:
        transaction.rollback()
        response['message'] = f"Error while adding metadata: {str(e)}"
    finally:
        connection.close()
    return jsonify(response)

@app.route('/retrive_metadata', methods=["GET"])
@login_required
@runtime_logger
def retrive_metadata():
    connection =  app._engine.connect()
    transaction = connection.begin()
    response = {
        "rows" : [],
        "total" : 0,
        "message" : ""
    }
    try:
        search = request.args.get('search')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        if search=='':
            count_duery = text(f"SELECT count(1) as total FROM tb_metadata;")
            result_count = connection.execute(count_duery)
            total = result_count.fetchone()[0]

            data_duery = text(f"SELECT id,element,type FROM tb_metadata limit {offset}, {limit};")
            result = connection.execute(data_duery)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_metadata where concat(COALESCE(element, ''), ' ', COALESCE(type, '')) like '%{search}%';")
            result_count = connection.execute(count_duery)
            total = result_count.fetchone()[0]

            data_duery = text(f"SELECT id,element,type FROM tb_metadata where concat(COALESCE(element, ''), ' ', COALESCE(type, '')) like '%{search}%' limit {offset}, {limit};")
            result = connection.execute(data_duery)

        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "element" : row[1],
                    "type" : row[2]
                })

        response['total'] = total
        return jsonify(response)
    except Exception as e:
        print("Error while getting metadata : "+ str(e))
        return jsonify(response)
    
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
        duery = text(f"select * from tb_leave;")
        result = connection.execute(duery)
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "employee_name" : row[1],
                    "from_date" : row[2],
                    "from_shift" : row[3],
                    "to_date" : row[4],
                    "to_shift" : row[5],
                    "no_of_days" : row[6],
                    "leave_reason" : row[7],
                    "status" : row[8],
                    "approved_on" : row[9],
                    "approved_by" : row[10],
                    "leave_reason" : row[11],
                    "applied_by" : row[12],
                    "applied_on" : row[13]
                    })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
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
        attendance_date = datetime.strptime(data['date'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        existing_data = connection.execute(
            text(f"SELECT * FROM tb_attendance WHERE employee_name = '{data['employee_name']}' AND date = '{attendance_date}'")).fetchone()

        if existing_data:
            # Duplicate entry found
            transaction.rollback()
            connection.close()
            response['message'] = "Attendance entry already exists for this employee on the given date."
            flash("Attendance entry already exists for this employee on the given date.", "error")
            return redirect('/manage_attendance' )
            
        connection.execute(text(f"INSERT INTO tb_attendance(`employee_name`,`date`) VALUES ('{data['employee_name']}', '{attendance_date}');"))
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

@app.route('/manage_leave')
@login_required
@runtime_logger
def manage_leave(): 
    try:
        employees = retrive_employee ()
        return render_template('manage_leave.html', employees=employees)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))       

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
        search = request.args.get('search')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)

        # Assuming the date format is day-month-year hour:minute:second (e.g., 17-12-2023 22:58:00)

        count_duery = text(f"SELECT count(1) as total FROM tb_leave;")
        result_count = connection.execute(count_duery)
        response['total'] = result_count.fetchone()[0]

        query = text(f"SELECT * FROM tb_leave ;")
        result = connection.execute(query)
        
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id": row[0],
                    "employee_name": row[1],
                    "from_date": row[2],
                    "from_shift": row[3],
                    "to_date": row[4],
                    "to_shift": row[5],
                    "no_of_days": row[6],
                    "status": row[7],
                    "approved_on": row[8],
                    "leave_reason": row[10]
                })

        return jsonify(response)
    except Exception as e:
        print("Error while retrieving attendance data: " + str(e))
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
        from_date = datetime.strptime(data['from_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        to_date = datetime.strptime(data['to_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        existing_data = connection.execute(
            text(f"SELECT * FROM tb_leave WHERE employee_id = '{data['employee_name']}'")).fetchone()

        if existing_data:
            # Duplicate entry found
            transaction.rollback()
            connection.close()
            response['message'] = "Attendance entry already exists for this employee on the given date."
            flash("Attendance entry already exists for this employee on the given date.", "error")
            return redirect('/manage_leave' )
            
        connection.execute(text(f"INSERT INTO tb_leave(`employee_id`,`from_date`,`from_shift`,`to_date`,`to_shift`,`no_of_days`,`leave_reason`) VALUES ('{data['employee_name']}', '{from_date}','{data['from_shift']}','{to_date}','{data['to_shift']}','{data['no_of_days']}','{data['leave_reason']}');"))
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

