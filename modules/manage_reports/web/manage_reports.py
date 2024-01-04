
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

        # Fetch attendance data for the selected month
        attendance_data = generate_all_attendance_data(selected_month, selected_year)

        # Initialize the attendance dictionary
        attendance = {}

        # Extract employee details from attendance data
        for emp_attendance in attendance_data:
            employee_id = emp_attendance['employee_id']
            employee_name = emp_attendance['employee_name']  # Fetch the employee name from the database if available

            # Convert attendance_date to a datetime object
            attendance_date = datetime.strptime(emp_attendance['attendance_date'], "%Y-%m-%d")

            # Update attendance dictionary for all days of the month
            for day in range(1, total_days_in_month + 1):
                Day_key = f"Day_{day}"

                if employee_id in attendance:
                    # Check if the attendance date matches the current day
                    if day == int(attendance_date.strftime("%d")):
                        attendance[employee_id][Day_key] = 'P'  # Mark 'P' for present
                        attendance[employee_id]['present_days'] += 1  # Increment present days
                        attendance[employee_id]['absent_days'] -= 1  # Decrement absent days
                    else:
                        attendance[employee_id][Day_key] = 'A'  # Mark 'A' for absent

                else:
                    # Create new entry for the employee
                    data = {
                        "employee_id": employee_id,
                        "employee_name": employee_name,
                        "total_days": total_days_in_month,
                        "present_days": 0,  # Initialize present days as 0
                        "absent_days": total_days_in_month  # Initialize absent days as total_days_in_month

                    }

                    data[Day_key] = 'P' if day == int(attendance_date.strftime("%d")) else 'A'  # Mark 'P' for present and 'A' for absent

                    attendance[employee_id] = data
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
