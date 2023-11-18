

@app.route('/login', methods=['GET'])
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        print("exception while rendering login page : "+ str(e))
        return redirect('/')