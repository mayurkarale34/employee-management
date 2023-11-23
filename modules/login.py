

@app.route('/login_page', methods=['GET'])
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
    
@app.route('/SignUpSubmit', methods=['GET','POST'])
def SignUpSubmit():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'emailaddress' in request.form and 'Contactnumber' in request.form and 'password' in request.form and 'confirmpassword' in request.form and 'Gender' in request.form :
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailaddress = request.form['emailaddress']
        Contactnumber = request.form['Contactnumber']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        Gender = request.form['Gender']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tluser WHERE firstname = % s', (firstname, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO tluser VALUES (NULL, % s, % s, % s, %s, %s, %s, %s)', (firstname, lastname, emailaddress, Contactnumber, password, confirmpassword, Gender))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)