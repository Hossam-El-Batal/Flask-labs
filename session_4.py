from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
## this gloval students can be accessed through any functions 
students = [{"id":1,"name":"ahmed"},{"id":2,"name":"samy"},{"id":3,"name":"mohamed"}]
## url_for returns the url of a certain endpoint for example home_page endpoint
## redirect returns me to a certain route 
## render template runs the template 

@app.route("/")
def home_page():
    ## this will return a json
    # return {"id":1,"name" : "hossam"}
    
    return render_template("index.html", students=students)


@app.route("/search/<int:id>")
def search_student(id):
    student = None
    for s in students:
        if s["id"] == id:
            student = s
            break
        
    return render_template("search_student.html", student=student)













if __name__ == "__main__":
    app.run(debug=True, port=5000)
