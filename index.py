from flask import *
from flask import Flask,render_template,request
import re
import pymongo

app=Flask(__name__)

client=pymongo.MongoClient("mongodb+srv://db:hemanthdb@hemanthcluster.tvtan.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('total_records')
register=db.register




@app.route('/')
def home():
    return render_template("signup.html")

#calling function
@app.route("/login",methods=["GET","POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    
    if(valid_email(email) and validate_password(password)):
        register.insert_one({"email":email,"password":password})
        return render_template("success.html")
    else:
        return render_template("Travel_Information.html")

def validate_password(password):
    l, u, p, d = 0, 0, 0, 0
    if (len(password)>= 8):
	    for i in password:

		# counting lowercase alphabets
		    if (i.islower()):
			    l+=1			

		# counting uppercase alphabets
		    if (i.isupper()):
			    u+=1			

		# counting digits
		    if (i.isdigit()):
			    d+=1			

		# counting the mentioned special characters
		    if(i=='@'or i=='$' or i=='_'):
			    p+=1		
    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
        return True
    else:
        return False
     


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[{A-Za-z0-9.-}]+\.[A-Z|a-z]{2,}\b'
    if(re.match(regex, email)):
        return True
    else:
        return False


@app.route("/signup",methods=["GET", "POST"])
def signup():
    Firstname=request.form.get("firstname")
    Lastname=request.form.get("lastname")
    email=request.form.get("email")
    password=request.form.get("password")
    if(valid_email(email) and validate_password(password)):
        register.insert_one({"firstname":Firstname,"Lastname":Lastname,"email":email,"password":password})
        return render_template("login.html")
    else:
        return render_template("error.html")


@app.route("/forgot",methods=['GET', 'POST'])
def forgot():
    new_password = request.form.get('New Password')
    ConfirmPassword=request.form.get('Confirm Password')
    if (validate_password(new_password)):
        return render_template('success.html')
    else:
        return render_template('error.html')
        #return render_template('forgot.html')




if __name__ == "__main__":
    app.run(debug=True)