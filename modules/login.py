

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
    try:
        request_data = dict(request.form)
        if request_data['password'] == 'test':

            response['message'] = 'Login Successfully.'
            response['status'] = True
        else:
            response['message'] = 'Incorrect Password'
            
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
        return render_template('manage_resources.html')
    except Exception as e:
        print("exception while login : "+ str(e))
        return render_template('login.html')
    
@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = dict(request.form)
    msg = ''
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    result = connection.execute(text(f"SELECT * FROM tluser WHERE email_id = '{data['email_id']}' or contact_no = '{data['contact_no']}'"))

    if result.rowcount:
        msg = 'Account already exists !'
        transaction.rollback()
        connection.close()
    else:
        connection.execute(text(f"INSERT INTO tluser(`first_name`, `last_name`, `email_id`, `contact_no`, `password`) VALUES ('{data['first_name']}', '{data['last_name']}', '{data['email_id']}', '{data['contact_no']}', '{data['confirmpassword']}');"))
        msg = 'You have successfully registered !'
        transaction.commit()
        connection.close()

    return jsonify(msg)

@app.route('/forgotpassword_page', methods=['GET'])
def forgotpassword_page():
    try:
        return render_template('forgotpassword.html')
    except Exception as e:
        print("exception while rendering forgot password page : "+ str(e))
        return redirect('/')