

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    try:
        return render_template('login.html')
    except Exception as e:
        print("exception while rendering login page : "+ str(e))
        return redirect('/')
    
@app.route('/login', methods=['POST'])
def login():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        """import pdb
        pdb.set_trace()"""
        data = dict(request.form)
        result = connection.execute(text(f"SELECT password FROM tluser WHERE email_id = '{data['username']}' or contact_no = '{data['username']}'"))
        if result.rowcount:
            result_data = result.fetchone()
            password = result_data[0]
            dec = decrypt_password(ENCRYPTION_KEY, password)
            if data['password'] == dec:
                transaction.commit()
                connection.close()
                response['message'] = 'Login Successfully.'
                response['status'] = True
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
    
@app.route('/manage_resources', methods=['GET'])
def manage_resources():
    try:
        user_name = "Mayur"
        return render_template('manage_resources.html', name = user_name)
    except Exception as e:
        print("exception while login : "+ str(e))
        return render_template('login.html')
    
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
            enc = encrypt_password(ENCRYPTION_KEY, data['confirmpassword'])
            
            query = connection.execute(
                text("INSERT INTO tluser(`first_name`, `last_name`, `email_id`, `contact_no`, `password`) "
                     "VALUES (:first_name, :last_name, :email_id, :contact_no, :password)"),
                {
                    "first_name": data['first_name'],
                    "last_name": data['last_name'],
                    "email_id": data['email_id'],
                    "contact_no": data['contact_no'],
                    "password": enc,
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