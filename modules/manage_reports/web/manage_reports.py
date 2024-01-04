
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
                attendance[employee_id][day_key] = 'P'

         # Fetch leave data for the selected month and date range
        leave_data = generate_all_leave_data(selected_month, selected_year)
        print(leave_data)

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
