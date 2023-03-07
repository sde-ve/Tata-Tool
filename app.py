from flask import Flask, redirect, url_for, request, render_template,send_file , session
import json
from flask_mysqldb import MySQL
from pymysql import*
import xlwt
import pandas.io.sql as sql
from  sms_info_bip import *
import pandas as pd
app = Flask(__name__)

app.secret_key = 'your_secret_key_here'
database_conn= open("config.json", 'r')
configuration= json.load(database_conn)
app.config['MYSQL_HOST'] = configuration['host']
app.config['MYSQL_USER'] = configuration['user']
app.config['MYSQL_PASSWORD'] = configuration['password']
app.config['MYSQL_DB'] = configuration['database']

con=connect(user= configuration['user'],password=configuration['password'],host= configuration['host'],database=configuration['database'])
mysql = MySQL(app)

 
        
@app.route('/', methods=['POST', 'GET'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur.execute("SELECT * from login where username='{}' and password='{}'".format(username,password) )
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            if 'username' in session:
             username = 'Welcome '+session['username']
            return render_template('base.html', username=username)
    
        else:
            return render_template('login.html',msg='Incorrect username/password!')
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
            username = session['username']
            return render_template('base.html', username=username)
    else:
        return render_template('login.html')
      

@app.route('/pincode', methods=['POST', 'GET'])
def input(): 
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        pincode = request.form['pin_code']
        cur.execute("SELECT * from servicing_pin  where pin_code='{}'".format(pincode) )
        service_table_data = cur.fetchone()
        if service_table_data != None: 
            username = session['username']
            return render_template('form.html',pincode =pincode ,username=username)
        
        else:
            message="Your location is not eligible for pick - up"
            return render_template('input.html',message=message)
        
    else:
        return  render_template('/input.html')

 

@app.route('/add-data',methods=['GET','POST'])
def storeData():
    cur = mysql.connection.cursor()
     
    if request.method == 'POST' :
        #passing HTML form data into python variable
         
        cseName=request.form['cse_name']
        policyNo=request.form['policy_no']
        pickupPin=request.form['pickup_pin']
        pickupAddress= request.form['pickup_address']
        contactPerson= request.form['contact_person']
        mobileNo= request.form['mobile_no']
        cur.execute('INSERT INTO pick_up_detail(cse_name, policy_no, pick_up_pin,pick_up_address, contact_person, mobile_no) values("{}","{}","{}","{}","{}","{}")'.format(cseName , policyNo, pickupPin, pickupAddress,contactPerson,mobileNo ))
        mysql.connection.commit()
           
        
    return redirect('pincode')
    

def get_data(page):
    per_page = 12 # Number of items to display per page
    offset = (page - 1) * per_page # Calculate offset based on page number
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM pick_up_detail LIMIT {per_page} OFFSET {offset}")
    data = cur.fetchall()
    return data

@app.route('/pick-up-detail', methods=['GET'])
def pickUpDetail():
    page = request.args.get('page', 1, type=int)
    data = get_data(page)
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM pick_up_detail")
    total_rows = cur.fetchone()[0]

    total_pages = total_rows // 10 # Calculate total number of pages
     
    return render_template('show_pickup_detail.html', data=data, total_pages=total_pages )

@app.route('/download-detail')
def generate_excel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from pick_up_detail")
    result = cur.fetchall()
    results=json.dumps(result, indent=4, default=str)
    pd.read_json(results).to_excel("pick_up_detail.xlsx")
    outputData=pd.read_excel("pick_up_detail.xlsx")
    return send_file('pick_up_detail.xls')
    
    # return send_file(output, attachment_filename='pick_up_detail.xls', as_attachment=True)


@app.route('/upload-list', methods=['GET','POST'])
def uploadList():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
                       
        file=request.files['upload_file']
        data=pd.read_excel(file)
        df = data
        df.reset_index(inplace=True)
        
        json_str = json.loads(df.to_json(orient='records',date_format='iso'))
        jsonInputs = json_str
        try:
            cur = mysql.connection.cursor()
            jsonOutputs=[]
            for jsoninputstring in jsonInputs:
                try:
                    Policy_Number = jsoninputstring['Policy_Number']
                except:
                    raise Exception("Policy Number is empty")
            
                try:
                    mobile_number = str(jsoninputstring['Mobile Number'])
                except:
                    raise Exception("Mobile Number is empty")
            
                try:
                    xx1 = str(jsoninputstring['XX1'])
                except:
                    raise Exception("XX1 is empty")
                try:
                    xx2 = str(jsoninputstring['XX2'])
                except:
                    raise Exception("XX2")
                try:
                    xx3 = str(jsoninputstring['XX3'])
                except:
                    raise Exception("XX3  is empty")
                
                try:
                    xx4 = str(jsoninputstring['XX4'])
                except:
                    raise Exception("XX4 is empty")
                try:
                    xx5 = str(jsoninputstring['XX5'])
                except:
                    raise Exception("XX5")
                try:
                    xx6 = str(jsoninputstring['XX6'])
                except:
                    raise Exception("XX6  is empty")
# compny name is change 
                if xx3 == "DIAMOND SAVINGS PLAN":
                    xx3 = "DIAMOND SAVINGS PLAN"
                elif xx3 == "TATA AIA FORTUNE PRO":
                    xx3 = "TATA AIA FORTUNE PRO"
                elif xx3 == "Tata AIA Life Guaranteed Return Insurance Plan":
                    xx3 = "Tata AIA Life G.R.I.P"
                elif xx3 == "Tata AIA Life Insurance Fortune Pro":
                    xx3 = "Tata AIA Life Insurance Fortune Pro"
                elif xx3 == "TATA AIA LIFE INSURANCE POS SMART INCOME PLUS":
                    xx3 = "TATA AIA LIFE INSURANCE POS S.I.P."
                elif xx3 == "TATA AIA LIFE INSURANCE SMART INCOME PLUS":
                    xx3 = "TATA AIA LIFE INSURANCE S.I.P."
                elif xx3 == "Tata AIA Life Insurance Wealth Pro":
                    xx3 = "Tata AIA Life Insurance Wealth Pro"
                elif xx3 == "TATA AIA WEALTH PRO":
                    xx3 = "TATA AIA WEALTH PRO"
                    
                cur.execute("select*from data_list where policy_no= '{}'".format(Policy_Number))
                data_list_table = cur.fetchone() 
                if data_list_table == None:
                    cur.execute("insert into data_list(policy_no, mobile_no, XX1, XX2, XX3, XX4, XX5, XX6) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(Policy_Number,mobile_number,xx1,xx2,xx3,xx4,xx5,xx6))
                else:
                    cur.execute("update data_list set mobile_no = '{}', XX1 = '{}', XX2 = '{}', XX3 = '{}', XX4 = '{}', XX5 = '{}', XX6 = '{}' ".format(mobile_number, xx1,xx2,xx3,xx4,xx5,xx6))
                
                    
                mysql.connection.commit()
        except Exception as e:
                warning_message = {"Message":"Error Message : " + str(e),"flag":0}
                return render_template ("upload_list.html",message = warning_message)
        
        return render_template ("upload_list.html",message="your data is successfully stored")
        
    else :
        return  render_template ("upload_list.html")

@app.route('/send-sms',methods=['POST','GET'])
def sms():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        policy_no =request.form['policy_no']
        cur.execute("select*from data_list where policy_no= '{}'".format(policy_no))
        sms_data = cur.fetchone()
        mobile_number = sms_data[2]
        xx1 = sms_data[3]
        xx2 = sms_data[4]
        xx3 = sms_data[5]
        xx4 = sms_data[6]
        xx5 = sms_data[7]
        xx6 = sms_data[8]
    
        sendSMS=SendSMS()
             
        sendSMS.send(recipient=  "91"+str(mobile_number),name = xx1,premium=xx2,company =xx3,contract=xx4,regard= xx5,age = xx6)
            
        return render_template("success.html", message = "Your message is successfully sent")
    else :
        cur.execute("SELECT policy_no from data_list")
        result = cur.fetchall()
        data_list = []
        for x in result:
            data_list.append (x[0])

        return render_template ("sms.html",data_list=data_list)
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run()
