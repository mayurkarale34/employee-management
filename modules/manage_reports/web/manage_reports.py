
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
        # Generate attendance data for all entries
        """import pdb
        pdb.set_trace()"""
        selected_month =int( request.form.get('month'))
        selected_year = int(request.form.get('year')
)
        # Generate attendance data for the selected month
        new = generate_all_dates_table(selected_month, selected_year)
       
        attendance_data = generate_all_attendance_data(selected_month,selected_year)
        
        # # Create a DataFrame from the attendance data
        df = pd.DataFrame(attendance_data)

        df['attendance_date'] = pd.to_datetime(df['attendance_date'])
        new.index = pd.to_datetime(new.index)
        # Append 'new' DataFrame to 'df' DataFrame
        df = pd.concat([df, new], axis=1)
        if 'attendance' not in df.columns:
         df['attendance'] = 'P'
        # attendance_pivot = df.groupby(['employee_id', 'attendance_date'])['attendance'].first().unstack(fill_value='A')
        attendance_pivot = df.groupby(['employee_id'])[new.columns].first().fillna('A')
        # Save the DataFrame to an Excel file
        excel_filename = "all_attendance_sheet.xlsx"
        attendance_pivot.to_excel(excel_filename)

        # Send the Excel file as a downloadable attachment
        return send_file(excel_filename, as_attachment=True, download_name="all_attendance_sheet.xlsx")

    except Exception as e:
        print(f"Error handling download_all_attendance route: {e}")
        flash("Error generating attendance sheet. Please try again.", "error")
        return redirect('/manage_reports')  # Replace with the actual redirect route

@app.route('/retrive_attendance', methods=["GET"])
@login_required
@runtime_logger
def retrive_attendance():
    connection = app._engine.connect()
    transaction = connection.begin()
    response = {
        "rows": [],
        "total": 0,  # Add total count for pagination
        "message": ""
    }

    try:
        selected_month = request.args.get('monthFilter')
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 50)) 
        search_term = request.args.get('search', '')  # Adjust as needed

        # Use a parameterized query to avoid SQL injection
        query = text("SELECT id, employee_id, attendance_date FROM tb_attendance WHERE MONTH(attendance_date) = :selected_month AND (employee_id LIKE :search_term OR attendance_date LIKE :search_term) LIMIT :limit OFFSET :offset")
        result = connection.execute(query.params(selected_month=selected_month, search_term=f'%{search_term}%', limit=limit, offset=offset))

        # Fetch total count without limit and offset for pagination
        total_query = text("SELECT COUNT(*) FROM tb_attendance WHERE MONTH(attendance_date) = :selected_month AND (employee_id LIKE :search_term OR attendance_date LIKE :search_term)")
        total_result = connection.execute(total_query.params(selected_month=selected_month, search_term=f'%{search_term}%'))
        response['total'] = total_result.scalar()

        if result.rowcount:
            for row in result:
                response['rows'].append({
                    "id": row[0],
                    "employee_id": row[1],
                    "attendance_date": row[2].strftime("%Y-%m-%d")  # Format the date as needed
                })

            response['message'] = "Attendance data retrieved successfully"
        else:
            response['message'] = "No attendance data found"

    except Exception as e:
        print("Error while retrieving attendance data: " + str(e))
        response['message'] = "Error retrieving attendance data"

    finally:
        transaction.rollback()
        connection.close()

    return jsonify(response)
