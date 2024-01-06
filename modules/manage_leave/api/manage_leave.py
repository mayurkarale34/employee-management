

@app.route('/api/v1/apply-for-leave', methods=["POST"])
@runtime_logger
def apply_for_leave():
    response = {"status" : False, "message" : ""}
    connection =  app._engine.connect() 
    transaction = connection.begin() 
    try:
        data = dict(request.get_json())

        data['applied_on']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['from_date'] = datetime.strptime(data['from_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
        data['to_date'] = datetime.strptime(data['to_date'], '%d-%m-%Y').strftime('%Y-%m-%d')

        application_response = apply_for_leave_info(data, connection)
        if not application_response['status']:
            transaction.rollback()
            connection.close()
            response['message'] = application_response['message']
            return jsonify(response)
        
        transaction.commit()
        connection.close()
        response['status'] = True
        response['message'] = "Leave Applied Successfully."
        return jsonify(response)
    
    except Exception as e:
        transaction.rollback()
        connection.close()
        message = "Error while adding user, Please contact administrator. : "+ str(e)
        print(message)
        response['message'] = message
        return jsonify(response)   
    