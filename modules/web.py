
@app.route('/')
def index():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('index.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))

@app.route('/home')
def home():
    try:
        var1 = "Welcome to the Python Flask"
        return render_template('manage_resources.html', var = var1)
    except Exception as e:
        print("exception while rendering index page : "+ str(e))
                                