
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

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.leave_type, tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id) where status = if('{data['status']}' = 'All', status, '{data['status']}') ORDER BY id desc limit {data['offset']}, {data['limit']};")

            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_leave tbl where  status = if('{data['status']}' = 'All', status, '{data['status']}') and tbl.employee_id like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tbl.id, tbl.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tbl.from_date, tbl.from_shift, tbl.to_date, tbl.to_shift, tbl.no_of_days, tbl.leave_type,tbl.status, tbl.approved_by, tbl.approved_on, tbl.applied_by, tbl.applied_on, tbl.leave_reason FROM tb_leave tbl left join tb_manage_employee tbme on(tbl.employee_id = tbme.employee_id) where status = if('{data['status']}' = 'All', status, '{data['status']}') and tbl.employee_id like '%{data['search']}%'  ORDER BY id desc limit {data['offset']}, {data['limit']};")
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
            
        connection.execute(text(f"INSERT INTO tb_leave(`employee_id`,`from_date`,`from_shift`,`to_date`,`to_shift`,`no_of_days`,`leave_type`,`leave_reason`,`status`,`applied_by`,`applied_on`) VALUES ('{data['employee_id']}', '{data['from_date']}','{data['from_shift']}','{data['to_date']}','{data['to_shift']}','{data['no_of_days']}','{data['leave_type']}','{data['leave_reason']}','pending','{data['applied_by']}','{data['applied_on']}');"))

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
        query = text(f"SELECT from_date, from_shift, to_date, to_shift, no_of_days, leave_type, status, leave_reason FROM tb_leave where employee_id = '{employee_id}'")
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
def api_get_leave_type_info(employee_id):
    response = {
        "status": False,
        "message": "",
        "rows":[]
    }
    connection = app._engine.connect()
    try:
        query = text(f"SELECT casual_leave, earn_leave, comp_offs, sick_leave from tb_overall_leave_master where employee_id = '{employee_id}'")
        result = connection.execute(query)

        for row in result:
            columns = result.keys()
            row_dict = dict(zip(columns, row))
            response['rows'].append(row_dict)
        response['status'] = True
        response['message'] = "leave type data retrived successfully"
        return response

    except Exception as e:
        exception = "Exception: " + str(e)
        print(exception)
        response['message'] = exception
        return response
    

@runtime_logger
def deduct_leave_balances(employee_id, leave_type, no_of_days, connection):
    try:
        # Assuming you have a table named 'overall_leave_master'
        # Adjust the query based on your actual table structure
        check_balance_query = text(f"SELECT casual_leave, sick_leave, earn_leave, comp_offs FROM tb_overall_leave_master WHERE employee_id = '{employee_id}'")
        result = connection.execute(check_balance_query)
        leave_balances = result.fetchone()
        no_of_days = int(no_of_days)
        if leave_balances:
            # Check the requested leave type and deduct the balance accordingly
            if leave_type == 'casual_leave':
                remaining_leave = int(leave_balances[0])
            elif leave_type == 'sick_leave':
                remaining_leave = int(leave_balances[1])
            elif leave_type == 'earn_leave':
                remaining_leave = int(leave_balances[2])
            elif leave_type == 'comp_offs':
                remaining_leave = int(leave_balances[3])
            else:
                return {'status': False, 'message': 'Invalid leave type.'}

            if remaining_leave == 0: 
                return {'status': False, 'message': 'You have no remaining leave.'}

            new_balance = remaining_leave - no_of_days
            update_balance_query = text(f"UPDATE tb_overall_leave_master SET {leave_type} = :new_balance WHERE employee_id = :employee_id")

            # Update the leave balance in the database
            connection.execute(update_balance_query, {'employee_id': employee_id, 'new_balance': new_balance})
              # Commit the transaction

            return {'status': True, 'message': 'Leave balance deducted successfully.'}
        else:
              # Rollback the transaction
            return {'status': False, 'message': 'Employee not found or leave balances not available.'}

    except Exception as e:
        connection.rollback()  # Rollback the transaction in case of an exception
        return {'status': False, 'message': f'Error deducting leave balance: {str(e)}'}


    
