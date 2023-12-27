
@runtime_logger
def get_all_attendance_info(data, connection):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:

        if data['search'] == '':
            count_duery = text(f"SELECT count(1) as total FROM tb_attendance;")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tba.id, tba.employee_id,tba.date FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_attendance where concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.date, '')) like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tba.id, tba.employee_id,tba.date FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) where concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.date, '')) like '%{data['search']}%' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id": row[0],
                    "employee_id": row[1],
                    "date": row[2]
                })
        response['status'] = True
        response['message'] = "data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response
