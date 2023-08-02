# 執行(terminal): flask run --->瀏覽器訪問 127.0.0.1:5000
# (Press CTRL+C to quit)
# 教學: https://ithelp.ithome.com.tw/articles/10258223
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for, jsonify, json, Response, send_from_directory
from sqlalchemy import text

app = Flask(__name__) 

# 設置資料庫連接地址
DB_URI='mysql+pymysql://root:@127.0.0.1:3306/subway_ease_up'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO']=True
# 初始化DB，關聯flask項目
db = SQLAlchemy()
db.init_app(app)  # 初始化db物件，將其與app關聯

# 裝飾器是告訴 Flask，哪個 URL 應該觸發我們的函式。
# 斜線代表的就是網站的根目錄，可以疊加。
@app.route('/SubwayEaseUp/station/home') #裝飾器
def home():
    return render_template('home.html')

@app.route('/SubwayEaseUp/station/get_station_data', methods=['GET']) #裝飾器
def get_station_data():
    sid = request.args.get('sid')
    route_way = request.args.get('route-way')
    sql=text('SELECT sid, sName, route, route_order, english_name FROM station WHERE sid=:sid')
    result = db.session.execute(sql, {'sid': sid})
    station_list = [{'sid': row[0], 'sName': row[1], 'route': row[2], 'route_order': row[3], 'english_name': row[4]} for row in result]
    return redirect(url_for('station_platform', sid=station_list[0]['sid'],sName=station_list[0]['sName'],english_name=station_list[0]['english_name'],route=station_list[0]['route'],route_order=station_list[0]['route_order'], route_way=route_way))

@app.route('/SubwayEaseUp/station/station_platform', methods=['GET']) #裝飾器
def station_platform():
    sid = request.args.get('sid')
    sName = request.args.get('sName')
    english_name = request.args.get('english_name')
    route = request.args.get('route')
    route_order = request.args.get('route_order')
    route_way = request.args.get('route_way')
    return render_template('station_platform.html', sid=sid, sName=sName, english_name=english_name, route=route, route_order=route_order, route_way=route_way)

@app.route('/get_car_data', methods=['GET', 'POST'])
def get_car_data():
    route_order=request.json.get('route_order')
    route_way=request.json.get('route_way')
    finalArr={}
    # Get Car Info
    if(route_way=='OT1' or route_way=='R24' or route_way=='C37'):
        "INSERT INTO `access_signal`(`cid`, `route_way`, `leave_station`, `enter_station`) VALUES ('168','OT1','1','0');"
        "SELECT cid, leave_station, enter_station, timestamp FROM (SELECT a1.* FROM access_signal AS a1 INNER JOIN ( SELECT cid, MAX(timestamp) AS max_timestamp FROM access_signal GROUP BY cid ) AS a2 ON a1.cid = a2.cid AND a1.timestamp = a2.max_timestamp WHERE route_way = 'OT1' AND leave_station <= 2  AND leave_station=(enter_station-1)) AS filtered_data ORDER BY ABS(leave_station - 2), timestamp DESC LIMIT 1;"
        access_signal_sql=text('SELECT cid, leave_station, enter_station, timestamp FROM (SELECT a1.* FROM access_signal AS a1 INNER JOIN ( SELECT cid, MAX(timestamp) AS max_timestamp FROM access_signal GROUP BY cid ) AS a2 ON a1.cid = a2.cid AND a1.timestamp = a2.max_timestamp WHERE route_way = :route_way AND leave_station <= :route_order AND leave_station = (enter_station + 1)) AS filtered_data ORDER BY ABS(leave_station - :route_order), timestamp DESC LIMIT 1;')
    else:
        access_signal_sql=text('SELECT cid, leave_station, enter_station, timestamp FROM (SELECT a1.* FROM access_signal AS a1 INNER JOIN ( SELECT cid, MAX(timestamp) AS max_timestamp FROM access_signal GROUP BY cid ) AS a2 ON a1.cid = a2.cid AND a1.timestamp = a2.max_timestamp WHERE route_way = :route_way AND leave_station >= :route_order AND leave_station = (enter_station + 1)) AS filtered_data ORDER BY ABS(leave_station - :route_order), timestamp DESC LIMIT 1;')
    
    access_signal_result = db.session.execute(access_signal_sql, {'route_way':route_way,'route_order': route_order})
    access_signal_list = [{'cid': row[0], 'leave_station': row[1], 'enter_station': row[2], 'timestamp': row[3]} for row in access_signal_result]
    car_sql=text('SELECT ci.cid, ci.cNo, ci.pNum, ci.air, ci.volumn, ci.timestamp FROM carriage_info AS ci JOIN (SELECT cNo, MAX(timestamp) AS max_timestamp FROM carriage_info WHERE cid = :accs_cid GROUP BY cNo) AS max_ci ON ci.cNo = max_ci.cNo AND ci.timestamp = max_ci.max_timestamp;')
    car_result = db.session.execute(car_sql, {'accs_cid': access_signal_list[0]['cid']})
    car_list =  [{'cid': row[0], 'cNo': row[1], 'pNum': row[2], 'air': row[3], 'volumn': row[4], 'timestamp': row[5]} for row in car_result]
    finalArr['access_signal']=access_signal_list
    finalArr['car_info']=car_list

    return jsonify(finalArr)


@app.route('/get_arrivedTimeInterval', methods=['GET', 'POST'])
def get_arrivedTimeInterval():
    with open('Station_Platform/static/json/arrivedTimeInterval.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)
    

if __name__ == '__main__':
    app.debug = True
    app.run()