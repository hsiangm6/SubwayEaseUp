#車載面板伺服器
# 執行(terminal): flask run --->瀏覽器訪問 127.0.0.1:5000
# (Press CTRL+C to quit)
# 教學: https://ithelp.ithome.com.tw/articles/10258223
from flask import Flask, request, render_template, redirect, url_for, jsonify, json, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import random

app = Flask(__name__)

# 設置資料庫連接地址
DB_URI = 'mysql+pymysql://root:@127.0.0.1:3306/subway_ease_up'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO'] = True
# 初始化DB，關聯flask項目
db = SQLAlchemy()
db.init_app(app)  # 初始化db物件，將其與app關聯


# 裝飾器是告訴 Flask，哪個 URL 應該觸發我們的函式。
# 斜線代表的就是網站的根目錄，可以疊加。
@app.route('/SubwayEaseUp/station/home')  # 裝飾器
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    # 返回該圖片作為 favicon.ico 圖標
    return send_from_directory(app.static_folder, 'images/logo.svg', mimetype='image/svg+xml')


@app.route('/SubwayEaseUp/station/get_station_data', methods=['GET'])  # 裝飾器
def get_station_data():
    sid = request.args.get('sid')
    route_way = request.args.get('route-way')
    sql = text('SELECT sid, sName, route, route_order, english_name FROM station WHERE sid=:sid')
    result = db.session.execute(sql, {'sid': sid})
    station_list = [{'sid': row[0], 'sName': row[1], 'route': row[2], 'route_order': row[3], 'english_name': row[4]} for
                    row in result]
    return redirect(url_for('station_platform', sid=station_list[0]['sid'], sName=station_list[0]['sName'],
                            english_name=station_list[0]['english_name'], route=station_list[0]['route'],
                            route_order=station_list[0]['route_order'], route_way=route_way))


@app.route('/SubwayEaseUp/station/station_platform', methods=['GET'])  # 裝飾器
def station_platform():
    s_id = request.args.get('sid')
    s_name = request.args.get('sName')
    english_name = request.args.get('english_name')
    route = request.args.get('route')
    route_order = request.args.get('route_order')
    route_way = request.args.get('route_way')
    return render_template('station_platform.html', sid=s_id, sName=s_name, english_name=english_name, route=route,
                           route_order=route_order, route_way=route_way)


@app.route('/get_car_data', methods=['GET', 'POST'])
def get_car_data():
    route_order = request.json.get('route_order')
    route_way = request.json.get('route_way')
    final_arr = {}
    # Get Car Info
    access_signal_sql = text(
        'SELECT cid, leave_station, enter_station, timestamp, route_way '
        'FROM ('
        '   SELECT route_way, enter_station, leave_station, a1.cid, timestamp FROM access_signal AS a1 '
        '   INNER JOIN ( '
        '       SELECT cid, MAX(timestamp) AS max_timestamp '
        '       FROM access_signal '
        '       WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 50 MINUTE) '
        '       GROUP BY cid '
        '   ) AS a2 '
        '   ON a1.cid = a2.cid AND a1.timestamp = a2.max_timestamp '
        '   WHERE route_way = :route_way AND leave_station <= :route_order'
        ') AS filtered_data '
        'ORDER BY ABS(leave_station - :route_order), ABS(enter_station - :route_order) '
        'LIMIT 1;'
    )

    if route_way == 'OT1' or route_way == 'R24' or route_way == 'C37':
        access_signal_result = db.session.execute(access_signal_sql,
                                                  {'route_way': route_way, 'route_order': route_order})
    else:
        access_signal_result = db.session.execute(access_signal_sql,
                                                  {'route_way': route_way, 'route_order': 5 - 1 - int(route_order)})

    access_signal_list = [
        {'cid': row[0], 'leave_station': row[1], 'enter_station': row[2], 'timestamp': row[3], 'route_way': row[4]} for
        row in access_signal_result]

    if not access_signal_list:
        car_list = []
    else:
        car_sql = text(
            'SELECT ci.cid, ci.cNo, ci.dNo, ci.pNum, ci.air, ci.volume, ci.timestamp '
            'FROM carriage_info AS ci JOIN ('
            '   SELECT cNo, MAX(timestamp) AS max_timestamp '
            '   FROM carriage_info WHERE cid = :accs_cid GROUP BY cNo'
            ') AS max_ci '
            'ON ci.cNo = max_ci.cNo AND ci.timestamp = max_ci.max_timestamp;'
        )
        car_result = db.session.execute(car_sql, {'accs_cid': access_signal_list[0]['cid']})
        car_list = [{'cid': row[0], 'cNo': row[1], 'dNo': row[2], 'pNum': row[3], 'air': row[4], 'volume': row[5],
                     'timestamp': row[6]}
                    for row in car_result]

    final_arr['access_signal'] = access_signal_list
    final_arr['car_info'] = car_list

    return jsonify(final_arr)


