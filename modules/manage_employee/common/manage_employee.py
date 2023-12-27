
@runtime_logger
def get_all_employee_info(data, connection):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:
        count_duery = text(f"SELECT count(1) as total FROM tb_manage_employee;")
        result_count = connection.execute(count_duery)
        response['total'] = result_count.fetchone()[0]

        query = text(f"SELECT * from tb_manage_employee;")
        result = connection.execute(query)
        
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id" : row[0],
                    "employee_id" : row[1],
                    "first_name" : row[2],
                    "middle_name" : row[3],
                    "last_name" : row[4],
                    "contact" : row[5],
                    "email_id" : row[6],
                    "gender" : row[7],
                    "city" : row[8],
                    "Country" : row[9],
                    "aadhar_number" : row[10],
                    "birth_date" : row[11],
                    "blood_group" : row[12],
                    "pan_number" : row[13],
                    "total_experience" : row[14],
                    "designation" : row[15],
                    "employee_type" : row[16],
                    "joining_date" : row[17],
                    "current_address" : row[18],
                    "permanent_address" : row[19],
                    
                })
        response['status'] = True
        response['message'] = "data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response