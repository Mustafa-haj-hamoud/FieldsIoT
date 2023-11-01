# Import required libraries
from flask import Flask,render_template,request,session,redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from funcs import login_required

app = Flask(__name__)

db = SQL("sqlite:///fields.db")
#db = SQL("mysql://sql11654668:hdyALlvutz@sql11.freemysqlhosting.net:3306/sql11654668")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    firstname = session["firstname"]
    fields = db.execute("SELECT * FROM fields WHERE user_id = ? ORDER BY id", session["user_id"])
    return render_template("index.html", fields = fields , firstname = firstname)


@app.route("/login", methods=["GET","POST"])
def login():
    
    session.clear()
    
    if request.method == "GET":     
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        
        if not username or not password:
            return render_template("login.html", error = "Please provide both a username and a password")
        
        db_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        if not db_user:
            return render_template("login.html", error = "Username does not exist")

        if len(db_user) != 1 or not check_password_hash(db_user[0]["hash"], password):
            return render_template("login.html", error = "Incorrect Password")
            
        session["user_id"] = db_user[0]["id"]
        session["firstname"] = db_user[0]["firstname"].title()
        return redirect("/")
        
    else:
        return render_template("failed.html")
    
    
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":     
        return render_template("register.html")
    elif request.method == "POST":
        firstname = request.form.get("firstname").lower()
        lastname = request.form.get("lastname").lower()
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        
        print(request.form)
        
        if not firstname or not lastname or not username or not password or not confirmpassword:
            return render_template("failed.html", error = "You must fill out all fields while registering!")
        
        if password != confirmpassword:
            return render_template("failed.html", error = "Entered Passwords Must Match!")
        
        # check if user exists:
        check_username = db.execute("SELECT username FROM users WHERE username = ?",username)
        print(check_username)
        if check_username:
            return render_template("failed.html", error = "Username Already Exists")
        
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO users (firstname,lastname,username,hash) VALUES(?,?,?,?)", firstname, lastname, username, hashed)
        
        login()
        
        return redirect("/")
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@login_required
@app.route("/create", methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    
    elif request.method == "POST":
        fieldname = request.form.get("fieldname")
        value = request.form.get("value")
        
        if not fieldname:
            return render_template("create.html", error = "Field Not Created: Field Name is Required")
        
        db_fieldname = db.execute("SELECT * FROM fields WHERE user_id = ? AND field_name = ?",session["user_id"], fieldname)
        if db_fieldname:
            return render_template("create.html", error = f'Field Not Created: Field Name "{ fieldname }" Already Exists')
        
        if not value:
            value = 0
            
        db.execute("INSERT INTO fields (user_id, field_name, value) VALUES(?,?,?)", session["user_id"], fieldname, value)
        
        
        return render_template("create.html", success = f'Created Field "{fieldname}" Successfully With Initial Value {value}')
        
                
    else:
        return render_template("failed.html", error = "Method Not Allowed")
    
    
@app.route("/update")
def update():
    # request should look like this :
    # /update?user_id=1234  &  1=5  &  3=2
    
    fields = []
    user_id = request.args.get("user_id")
    if not user_id:
        return render_template("failed.html", error = "Please Provide a user_id in the request")
    field_ids = dict(request.args)
    field_ids.pop("user_id")
    
    for field in field_ids:
        
        # catch exception in case user enters a random string (not even a number)
        try:
            field_ids[field] = float(field_ids[field])
        except ValueError:
            field_ids[field] = "NO"
            continue
        
        if field_ids[field] % 1 != 0:
            field_ids[field] = "NO"
            continue
        
        #check whether field exists in database
        check_db = db.execute("SELECT * FROM fields WHERE user_id = ? AND id = ?", user_id , field)
        if not check_db:
            field_ids[field] = "NO"
        else:
            db.execute("UPDATE fields SET value = ? WHERE user_id = ? AND id = ?", field_ids[field], user_id, field)
            field_ids[field] = "YES"
        
    return render_template("update_success.html", field_ids=field_ids)


@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    if request.method == "GET":
        fields = db.execute("SELECT * FROM fields WHERE user_id = ? ORDER BY id", session["user_id"])
        return render_template("delete.html", fields=fields)
    
    else:
        user_id = request.form.get("user_id")
        field_id = request.form.get("field_id")
        
        db.execute("DELETE FROM fields WHERE user_id = ? AND id = ?", user_id, field_id)
        return redirect("/")
    

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "GET":
        session.clear()
        auth = 0
        return render_template("forgot.html", auth = auth)
    elif request.method == "POST":
        username = request.form.get("username").lower()
        user =  db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # check whether username exists in users database
        if not user:
            return render_template("forgot.html", error = "Username does not exist")
        
        firstname = request.form.get("firstname").lower()
        lastname = request.form.get("lastname").lower()
        
        if user[0]["firstname"] != firstname:
            return render_template("forgot.html", error="First Name Does Not Match, Try Again")
        
        if user[0]["lastname"] != lastname:
            return render_template("forgot.html", error="Last Name Does Not Match, Try Again")
        
        
        session["username_reset"] = username
        auth = 1
        return render_template("forgot.html", auth = auth)
    
@app.route("/reset", methods=["POST"])
def reset():
    password = request.form.get("password")
    confirmpassword = request.form.get("confirmpassword")
    
    if password != confirmpassword:
        return render_template("forgot.html", auth = 1, error = "Confirmation Must Match With Password")
    
    try:
        username = session["username_reset"]
    except KeyError:
        return render_template("failed.html", error = "Username was removed from cookies")
    
    password_hash = generate_password_hash(password)
    db.execute("UPDATE users SET hash = ? WHERE username = ?", password_hash,username)
    
    return redirect("/")
    

@app.route("/read_api")
@login_required
def read_api():
    # http://www.url.com/read?user_id=7&8=15
    
    link = request.host_url
    link += "read?"
    link += f"user_id={session['user_id']}"
    
    fields = db.execute("SELECT * FROM fields WHERE user_id = ?", session["user_id"])
    for field in fields:
        link += "&"
        link += str(field["id"])
    
    return render_template("read.html", link = link)


@app.route("/read")
def read():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify("INVALID USER ID")
    
    field_ids = dict(request.args)
    field_ids.pop("user_id")
    
    database_fields = db.execute("SELECT * FROM fields WHERE user_id = ?", user_id)
    result = []
    
    for dbfield in database_fields:
        dbfield_id = str(dbfield["id"])
        if dbfield_id in field_ids:
            result.append(dbfield)
            field_ids.pop(dbfield_id)
            
    if field_ids:
        return jsonify("USER ID AND FIELD IDS DO NOT MATCH")
    
    return jsonify(result)


@app.route("/password")
@login_required
def password():
    
    session["username_reset"] = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("forgot.html", auth = 1)