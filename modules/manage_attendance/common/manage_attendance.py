
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
            count_duery = text(f"SELECT count(1) as total FROM tb_attendance where attendance_date = '{data['attendance_date']}';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT  tba.id, tba.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, date_format(tba.attendance_date, '%d-%m-%Y') as attendance_date, date_format(tba.clock_in, '%d-%m-%Y %H:%i:%S') as clock_in, date_format(tba.clock_out, '%d-%m-%Y %H:%i:%S') as clock_out FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) where attendance_date = '{data['attendance_date']}' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_attendance tba where attendance_date = '{data['attendance_date']}' and concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.attendance_date, '')) like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tba.id, tba.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, date_format(tba.attendance_date, '%d-%m-%Y') as attendance_date, date_format(tba.clock_in, '%d-%m-%Y %H:%i:%S') as clock_in, date_format(tba.clock_out, '%d-%m-%Y %H:%i:%S') as clock_out FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) where attendance_date = '{data['attendance_date']}' and concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.attendance_date, '')) like '%{data['search']}%' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        
        if result.rowcount:
            for row in result:
                columns = result.keys()
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
def add_attendance_info(data, connection):
    response = {
       "status" : False,
       "message" : ""
   }
    try:
        existing_data = connection.execute(text(f"SELECT count(1) as total FROM tb_attendance WHERE employee_id = '{data['employee_id']}' AND attendance_date = '{data['attendance_date']}'")).fetchone()[0]

        if existing_data > 0:
            response['message'] = "Attendance entry already exists for this employee on the given date."
            return response
            
        connection.execute(text(f"INSERT INTO tb_attendance(`employee_id`,`attendance_date`, `clock_in`, `status`) VALUES ('{data['employee_id']}', '{data['attendance_date']}', '{data['clock_in_date_time']}', 'Present');"))

        response['status'] = True
        response['message'] = "Attendance Marked Successfully "
        return response
    except Exception as e:
        print("Error while adding Attendance, Please contact administrator. : "+ str(e))
        return response['message']     
