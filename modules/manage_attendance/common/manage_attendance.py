
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

            query = text(f"SELECT  tba.id, tba.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, date_format(tba.attendance_date, '%d-%m-%Y') as attendance_date, date_format(tba.clock_in, '%d-%m-%Y %H:%i:%S') as clock_in, date_format(tba.clock_out, '%d-%m-%Y %H:%i:%S') as clock_out, date_format(tba.working_hours, '%H:%i:%S') as working_hours FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) where attendance_date = '{data['attendance_date']}' limit {data['offset']}, {data['limit']};")
            result = connection.execute(query)
        else:
            count_duery = text(f"SELECT count(1) as total FROM tb_attendance tba where attendance_date = '{data['attendance_date']}' and concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.attendance_date, '')) like '%{data['search']}%';")
            result_count = connection.execute(count_duery)
            response['total'] = result_count.fetchone()[0]

            query = text(f"SELECT tba.id, tba.employee_id, concat(tbme.first_name, ' ', tbme.last_name) as employee_name, date_format(tba.attendance_date, '%d-%m-%Y') as attendance_date, date_format(tba.clock_in, '%d-%m-%Y %H:%i:%S') as clock_in, date_format(tba.clock_out, '%d-%m-%Y %H:%i:%S') as clock_out, date_format(tba.working_hours, '%H:%i:%S') as working_hours FROM tb_attendance tba left join tb_manage_employee tbme on(tba.employee_id = tbme.employee_id) where attendance_date = '{data['attendance_date']}' and concat(COALESCE(tba.employee_id, ''), ' ', COALESCE(tba.attendance_date, '')) like '%{data['search']}%' limit {data['offset']}, {data['limit']};")
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
        employee_id = data['employee_id']
        attendance_date = data['attendance_date']
        leave_query = text(f"SELECT count(1) as leave_count FROM tb_leave WHERE employee_id = '{employee_id}'AND '{attendance_date}' BETWEEN from_date AND to_date ")
        result_leave = connection.execute(leave_query).fetchone()
        leave_count = result_leave[0] if result_leave else 0

        if leave_count > 0:
            response['message'] = "Leave is already applied for this date. Cannot mark attendance."
            return response
        
        if data['action'] == 'CLOCK_IN':
            existing_data = connection.execute(text(f"SELECT count(1) as total FROM tb_attendance WHERE employee_id = '{employee_id}' AND attendance_date = '{attendance_date}'")).fetchone()[0]

            if existing_data > 0:
                response['message'] = "Attendance entry already exists for this employee on the given date."
                return response
                
            connection.execute(text(f"INSERT INTO tb_attendance(`employee_id`,`attendance_date`, `clock_in`, `status`) VALUES ('{employee_id}', '{attendance_date}', '{data['clock_time']}', 'Present');"))

            response['status'] = True
            response['message'] = "Clock In Successful."

        elif data['action'] == 'CLOCK_OUT':
            
            clock_out = datetime.strptime(data['clock_time'], '%Y-%m-%d %H:%M:%S')

            result_attendance = connection.execute(text(f"SELECT date_format(clock_in, '%d-%m-%Y %H:%i:%S') as clock_in FROM tb_attendance WHERE id = '{data['attendance_id']}';"))

            if result_attendance.rowcount:
                clock_in = result_attendance.fetchone()[0]
            else:
                response['message'] = 'Attendance details not found, please try again'
                return response
            clock_in = datetime.strptime(clock_in, '%d-%m-%Y %H:%M:%S')
            if (clock_out - clock_in) < timedelta(minutes=30):
                response['status'] = False
                response['message'] = 'Clock Out not allowed within the first half hour of Clock In.'
                return response

            working_hours = datetime_difference(clock_in, clock_out)

            # Convert the string to a datetime object
            working_hours = datetime.strptime(working_hours, "%H:%M:%S").strftime('%H:%M:%S')

            result_update_attendance = connection.execute(text(f"update tb_attendance set clock_out = '{data['clock_time']}', working_hours = '{working_hours}' WHERE id = '{data['attendance_id']}';"))

            response['status'] = True
            response['message'] = "Clock Out Successful."

        else:
            response['message'] = 'Invalid Action, Please contact to admin'
            return response
        
        return response
    except Exception as e:
        print("Error while adding Attendance, Please contact administrator. : "+ str(e))
        return response['message']     


@runtime_logger
def datetime_difference(start_datetime, end_datetime):
    # Calculate the time difference
    time_diff = end_datetime - start_datetime

    # Extract days, hours, minutes, and seconds
    days, seconds = time_diff.days, time_diff.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return str(hours) + ':' + str(minutes) + ':' + str(seconds)
