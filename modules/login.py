

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
    
@app.route('/manage_resources', methods=['GET'])
def manage_resources():
    try:
        return render_template('manage_resources.html')
    except Exception as e:
        print("exception while login : "+ str(e))
        return render_template('login.html')