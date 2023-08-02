# 執行(terminal): flask run --->瀏覽器訪問 127.0.0.1:5000
# (Press CTRL+C to quit)
# 教學: https://ithelp.ithome.com.tw/articles/10258223
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for, jsonify, json, Response, send_from_directory
from sqlalchemy import text
import datetime
# import io
# import base64
# import matplotlib.pyplot as plt

app = Flask(__name__) 

# 設置資料庫連接地址
DB_URI='mysql+pymysql://root:@127.0.0.1:3306/subway_ease_up'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO']=True
# 初始化DB，關聯flask項目
db = SQLAlchemy()
db.init_app(app)  # 初始化db物件，將其與app關聯


@app.route('/SubwayEaseUp/car/home') #裝飾器
def home():
    return render_template('home.html')

@app.route('/favicon.ico')
def favicon():
    # 返回該圖片作為 favicon.ico 圖標
    return send_from_directory(app.static_folder, 'images/logo.svg', mimetype='image/svg+xml')

@app.route('/SubwayEaseUp/car/onstation_template', methods=['GET']) #裝飾器
def onstation_template():
    cid = request.args.get('cid') # car id(車次)
    dNo = request.args.get('dNo') # door number(車門號)
    cNo = (int(dNo)//4)+1 #carriage number(車廂號)
    route = request.args.get('route')
    route_way = request.args.get('route_way')
    now= datetime.datetime.now()
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    return render_template('v0_car_onstation_platform.html', cid=cid, cNo=cNo, dNo=dNo, route=route, route_way=route_way, hour=hour, minute=minute)

@app.route('/SubwayEaseUp/car/car_onstation_platform', methods=['GET']) #裝飾器
def car_onstation_platform():
    cid = request.args.get('cid') # car id(車次)
    dNo = request.args.get('dNo') # door number(車門號)
    cNo = (int(dNo)//4)+1 #carriage number(車廂號)
    route = request.args.get('route')
    route_way = request.args.get('route_way')
    now= datetime.datetime.now()
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    
    return render_template('car_onstation_platform.html', cid=cid, cNo=cNo, dNo=dNo, route=route, route_way=route_way, hour=hour, minute=minute)

@app.route('/get_initial_onstation_data', methods=['POST'])
def get_initial_onstation_data():
    
    cid=request.json.get('cid')
    dNo=request.json.get('dNo')
    route=request.json.get('route')
    route_way=request.json.get('route_way')
    cNo = int(dNo)//4 + 1
    final_result={}

    # Get Car Info
    car_sql=text('SELECT ci.cid, ci.cNo, ci.pNum, ci.air, ci.volumn, accs.leave_station, accs.enter_station, accs.route_way, accs.timestamp FROM carriage_info AS ci JOIN ( SELECT cid, route_way, leave_station, enter_station, timestamp FROM access_signal WHERE cid=:cid ORDER BY timestamp DESC LIMIT 1) AS accs ON ci.cid=accs.cid WHERE ci.cid=:cid AND ci.cNo=:cNo ORDER BY ci.timestamp DESC LIMIT 1;')
    car_result = db.session.execute(car_sql, {'cid': cid, 'cNo': cNo})
    car_list =  [{'cid': row[0], 'cNo': row[1], 'pNum': row[2], 'air': row[3], 'volumn': row[4], 'leave_station': row[5], 'enter_station': row[6], 'route_way': row[7], 'timestamp':row[8] } for row in car_result]
    final_result['car']=car_list

    # Get Station Info
    sql = text('SELECT station.sid,  station.sName,  station.english_name, fl.facility_type, fl.facility_way, fl.relative_position FROM station JOIN (SELECT * FROM facility_location WHERE way=:route_way ORDER BY relative_position DESC) AS fl ON fl.sid=station.sid WHERE route=:route AND route_order=:route_order')
    result = db.session.execute(sql, {'route_way': route_way, 'route': route, 'route_order': car_list[0]['enter_station']})

    # sql=text('SELECT station.sid,  station.sName,  station.english_name, fl.facility_type, fl.facility_way, fl.relative_position FROM station JOIN (SELECT * FROM facility_location WHERE way=:route_way ORDER BY relative_position) AS fl ON fl.sid=station.sid WHERE route=:route AND route_order=:route_order')
    # result = db.session.execute(sql, {'route_way': route_way,'route': route, 'route_order': car_list[0]['enter_station']})
    station_list = [{'sid': row[0], 'sName': row[1], 'english_name': row[2], 'facility_type': row[3], 'facility_way': row[4], 'relative_position': row[5]} for row in result]
    final_result['station']=station_list
    
    return jsonify(final_result)

@app.route('/SubwayEaseUp/car/car_onmove_platform', methods=['GET']) #裝飾器
def car_onmove_platform():
    cid = request.args.get('cid') # car id(車次)
    dNo = request.args.get('dNo') # door number(車門號)
    cNo = (int(dNo)//4)+1 #carriage number(車廂號)
    route = request.args.get('route')
    route_way = request.args.get('route_way')
    now= datetime.datetime.now()
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    return render_template('car_onmove_platform.html', cid=cid, cNo=cNo, dNo=dNo, route=route, route_way=route_way, hour=hour, minute=minute)


@app.route('/get_station_data', methods=['POST'])
def get_station_data():
    route=request.json.get('route')
    route_way=request.json.get('route_way')
    cid=request.json.get('cid')
    dNo=request.json.get('dNo')

    finalArr={}
    # Get Car Info
    car_sql=text('SELECT cid, route_way, leave_station, enter_station, timestamp FROM access_signal WHERE cid=:cid ORDER BY timestamp DESC LIMIT 1')
    car_result = db.session.execute(car_sql, {'cid': cid})
    car_list =  [{'cid': row[0], 'route_way':row[1], 'leave_station': row[2], 'enter_station': row[3], 'timestamp':row[4]} for row in car_result]
        
    # Get Station Info
    if route_way=="OT1" or route_way=="R24" or route_way=="C37":
        sql=text('SELECT * FROM station WHERE route=:route ORDER BY route_order')
    elif route_way=="O1" or route_way=="R3" or route_way=="C1":
        sql=text('SELECT * FROM station WHERE route=:route ORDER BY route_order DESC')
    result = db.session.execute(sql, {'route': route})
    station_list = [{'idx': row[0], 'sid': row[1], 'sName': row[2], 'route': row[3], 'route_order': row[4], 'english_name': row[5]} for row in result]
    finalArr['car']=car_list
    finalArr['station']=station_list
    return jsonify(finalArr)

@app.route('/get_car_data', methods=['POST'])
def get_car_data():
    cid=request.json.get('cid') # car id(車次)
    dNo=request.json.get('dNo')
    cNo = int(dNo)//4 + 1 # carriage number(車廂號)
    # Get Car Info
    car_sql=text('SELECT ci.cid, ci.cNo, ci.pNum, ci.air, ci.volumn, accs.leave_station, accs.enter_station, accs.route_way, accs.timestamp FROM carriage_info AS ci JOIN ( SELECT cid, leave_station, enter_station, route_way, timestamp FROM access_signal WHERE cid=:cid ORDER BY timestamp DESC LIMIT 1) AS accs ON ci.cid=accs.cid WHERE ci.cid=:cid AND ci.cNo=:cNo ORDER BY ci.timestamp DESC LIMIT 1;')
    car_result = db.session.execute(car_sql, {'cid': cid, 'cNo': cNo})
    car_list =  [{'cid': row[0], 'cNo': row[1], 'pNum': row[2], 'air': row[3], 'volumn': row[4], 'leave_station': row[5], 'enter_station': row[6], 'route_way': row[7], 'timestamp':row[8]} for row in car_result]
    
    return jsonify(car_list)

@app.route('/get_arrivedTimeInterval', methods=['GET', 'POST'])
def get_arrivedTimeInterval():
    with open('Car_Panel/static/json/arrivedTimeInterval.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

@app.route('/demo_insert', methods=['POST'])
def demo_insert():
    cid=request.json.get('cid')
    dNo=request.json.get('dNo')
    cNo = int(dNo)//4 + 1
    # Get Car Info
    car_sql=text('SELECT cid, leave_station, enter_station, route_way FROM access_signal WHERE cid=:cid ORDER BY timestamp DESC LIMIT 1')
    car_result = db.session.execute(car_sql, {'cid': cid})
    car_list =  [{'cid': row[0], 'leave_station': row[1], 'enter_station': row[2], 'route_way': row[3]} for row in car_result]
    
    # It has been to final station
    if(car_list[0]['enter_station']==3):
        return jsonify({'message': 2})
    
    pro_sql=text('INSERT INTO `access_signal`(`cid`, `leave_station`, `enter_station`, `route_way`) VALUES (:cid, :leave, :enter, :route_way);')
    if(car_list[0]['leave_station']==car_list[0]['enter_station']):
        pro_result = db.session.execute(pro_sql, {'cid': cid, 'leave': car_list[0]['leave_station']+1, 'enter':car_list[0]['enter_station'], 'route_way': car_list[0]['route_way']})
    elif(car_list[0]['leave_station']!=car_list[0]['enter_station']):
        pro_result = db.session.execute(pro_sql, {'cid': cid, 'leave': car_list[0]['leave_station'], 'enter':car_list[0]['enter_station']+1, 'route_way': car_list[0]['route_way']})
    
    db.session.commit()

    return jsonify({'message': 1})

if __name__ == '__main__':
    app.debug = True
    app.run()