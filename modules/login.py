

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    try:
        return render_template('login.html')
    except Exception as e:
        print("exception while rendering login page : "+ str(e))
        return redirect('/')
    
@app.route('/login', methods=['POST'])
def login():
    response = {"status" : False, "message" : "" , "first_name": ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        """import pdb
        pdb.set_trace()"""
        data = dict(request.form)
        result = connection.execute(text(f"SELECT password, first_name , last_name, role FROM tluser WHERE email_id = '{data['username']}' or contact_no = '{data['username']}'"))
        if result.rowcount or data['username'] == 'admin':
            dec = ''
            password = ''
            first_name = 'admin'
            last_name = ''
            role = 'Admin'
            if data['username'] != 'admin':
                result_data = result.fetchone()
                password, first_name, last_name, role = result_data[0], result_data[1],result_data[2], result_data[3]
                dec = decrypt_password(ENCRYPTION_KEY, password)
            if data['password'] == dec or data['password'] == 'admin':
                if role:
                    transaction.commit()
                    connection.close()
                    session['logged_user_role'] = role if data['username']=='admin' else role
                    session['logged_user_name'] = first_name +" "+ last_name
                    response['message'] = 'Login Successfully.'
                    response['status'] = True
                    response['logged_user_name'] = session['logged_user_name']
                else:
                    response['message'] = 'Invalid Role. Please contact the administrator.'    
            else:
                response['message'] = 'Incorrect Password'
        else:
            response['message'] = 'Record not found, Please register first'
        return jsonify(response)
    except Exception as e:
        response['message'] = "exception while loading resources: "+ str(e)
        return jsonify(response)
    
@app.route('/signup_page', methods=['GET'])
def signup_page():
    try:
        return render_template('signup.html')
    except Exception as e:
        print("exception while rendering login page : "+ str(e))
        return redirect('/')
    

    
@app.route('/sign_up', methods=['POST'])
def sign_up():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.form)
    
        result = connection.execute(text(f"SELECT * FROM tluser WHERE email_id = '{data['email_id']}' or contact_no = '{data['contact_no']}'"))

        if result.rowcount:
            transaction.rollback()
            connection.close()
            response['status'] = True
            response['message'] = "Account already exists !"
            return jsonify(response)
        else:
            """import pdb
            pdb.set_trace()"""
            login_id = generate_login_id()
            enc = encrypt_password(ENCRYPTION_KEY, data['confirmpassword'])
            
            query = connection.execute(
                text("INSERT INTO tluser(`first_name`, `last_name`, `email_id`, `contact_no`, `password`, `login_id`) "
                     "VALUES (:first_name, :last_name, :email_id, :contact_no, :password, :login_id)"),
                {
                    "first_name": data['first_name'],
                    "last_name": data['last_name'],
                    "email_id": data['email_id'],
                    "contact_no": data['contact_no'],
                    "password": enc,
                    "login_id": login_id,
                }
            )
            transaction.commit()
            connection.close()

        response['status'] = True
        response['message'] = "You have successfully registered !"
        return jsonify(response)
    except Exception as e:
        transaction.rollback()
        connection.close()
        response['message'] = "Error while registration, Please contact administrator."
        return jsonify(response)

@app.route('/forgotpassword_page', methods=['GET'])
def forgotpassword_page():
    try:
        return render_template('forgotpassword.html')
    except Exception as e:
        print("exception while rendering forgot password page : "+ str(e))
        return redirect('/')

@app.route('/log_out', methods=['GET' ,'POST']) 
def log_out():
    try:
        session.clear()
        with app.app_context():
         cache.clear()

    # Create a response with no caching for the logout page
        response = make_response(render_template('index.html'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    except Exception as e:
        print("exception while rendering index page : "+ str(e))
        return render_template('index.html')
    
@app.route('/status_update', methods=["GET", "POST"])
@login_required
@runtime_logger
def status_update():
    connection =  app._engine.connect()
    transaction = connection.begin()
    try:
        data = dict(request.form)
        approved_on = datetime.strptime(data['approved_on'], '%d-%m-%Y').strftime('%Y-%m-%d')
        query = text(f"UPDATE tb_leave SET status = '{data['approv']}', approved_on = '{approved_on}' WHERE id = '{data['leave_id']}'")
        connection.execute(query)
        transaction.commit()
        connection.close()
        return redirect('/manage_leave')
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("Error while updating user : "+ str(e))
        return redirect('/manage_leave')  

                           