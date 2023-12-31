
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
            columns = result.keys()
            for row in result:
                row_dict = dict(zip(columns, row))
                response['rows'].append(row_dict)

        response['status'] = True
        response['message'] = "data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response

@runtime_logger
def get_all_employees(data):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:
        query = text(f"SELECT employee_id, concat(first_name, ' ', last_name) as employee_name from tb_manage_employee where concat(COALESCE(employee_id, ''), ' ', COALESCE(first_name, ''), ' ', COALESCE(last_name, '')) like '%{data['search_val']}%';")
        result = app._engine.connect().execute(query)
        for row in result:
            columns = result.keys()
            row_dict = dict(zip(columns, row))
            response['rows'].append(row_dict)
            
        response['status'] = True
        response['total'] = len(response['rows'])
        return response
    except Exception as e:
        response['message'] = str(e)
        return response