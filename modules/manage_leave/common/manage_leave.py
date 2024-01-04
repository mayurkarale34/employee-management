
@runtime_logger
def get_all_leave_info(data, connection):
    response = {
        "status" : False,
        "message" : "",
        "rows" : [],
        "total" : 0
    }
    try:
        if data['search'] == '':
            count_duery = text(f"SELECT count(1) as total FROM tb_leave;")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id) limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_leave tbl where tbl.employee_id like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id)  where tbl.employee_id like '%{data['search']}%' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
            
        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id": row[0],
                    "employee_id": row[1],
                    "employee_name": row[2],
                    "from_date": row[3],
                    "from_shift": row[4],
                    "to_date": row[5],
                    "to_shift": row[6],
                    "no_of_days": row[7],
                    "status": row[8],
                    "approved_by": row[9],
                    "approved_on": str(row[10]),
                    "applied_by": row[11],
                    "applied_on": str(row[12]),
                    "leave_reason": row[13]
                })
        response['status'] = True
        response['message'] = "data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response

# Common method to approve the leave
@runtime_logger
def approve_leave_info(data, connection):
    response = {
        "status" : False,
        "message" : ""
    }
    try:
        update_query = text(f"UPDATE tb_leave SET status = 'Approved', approved_by = '{data['approved_by']}', approved_on = '{data['approved_on']}' where id = {data['leave_id']}")
        connection.execute(update_query)

        response['status'] = True
        response['message'] = "Leave Approved Successfully."

        return response
    
    except Exception as e:
        print("Exception : " + str(e))
        response['message'] = "Error while approving the leave, Please contact to Admin"
        return response