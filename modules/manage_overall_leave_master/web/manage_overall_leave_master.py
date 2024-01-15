
@app.route('/manage_overall_leave_master')
def manage_overall_leave_master():
    try:
        return render_template('manage_overall_leave_master.html')
    except Exception as e :
        return e
    
@app.route('/retrive_tb_overall_leave_master', methods=["GET"])
@login_required
@runtime_logger
def retrive_tb_overall_leave_master():
    response = {
        "rows": [],
        "total": 0,
        "message": ""
    }
    try:

        request_data = {}
        request_data['search'] = request.args.get('search')
        request_data['status'] = request.args.get('status')
        request_data['limit'] = request.args.get('limit', type=int)
        request_data['offset'] = request.args.get('offset', type=int)

        result_leaves = get_overall_leave_master_info(request_data, app._engine.connect())
        if result_leaves['status']:
            response['status'] = True
            response['message'] = 'Overall Leave Master details retrived successfully.'
            response['rows'] = result_leaves['rows']
            response['total'] = result_leaves['total']
            return jsonify(response)
        else:
            response['message'] = result_leaves['message']
            return jsonify(response)

    except Exception as e:
        print("Error while retrieving leave data: " + str(e))
        return jsonify(response)    