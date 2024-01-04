
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