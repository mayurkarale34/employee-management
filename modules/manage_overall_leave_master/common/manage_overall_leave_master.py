
@runtime_logger
def get_overall_leave_master_info(data, connection):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:
        if data['search'] == '':
            count_duery = text(f"SELECT count(1) as total FROM tb_overall_leave_master;")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT sr_no, employee_id, employee_name, casual_leave, earn_leave, comp_offs, sick_leave FROM tb_overall_leave_master limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_overall_leave_master where employee_id OR employee_name like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT sr_no, employee_id, employee_name, casual_leave, earn_leave, comp_offs, sick_leave FROM tb_overall_leave_master where employee_id OR employee_name like '%{data['search']}%' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
            
        if result.rowcount:
            for row in result:
                columns = result.keys()
                row_dict = dict(zip(columns, row))
                response['rows'].append(row_dict)
        response['status'] = True
        response['message'] = "overall_leave_master data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response