from flask import Flask, render_template, url_for, redirect
from flask import request, session # routing data through pages without calling db everytime
from datetime import timedelta
from flask import flash


app = Flask(__name__)
app.secret_key = "Ahmed123" # session key
app.permanent_session_lifetime = timedelta(days=1) # session_lifetime

@app.route("/home")
@app.route("/")
def home_page():
    return render_template("home.html")

# def login_page():
#     return render_template("login.html")

# app.add_url_rule("/login", view_func=login_page)

## http methods [GET, POST]

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST": # POST
        user_name = request.form['nm']
        password = request.form['ps']
        confirm_password = request.form['confirm_ps']
        # validate confirm == password
        if password == confirm_password:
            # validate db
            return f"Username is {user_name}, Password is {password}"
        else:
            return f"confirm password and password doesnt match"
    else: # GET
        return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET": 
        if 'username' in session:
            flash("You are already logged in", "info")  
            return redirect(url_for('user.profile'))  
        else:
            return render_template("login.html")

    else:  # POST request
        user_name = request.form['nm']
        password = request.form['ps']

        session['username'] = user_name
        session['password'] = password  
        flash("Successfully logged in", "info")
        return redirect(url_for('user.profile'))  

    
@app.route("/profile", endpoint = "user.profile")
def show_profile():
    if 'username' in session.keys():
        
      name = session['username']
      password = session['password']
      return render_template("profile.html", name = name )
    else:
        flash("session ended, login again !", "info")
        return redirect(url_for("login"))

# lab 2 

@app.route("/logout")
def logout():
     if 'username' in session.keys():
        
      session.pop('username')
      session.pop('password')
      return redirect(url_for("home_page"))
     else:
       return redirect(url_for("home_page"))
      
 
if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True, port=5000)