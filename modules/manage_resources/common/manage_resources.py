
@runtime_logger
def get_all_tluser_info(data, connection):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:
        count_duery = text(f"SELECT count(1) as total FROM tluser;")
        result_count = connection.execute(count_duery)
        response['total'] = result_count.fetchone()[0]

        query = text(f"SELECT id,first_name,last_name,contact_no,email_id, role, status FROM tluser;")
        result = connection.execute(query)
        
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
        response['status'] = True
        response['message'] = "data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response
    
def total_employee(connection):
    response = {
        "status" : False,
        "messege" : "",
        "total" : 0
    } 
    try: 
        query = text("SELECT COUNT(*) AS total FROM tb_manage_employee;")
        result = connection.execute(query).fetchone()
        result = list(result)
        total_count = result[0] if result and result[0] else 0
        response["status"] = True
        response["total"] = total_count
        response["message"] = "Successfully retrieved total count."
        print(response['total'])
        return response['total']
    except exception as e :
        transaction.rollback()
        connection.close()
        print("error while retrive total employee")
        return e
    
def total_present(date, connection):
    response = {
        "status": False,
        "message": "",
        "total_present": 0
    }
    try:
        query = text("SELECT COUNT(employee_id) AS total FROM tb_attendance WHERE attendance_date = '{date}';")
        result = connection.execute(query).fetchone()
        total_count = result[0] if result else 0
        response["status"] = True
        response["total_present"] = total_count
        response["message"] = "Successfully retrieved total present count."
        return response['total_present']
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("error while retrive total present")
        return e
    
def total_leave(date, connection):
    response = {
        "status": False,
        "message": "",
        "total_leave": 0
    }
    try:
        query = text("SELECT COUNT(employee_id) AS total FROM tb_leave WHERE '{date}' BETWEEN from_date AND to_date;")
        result = connection.execute(query).fetchone()
        total_count = result[0] if result else 0
        response["status"] = True
        response["total_leave"] = total_count
        response["message"] = "Successfully retrieved total present count."
        return response['total_leave']
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("error while retrive total leave")
        return e