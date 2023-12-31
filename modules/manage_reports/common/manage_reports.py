
def generate_all_attendance_data(selected_month,selected_year):
    response = {
        "status" : False,
        "message" : "",
    }
    connection =  app._engine.connect() 
    transaction = connection.begin()
    try:
    # Fetch all attendance data from the database
        start_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%m-%d")
        last_day_of_month = calendar.monthrange(selected_year, selected_month)[1]
        end_date = start_date.replace(day=last_day_of_month)
            # Execute the query with parameters
        attendance_data = connection.execute(text("SELECT id, employee_id, date FROM tb_attendance WHERE date BETWEEN :start_date AND :end_date"), {"start_date": start_date, "end_date": end_date}).fetchall()
            # Convert the SQLAlchemy results to a list of dictionaries
        attendance_data_list = [
                {"id": entry.id, "employee_id": entry.employee_id, "date": entry.date.strftime("%Y-%m-%d")}
                for entry in attendance_data
            ]
        transaction.commit()
        connection.close()
        response['status'] = True
        response['message'] = "data extract successfully"
        flash(response['message'], 'success')
        return attendance_data_list
    
    except Exception as e:
        transaction.rollback()
        connection.close()
        print("Error while adding user, Please contact administrator. : "+ str(e))
        flash("Error while adding user. Please contact the administrator.", 'error')
        return jsonify(response)     