@app.route('/get_arrived_time_interval', methods=['GET', 'POST'])
def get_arrived_time_interval():
    with open('Station_Platform/static/json/arrivedTimeInterval.json') as json_file:
        # with open('../Station_Platform/static/json/arrivedTimeInterval.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

#進站訊號
@app.route('/access_signal', methods=['GET', 'POST'])
def access_signal():
    c_id = request.args.get('c_id')  # 車次
    route_way = request.args.get('route_way')  # 路線方向
    leave_station = request.args.get('leave_station')  # 離站數
    enter_station = request.args.get('enter_station')  # 進站數

    insert_sql = text(
        'INSERT INTO `access_signal`(`cid`, `route_way`, `leave_station`, `enter_station`) '
        'VALUES (:cid, :route_way, :leave, :enter);')

    db.session.execute(insert_sql, {
        'cid': c_id,
        'route_way': route_way,
        'leave': leave_station,
        'enter': enter_station})

    db.session.commit()

    return jsonify({'message': 'Success'})

#車廂內部資訊
@app.route('/carriage_info', methods=['GET', 'POST'])
def carriage_info():
    c_id = request.args.get('c_id')  # 車次
    c_no = request.args.get('cNo')  # 車廂號
    p_num = request.args.get('pNum')  # 壅擠程度
    air = request.args.get('air')  # 有毒氣體
    volume = request.args.get('volume')  # 異常聲音

    insert_sql = text(
        'INSERT INTO `carriage_info`(`cid`, `cNo`, `dNo`, `pNum`, `air`, `volume`) '
        'VALUES (:cid, :cNo, :dNo, :pNum, :air, :volume);')

    db.session.execute(insert_sql, {
        'cid': c_id,
        'cNo': c_no,
        'dNo': 1,
        'pNum': p_num,
        'air': air,
        'volume': volume})

    db.session.commit()

    return jsonify({'message': 'Success'})


@app.route('/demo_insert', methods=['POST'])
def demo_insert():
    leave_station = request.json.get('leave_station')
    enter_station = request.json.get('enter_station')

    accs_sql = text(
        'INSERT INTO `access_signal`(`cid`, `leave_station`, `enter_station`, `route_way`) '
        'VALUES (:cid, :leave, :enter, :route_way);')

    db.session.execute(accs_sql, {
        'cid': 168, 'leave': leave_station,
        'enter': enter_station,
        'route_way': 'OT1'})
    db.session.commit()

    p_num_test = random.randint(0, 2)
    p_num = ''

    if p_num_test == 0:
        p_num = "不壅擠"
    elif p_num_test == 1:
        p_num = "尚可"
    elif p_num_test == 2:
        p_num = "壅擠"

    ci_sql = text(
        'INSERT INTO `carriage_info`(`cid`, `cNo`, `dNo`, `pNum`, `air`, `volume`) '
        'VALUES (:cid, :cNo, :dNo, :pNum, :air, :volume);')

    db.session.execute(ci_sql, {
        'cid': 168,
        'cNo': 1,
        'dNo': 1,
        'pNum': p_num,
        'air': random.random() * 2.5,
        'volume': random.random() * 2.5})

    db.session.commit()

    return jsonify({'leave_station': leave_station, 'enter_station': enter_station})


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001, host="0.0.0.0") #允許外部設備連接
    # app.run(port=5001)
