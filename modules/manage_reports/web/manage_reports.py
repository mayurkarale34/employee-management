
@app.route('/manage_reports')
def manage_reports():
    try:
     return render_template('manage_reports.html')
    except Exception as e:
        print("exception while rendering index page : "+ str(e))


# Route for handling the download of the entire attendance sheet
@app.route('/download_all_attendance', methods=['POST'])
def download_all_attendance():
    try:
        # Assuming request.form.get('year_month') returns a string like "2024-01"
        year_month_str = request.form.get('year_month')

        # Convert the string to a datetime object
        year_month_date = datetime.strptime(year_month_str, '%Y-%m')

        # Extract the month and year
        selected_month = int(year_month_date.strftime('%m'))
        selected_year = int(year_month_date.strftime('%Y'))
       
        # Generate attendance data for the selected month
        _, last_day = calendar.monthrange(selected_year, selected_month)

        # Calculate the total days in a month
        total_days_in_month = last_day

        # Get the name of the selected month
        month_name = calendar.month_name[selected_month]
        
        month_days = {}
        month_days['employee_id'] = ''
        month_days['employee_name'] = ''
        for day in range(1, total_days_in_month + 1):
            month_days['Day_'+str(day)] = 'A'

        # Fetch attendance data for the selected month
        attendance_data = generate_all_attendance_data(selected_month, selected_year)

        # Initialize the attendance dictionary
        attendance = {}

        # Extract employee details from attendance data
        for emp_attendance in attendance_data:
            employee_id = emp_attendance['employee_id']
            employee_name = emp_attendance['employee_name']  # Fetch the employee name from the database if available
            day = emp_attendance['day']
            day_key = 'Day_'+str(int(day))

            if employee_id in attendance:

                attendance[employee_id][day_key] = 'P'
                attendance[employee_id]['present_days'] += 1  # Increment present days
                attendance[employee_id]['absent_days'] -= 1 

            else:
                dict_format = month_days.copy()
                dict_format['employee_id'] = employee_id
                dict_format['employee_name'] = employee_name
                dict_format['total_days'] = total_days_in_month
                
                attendance[employee_id] = dict_format

                attendance[employee_id]['present_days'] = 1  # Increment present days
                attendance[employee_id]['absent_days'] = total_days_in_month-1
                attendance[employee_id]['leave_days'] = 0
                attendance[employee_id][day_key] = 'P'

         # Fetch leave data for the selected month and date range
        leave_data = generate_all_leave_data(selected_month, selected_year)

        # Incorporate leave data into the attendance dictionary
        for leave_entry in leave_data:
            employee_id = leave_entry['employee_id']
            leave_start_date = leave_entry['from_date']
            leave_end_date = leave_entry['to_date']

            # Iterate over the date range and mark each corresponding day as leave
            for leave_date in daterange(leave_start_date, leave_end_date):
                leave_day = leave_date.day
                leave_day_key = 'Day_'+str(leave_day)

                if employee_id in attendance:
                    attendance[employee_id]['leave_days'] += 1 
                    attendance[employee_id]['absent_days'] = attendance[employee_id]['absent_days']-1
                    attendance[employee_id][leave_day_key] = 'L'
        
        # Convert the dictionary to a list
        final_data = list(attendance.values())
        # Create a DataFrame from the attendance data
        df = pd.DataFrame(final_data)

        # Save the DataFrame to an Excel file
        excel_filename = "attendance_sheet.xlsx"
        df.to_excel(excel_filename)

        # Send the Excel file as a downloadable attachment with the month name in the filename
        return send_file(excel_filename, as_attachment=True, download_name=f"{month_name}_attendance_sheet.xlsx")

    except Exception as e:
        print(f"Error handling download_all_attendance route: {e}")
        flash("Error generating attendance sheet. Please try again.", "error")
        return redirect('/manage_reports')

@app.route('/attendance_download', methods=['POST'])
def attendance_download():
    response = {
        "status": False,
        "message": "",
        "row": []
    }

    connection = app._engine.connect()
    transaction = connection.begin()
    try:
        employee_id = request.form.get('employee_id')
        month_year_str = request.form.get('month_year')

        month_year_date = datetime.strptime(month_year_str, '%Y-%m')
        selected_month = int(month_year_date.strftime('%m'))
        selected_year = int(month_year_date.strftime('%Y'))
        _, last_day = calendar.monthrange(selected_year, selected_month)

        # Calculate the total days in a month
        total_days_in_month = last_day
        target_days = list(range(1, last_day + 1))

        # Get the name of the selected month
        month_name = calendar.month_name[selected_month]

        # Initialize attendance dictionary
        attendance = [{'days':'' ,'clock_in' : '','clock_out':'' ,'status': '', 'working_hours' : ''}]

        # Generate attendance_data (replace this with your actual data retrieval logic)
        attendance_data =  get_atteandance_data(employee_id, selected_month, selected_year, connection)
        leave_data =  get_leave_data(employee_id, selected_month, selected_year, connection)
        total_present = 0
        total_absent = 0
        total_leave = 0
        employee_name = attendance_data[0]["employee_name"]
        for target_day in target_days:
            leave_entry = next((entry for entry in leave_data if datetime.strptime(entry['from_date'], '%Y-%m-%d').day <= int(target_day) <= datetime.strptime(entry['to_date'], '%Y-%m-%d').day), None)

            if leave_entry:
                # Append the leave data to the attendance list
                total_leave += 1
                attendance.append({
                    'days': target_day,
                    'clock_in': '-',
                    'clock_out': '-',
                    'status': 'Leave',
                    'working_hours': '-'
                })
            else:
                # If the day is not a leave day, check attendance data
                day_data = next((entry for entry in attendance_data if datetime.strptime(entry['day'], '%Y-%m-%d').day == int(target_day)), None)
                if day_data:
                    # Append the data to the attendance list for a normal working day
                    total_present += 1
                    attendance.append({
                        'days': target_day,
                        'clock_in': day_data['clock_in'],
                        'clock_out': day_data['clock_out'],
                        'status': 'Present',
                        'working_hours': day_data['working_hours']
                    })
                else:
                    total_absent +=1
                    # If the day is not in attendance_data and not a leave day, append empty data with status 'Absent'
                    attendance.append({
                        'days': target_day,
                        'clock_in': '-',
                        'clock_out': '-',
                        'status': 'Absent',
                        'working_hours': '-'
                    })

        
        total_days = total_days_in_month
        
        pdf_buffer = create_attendance_pdf(attendance, employee_name,month_name, selected_year, total_absent,
                                           total_days, total_present,total_leave)

        # Set up the response for downloading the PDF
        response = Response(pdf_buffer, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename=attendance_report.pdf'
        transaction.rollback()
        connection.close()
        return response

    except Exception as e:
        print("Error while downloading attendance: ", e)
        return str(e)

