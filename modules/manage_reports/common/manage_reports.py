
def generate_all_attendance_data(selected_month, selected_year):
    # Response dictionary to track the status and provide messages
    response = {
        "status": False,
        "message": "",
    }

    # Connect to the database
    connection = app._engine.connect()
    transaction = connection.begin()

    try:
        # Fetch all attendance data from the database
        start_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%m-%d")
        last_day_of_month = calendar.monthrange(selected_year, selected_month)[1]
        end_date = start_date.replace(day=last_day_of_month)

        # Execute the SQL query to retrieve attendance data
        attendance_data = connection.execute(
            text(
                "SELECT tba.id, tba.employee_id, date_format(tba.attendance_date, '%d') as day,  concat(tbme.first_name, ' ', tbme.last_name) as employee_name FROM tb_attendance tba left join tb_manage_employee tbme on (tbme.employee_id = tba.employee_id) WHERE tba.attendance_date BETWEEN :start_date AND :end_date"
            ),
            {"start_date": start_date, "end_date": end_date},
        ).fetchall()

        # Convert the SQLAlchemy results to a list of dictionaries
        attendance_data_list = [
            {"id": entry[0], "employee_id": entry[1], "day": entry[2], "employee_name": entry[3]}
            for entry in attendance_data
        ]

        # Commit the transaction and close the database connection
        transaction.commit()
        connection.close()

        # Update response with success status and message
        response["status"] = True
        response["message"] = "Data extracted successfully"
        flash(response["message"], "success")

        # Return the list of attendance data
        return attendance_data_list

    except Exception as e:
        # Rollback the transaction, close the connection, and handle the exception
        transaction.rollback()
        connection.close()
        print("Error while adding user, Please contact administrator. : " + str(e))
        flash("Error while adding user. Please contact the administrator.", "error")

        # Return the response as JSON
        return jsonify(response)
    
def generate_all_leave_data(selected_month, selected_year):
    # Response dictionary to track the status and provide messages
    response = {
        "status": False,
        "message": "",
    }

    # Connect to the database
    connection = app._engine.connect()
    transaction = connection.begin()

    try:
        # Fetch all leave data from the database for the selected month
        start_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%m-%d")
        last_day_of_month = calendar.monthrange(selected_year, selected_month)[1]
        end_date = start_date.replace(day=last_day_of_month)

        # Execute the SQL query to retrieve leave data
        leave_data = connection.execute(
            text(
                "SELECT id, employee_id, from_date, to_date FROM tb_leave WHERE from_date BETWEEN :start_date AND :end_date"
            ),
            {"start_date": start_date, "end_date": end_date},
        ).fetchall()

        # Convert the SQLAlchemy results to a list of dictionaries
        leave_data_list = [
            {"id": entry[0], "employee_id": entry[1], "from_date": entry[2], "to_date": entry[3]}
            for entry in leave_data
        ]

        # Commit the transaction and close the database connection
        transaction.commit()
        connection.close()

        # Update response with success status and message
        response["status"] = True
        response["message"] = "Data extracted successfully"
        flash(response["message"], "success")

        # Return the list of leave data
        return leave_data_list

    except Exception as e:
        # Rollback the transaction, close the connection, and handle the exception
        transaction.rollback()
        connection.close()
        print("Error while retrieving leave data: " + str(e))
        flash("Error while retrieving leave data. Please try again.", "error")

        # Return the response as JSON
        return jsonify(response)

# Helper function to iterate over a date range
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def create_attendance_table(total_days_in_month):
    table = []
    for day in total_days_in_month:
        table.append({
            'Day': day,
            'Clock In': '',
            'Clock Out': '',
            'Status': 'Absent',
            'Working Hours': ''
        })
    return table 

def update_attendance_table(table, attendance_data):
    for record in attendance_data:
        day = record['day']  # assuming your records have a 'day' field
        entry = next((entry for entry in table if entry['Day'] == day), None)
        if entry:
            entry['Clock In'] = record['clock_in']
            entry['Clock Out'] = record['clock_out']
            entry['Status'] = 'Present'
            entry['Working Hours'] = calculate_working_hours(record['clock_in'], record['clock_out'])
    return table


