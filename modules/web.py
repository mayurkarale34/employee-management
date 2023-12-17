
@app.route('/')
def index():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('index.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/home')
def home():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('manage_resources.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))
                
@app.route('/helpd')
def helpd():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('helpdesk.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/manage_metadata')
def manage_metadata():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('metadata.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))           

@app.route('/resource', methods=['GET', 'POST'])
def resource():
   try:
        role_options = retrive_metadata_by_type("role")
        return render_template('resource.html', role_options=role_options)

   except Exception as e:
        print("Error while fetching role options: " + str(e))
        # Handle the error gracefully, perhaps redirect to an error page or return an appropriate response
        return render_template('error.html', error_message="An error occurred.")

    
@app.route('/retrive_user_master', methods=["GET"])
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
def add_employee_page():
    try:
        cities = retrive_metadata_by_type("City")
        countries = retrive_metadata_by_type("Country")
        return render_template('add_employee.html', cities = cities, countries = countries)
    except Exception as e:
        print("exception while rendering add_employee page : "+ str(e))
        return redirect('/')
                                
@app.route('/add_user', methods=['POST'])
def add_user():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.form)
        connection.execute(text(f"INSERT INTO tb_manage_employee(`first_name`, `middle_name`, `last_name`, `email_id`, `contact`, `gender`, `city`, `Country`, `aadhar_number`, `birth_date`, `blood_group`, `pan_number`, `total_experience`, `designation`, `employee_type`, `joining_date`, `current_address`, `permanent_address`) VALUES ('{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['email_id']}', '{data['contact']}', '{data['gender']}', '{data['city']}', '{data['Country']}', '{data['aadhar_number']}', '{data['birth_date']}', '{data['blood_group']}', '{data['pan_number']}','{data['total_experience']}','{data['designation']}', '{data['employee_type']}', '{data['joining_date']}', '{data['current_address']}', '{data['permanent_address']}');"))
        transaction.commit()
        connection.close()

        response['status'] = True
        response['message'] = "You have successfully added user!"
        return jsonify(response)
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        return jsonify(response)
    
@app.route('/employee_management')
def employee_management():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('employee_management.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))    

@app.route('/retrive_tb_manage_employee', methods=["GET"])
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
                    "permanent_address" : row[18] 
                    })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
        return jsonify(response)
                            
@app.route('/update_user', methods=["GET", "POST"])
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
        existing_data = connection.execute(
    text("SELECT element, type FROM tb_metadata WHERE element = :element AND type = :type"),
    {"element": data['element'], "type": data['type']}
).fetchone()



        if existing_data:
            transaction.rollback()
            response['message'] = "Metadata already exists!"
        else:
            # Insert new metadata
            connection.execute(
    text("INSERT INTO tb_metadata (`element`, `type`) VALUES (:element, :type)"),
    {"element": data['element'], "type": data['type']}
)

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
    
@app.route('/manage_page')
def manage_page():
    try:
        employees = retrive_employee ()
        return render_template('manage_page.html', employees=employees)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))    

@app.route('/retrive_tb_attendance', methods=["GET"])
def retrive_tb_attendance():
    connection =  app._engine.connect()
    transaction = connection.begin()
    response = {
        "rows" : [],
        "total" : 0,
        "message" : ""
    }
    try:
        # attendance_date = datetime.strptime(data['date_filter'], '%d-%B-%Y').strftime('%Y-%m-%d')
        duery = text(f"select * from tb_attendance;")
        result = connection.execute(duery)
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "employee_name" : row[1],
                    "date" : row[2],
                    "time" : row[3],
                    "status" : row[4],
                    })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
        return jsonify(response)
    
@app.route('/update_attendance', methods=["GET", "POST"])
def update_attendance():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    current_time = datetime.now().time().strftime("%H:%M")
    try:
        data = dict(request.form)
        # attendance_date = datetime.strptime(data['date'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        existing_data = connection.execute(
            text(f"SELECT * FROM tb_attendance WHERE employee_name = '{data['employee_name']}' AND date = '{data['date']}'")).fetchone()

        if existing_data:
            # Duplicate entry found
            transaction.rollback()
            connection.close()
            response['message'] = "Attendance entry already exists for this employee on the given date."
            flash("Attendance entry already exists for this employee on the given date.", "error")
            return render_template('manage_page.html')
            

        connection.execute(text(f"INSERT INTO tb_attendance(`employee_name`,`date`, `time`, `status`) VALUES ('{data['employee_name']}', '{data['date']}', '{data['time']}', '{data['status']}');"))
        transaction.commit()
        connection.close()

        response['status'] = True
        response['message'] = "You have successfully added user!"
        flash(response['message'], 'success')
        return render_template('manage_page.html', current_date=current_date, current_time=current_time )
    except Exception as e:
        print("Error while adding user, Please contact administrator. : "+ str(e))
        flash("Error while adding user. Please contact the administrator.", 'error')
        return jsonify(response)                       
