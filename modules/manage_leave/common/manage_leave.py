
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
            count_duery = text(f"SELECT count(1) as total FROM tb_leave where status = if('{data['status']}' = 'All', status, '{data['status']}');")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id) where status = if('{data['status']}' = 'All', status, '{data['status']}') ORDER BY id desc limit {data['offset']}, {data['limit']};")
            print(query)
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_leave tbl where  status = if('{data['status']}' = 'All', status, '{data['status']}') and tbl.employee_id like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id) where status = if('{data['status']}' = 'All', status, '{data['status']}') and tbl.employee_id like '%{data['search']}%'  ORDER BY id desc limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
            
        if result.rowcount:
            for row in result:
                columns = result.keys()
                row_dict = dict(zip(columns, row))
                row_dict['from_date'] = row_dict['from_date'].strftime('%Y-%m-%d')
                row_dict['to_date'] = row_dict['to_date'].strftime('%Y-%m-%d')
                row_dict['approved_on'] = str(row_dict['approved_on'])
                row_dict['applied_on'] = str(row_dict['applied_on'])
                response['rows'].append(row_dict)
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