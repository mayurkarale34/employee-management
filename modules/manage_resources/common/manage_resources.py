
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
    
