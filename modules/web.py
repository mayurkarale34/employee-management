
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
                                