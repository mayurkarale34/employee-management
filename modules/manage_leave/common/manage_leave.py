
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
    
# Leave application common
@runtime_logger
def apply_for_leave_info(data, connection):
    response = {
         "status" : False,
         "message" : ""
    }
    try:
        
        duplicate_leave_result = connection.execute(text(f"SELECT id FROM tb_leave WHERE employee_id = '{data['employee_id']}' AND (('{data['from_date']}' between from_date and to_date) or ('{data['to_date']}' between from_date and to_date))") )

        if duplicate_leave_result.rowcount:
            # Duplicate entry found
            response['message'] = "Leave already applied, Please check and try again"
            return response
            
        connection.execute(text(f"INSERT INTO tb_leave(`employee_id`,`from_date`,`from_shift`,`to_date`,`to_shift`,`no_of_days`,`leave_reason`,`status`,`applied_by`,`applied_on`) VALUES ('{data['employee_id']}', '{data['from_date']}','{data['from_shift']}','{data['to_date']}','{data['to_shift']}','{data['no_of_days']}','{data['leave_reason']}','pending','{data['applied_by']}','{data['applied_on']}');"))

        response['status'] = True
        response['message'] = "Leave Applied Successfully."
        return response
    except Exception as e:
        print(str(e))
        response['message'] = "Exception: " + str(e)
        return response
    
@runtime_logger
def api_get_leave_info(employee_id):
    response = {
        "status" : False,
        "message" : "",
        "rows" : []
    }
    connection = app._engine.connect()
    try:
        query = text(f"SELECT from_date, from_shift, to_date, to_shift, no_of_days, status, leave_reason FROM tb_leave where employee_id = '{employee_id}'")
        result = connection.execute(query)   
        for row in result:
            columns = result.keys()
            row_dict = dict(zip(columns, row))
            row_dict['from_date'] = row_dict['from_date'].strftime('%Y-%m-%d')
            row_dict['to_date'] = row_dict['to_date'].strftime('%Y-%m-%d')
            response['rows'].append(row_dict)
        response['status'] = True
        response['message'] = "leave data retrived successfully"
        return response
    
    except Exception as e:
        exception = "Exception : " + str(e)
        print(exception)
        response['message'] = exception
        return response    

@runtime_logger
def get_leave_counts(employee_id):
    response = {
        "status": False,
        "message": "",
        "leave_counts": {"casual_leave": 0, "sick_leave": 0}
    }
    connection = app._engine.connect()
    try:
        query = text(f"SELECT leave_type, COUNT(*) as count FROM tb_leave WHERE employee_id = '{employee_id}' GROUP BY leave_type")
        result = connection.execute(query)

        for row in result:
            leave_type, count = row
            if leave_type.lower() == 'casual':
                response['leave_counts']['casual_leave'] = count
            elif leave_type.lower() == 'sick':
                response['leave_counts']['sick_leave'] = count

        response['status'] = True
        response['message'] = "Leave counts retrieved successfully"
        return response

    except Exception as e:
        exception = "Exception: " + str(e)
        print(exception)
        response['message'] = exception
        return response

    
