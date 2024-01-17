
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
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
    return 'Cache cleared'


@app.route('/manage_metadata')
@login_required
@runtime_logger
def manage_metadata():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('metadata.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))           

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
    