def get_atteandance_data(employee_id,selected_month,selected_year,connection):
    response = {
        "status" : False,
        "message" : "",
    
    }
    try:
        start_dat = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%m-%d")
        last_day_of_month = calendar.monthrange(selected_year, selected_month)[1]
        end_dat = start_dat.replace(day=last_day_of_month)
        start_date = start_dat.strftime('%Y-%m-%d')
        end_date = end_dat.strftime('%Y-%m-%d')

        query = text(f"select DATE_FORMAT(tba.attendance_date, '%Y-%m-%d') as day ,DATE_FORMAT(tba.clock_in, '%H:%i') AS clock_in, DATE_FORMAT(tba.clock_out, '%H:%i') AS clock_out, tba.status, DATE_FORMAT(tba.working_hours, '%H:%i:%s') as  working_hours,concat(tbme.first_name, ' ', tbme.last_name) as employee_name, tba.employee_id from tb_attendance as tba  left join tb_manage_employee tbme on (tbme.employee_id = tba.employee_id) where tba.employee_id = '{employee_id}' AND tba.attendance_date between '{start_date}' AND '{end_date}'; ")
        result = connection.execute(query).fetchall()

        attendance_data_list = [
            {"day": entry[0], "clock_in": entry[1],"clock_out": entry[2],"status": entry[3],"working_hours": entry[4],"employee_name":entry[5], "employee_id": entry[6]}
            for entry in result
        ]
        response['status'] = True
        response['message'] = "get data extracted successfully"
        return attendance_data_list

    except Exception as e :
        print("Error while get attendance data as : ", e)    
        return e

def get_leave_data(employee_id,selected_month, selected_year,connection): 
    response = {
        "status" : False,
        "message" : "",
    
    }
    try:
        start_dat = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%m-%d")
        last_day_of_month = calendar.monthrange(selected_year, selected_month)[1]
        end_dat = start_dat.replace(day=last_day_of_month)
        start_date = start_dat.strftime('%Y-%m-%d')
        end_date = end_dat.strftime('%Y-%m-%d')

        leave_data = connection.execute(
            text(f"SELECT id, employee_id, DATE_FORMAT(from_date, '%Y-%m-%d') as from_date, DATE_FORMAT(to_date, '%Y-%m-%d') as to_date FROM tb_leave WHERE employee_id = '{employee_id}' and from_date  and to_date between '{start_date}' AND  '{end_date}'")).fetchall()

        # Convert the SQLAlchemy results to a list of dictionaries
        leave_data_list = [
            {"id": entry[0], "employee_id": entry[1], "from_date": entry[2], "to_date": entry[3]}
            for entry in leave_data
        ]
        response['status'] = True
        response['message'] = "get data extracted successfully"
        return leave_data_list

    except Exception as e:
        print("Error while get leave data as : ", e)    
        return e
    
def create_attendance_pdf(attendance,employee_name,month_name,selected_year,total_absent,total_days,total_present,total_leave):

    # attendance_data_dict = {entry['day']: entry for entry in attendance_data}
    buffer = BytesIO()

    # Create the PDF object, using BytesIO as its "file."
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Company Logo (replace 'company_logo.png' with the actual path or URL)
    page_width = 8.5 * 72  # 1 inch = 72 points
    # page_height = 11 * 72
    pdf.drawInlineImage('static/images/logo.png',(page_width - 320) / 2, 750 , width=300, height=50)

    # Employee ID, Month, and Year
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, 740, f"Employee Name: {employee_name}")
    pdf.drawString(220, 720, f"Month Year: {month_name} - {selected_year}")

    # Total Present, Total Absent, Total Days
    pdf.drawString(80, 700, f"Total Present: {total_present}")
    pdf.drawString(400, 700, f"Total Absent: {total_absent}")
    pdf.drawString(80, 680, f"Total Leave: {total_leave} ")
    pdf.drawString(400, 680, f"Total Days: {total_days}")
    #pdf.drawString(10, 620, str(attendance_table))

    # Table Header
    pdf.drawCentredString(75,638, "Day")
    pdf.drawCentredString(165,638, "Clock In")
    pdf.drawCentredString(265,638, "Clock Out")
    pdf.drawCentredString(373,638, "Working Hours")
    pdf.drawCentredString(465,638, "Status")


    # # Table Content
    pdf.setFont("Helvetica", 10)
    y_position = 650 # Starting Y position for table content
    cell_height = 20
   
    for entry in attendance:
        # Draw borders for each cell
        pdf.rect(40, y_position - cell_height, 90, cell_height)  # Day
        pdf.rect(130, y_position - cell_height, 100, cell_height)  # Clock In
        pdf.rect(230, y_position - cell_height, 100, cell_height)  # Clock Out
        pdf.rect(330, y_position - cell_height, 100, cell_height)  # Working Hours
        pdf.rect(430, y_position - cell_height, 90, cell_height)  # Status

        pdf.drawCentredString(75, y_position - cell_height/2, str(entry.get('days', '')))  # Day
        pdf.drawCentredString(165, y_position - cell_height/2, str(entry.get('clock_in', '')))  # Clock In
        pdf.drawCentredString(265, y_position - cell_height/2, str(entry.get('clock_out', '')))  # Clock Out
        pdf.drawCentredString(370, y_position - cell_height/2, str(entry.get('working_hours', '')))  # Working Hours
        pdf.drawCentredString(465, y_position - cell_height/2, str(entry.get('status', '')))  # Status

        y_position -= cell_height  # Adjust Y position for the next row

    pdf.save()

    # Move the buffer's cursor to the beginning
    buffer.seek(0)

    return buffer
