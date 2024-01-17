
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
        return response['total']
    except exception as e :
        print("error while retrive total employee")
        return e
    
def total_present(date, connection):
    response = {
        "status": False,
        "message": "",
        "total_present": 0
    }
    try:
        query = text(f"SELECT COUNT(employee_id) AS total FROM tb_attendance WHERE attendance_date = '{date}';")
        result = connection.execute(query).fetchone()
        result = list(result)
        total_count = result[0] if result else 0
        response["status"] = True
        response["total_present"] = total_count
        response["message"] = "Successfully retrieved total present count."
        return response['total_present']
    except Exception as e:
        print("error while retrive total present")
        return e
    
def total_leave(date, connection):
    response = {
        "status": False,
        "message": "",
        "total_leave": 0
    }
    try:
        query = text(f"SELECT COUNT(employee_id) AS total FROM tb_leave WHERE '{date}' BETWEEN from_date AND to_date;")
        result = connection.execute(query).fetchone()
        result = list(result)
        total_count = result[0] if result else 0
        response["status"] = True
        response["total_leave"] = total_count
        response["message"] = "Successfully retrieved total present count."
        return response['total_leave']
    except Exception as e:
        print("error while retrive total leave")
        return e