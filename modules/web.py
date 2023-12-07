
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

@app.route('/resource')
def resource():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('resource.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))    

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
        duery = text(f"select * from tluser;")
        result = connection.execute(duery)
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "first_name" : row[1],
                    "last_name" : row[2],
                    "contact_no" : row[3],
                    "email_id" : row[4],
                    "password" : row[5]
                })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
        return jsonify(response)
    
@app.route('/add_employee_page', methods=['GET', 'POST'])
def add_employee_page():
    try:
        return render_template('add_employee.html')
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
        connection.execute(text(f"INSERT INTO tb_manage_employee(`first_name`, `middle_name`, `last_name`, `email_id`, `contact`, `gender`, `city`, `Country`, `aadhar_number`) VALUES ('{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['email_id']}', '{data['contact']}', '{data['gender']}', '{data['city']}', '{data['Country']}', '{data['aadhar_number']}');"))
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
                    "Aadhar_number" : row[9]
                })
        response['total'] = len(response['rows'])
        return jsonify(response)
    except Exception as e:
        print("Error while adding user : "+ str(e))
        return jsonify(response)
                            
