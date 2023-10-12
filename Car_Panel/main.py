# 執行(terminal): flask run --->瀏覽器訪問 127.0.0.1:5000
# (Press CTRL+C to quit)
# 教學: https://ithelp.ithome.com.tw/articles/10258223
import datetime
import random
from flask import Flask, request, render_template, jsonify, json, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import aiohttp  # 提供了异步的 HTTP 客户端和服务器

# import asyncio  Python 提供的异步编程框架

app = Flask(__name__)

# 設置資料庫連接地址
DB_URI = 'mysql+pymysql://root:@127.0.0.1:3306/subway_easy_up_car'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO'] = True
# 初始化DB，關聯flask項目
db = SQLAlchemy()
db.init_app(app)  # 初始化db物件，將其與app關聯


@app.route('/')
@app.route('/SubwayEaseUp/car/home')  # 裝飾器
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    # 返回該圖片作為 favicon.ico 圖標
    return send_from_directory(app.static_folder, 'images/logo.svg', mimetype='image/svg+xml')


# @app.route('/SubwayEaseUp/car/on_station_template', methods=['GET'])  # 裝飾器
# def on_station_template():
#     c_id = request.args.get('cid')  # car id(車次)
#     d_no = request.args.get('dNo')  # door number(車門號)
#     c_no = (int(d_no) // 4) + 1  # carriage number(車廂號)
#     route = request.args.get('route')
#     route_way = request.args.get('route_way')
#     now = datetime.datetime.now()
#     hour = str(now.hour).zfill(2)
#     minute = str(now.minute).zfill(2)
#     return render_template('v0_car_on_station_platform.html', cid=c_id, cNo=c_no, dNo=d_no, route=route,
#                            route_way=route_way, hour=hour, minute=minute)


@app.route('/SubwayEaseUp/car/car_on_station_platform', methods=['GET'])  # 裝飾器
def car_on_station_platform():
    c_id = request.args.get('cid')  # car id(車次)
    d_no = request.args.get('dNo')  # door number(車門號)
    c_no = (int(d_no) // 4) + 1  # carriage number(車廂號)
    now = datetime.datetime.now()
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)

    return render_template('car_on_station_platform.html', cid=c_id, cNo=c_no, dNo=d_no, hour=hour, minute=minute)


@app.route('/get_initial_on_station_data', methods=['POST'])
def get_initial_on_station_data():
    c_id = request.json.get('cid')
    d_no = request.json.get('dNo')
    c_no = int(d_no) // 4 + 1
    final_result = {}

    # Get Car Info
    car_sql = text(
        'SELECT ci.cid, ci.cNo, ci.pNum, ci.air, ci.volume, accs.leave_station, accs.enter_station, accs.route_way, '
        '       accs.timestamp '
        'FROM carriage_info AS ci JOIN ( '
        '   SELECT cid, route_way, leave_station, enter_station, timestamp '
        '   FROM access_signal '
        '   WHERE cid=:cid '
        '   ORDER BY timestamp '
        '   DESC LIMIT '
        '1) AS accs '
        'ON ci.cid=accs.cid '
        'WHERE ci.cid=:cid AND ci.cNo=:cNo '
        'ORDER BY ci.timestamp '
        'DESC LIMIT 1;'
    )

    car_result = db.session.execute(car_sql, {'cid': c_id, 'cNo': c_no})
    car_list = [{'cid': row[0], 'cNo': row[1], 'pNum': row[2], 'air': row[3], 'volume': row[4], 'leave_station': row[5],
                 'enter_station': row[6], 'route_way': row[7], 'timestamp': row[8]} for row in car_result]
    final_result['car'] = car_list

    route_way = car_list[0]['route_way']
    route = route_way[0]
    final_result['route_way'] = [route_way]

    # Get Station Info(relative_position of facility(0~11))
    sql = text(
        'SELECT station.sid,  station.sName,  station.english_name, fl.facility_type, fl.facility_way, '
        '       fl.relative_position '
        'FROM station LEFT JOIN ('
        '   SELECT * FROM facility_location '
        '   WHERE way=:route_way '
        '   ORDER BY relative_position'
        ') AS fl '
        'ON fl.sid=station.sid '
        'WHERE route=:route AND route_order=:route_order'
    )

    if route_way == "OT1" or route_way == "R24" or route_way == "C37":
        result = db.session.execute(sql, {'route_way': route_way, 'route': route,
                                          'route_order': car_list[0]['enter_station']})
    else:
        result = db.session.execute(sql, {'route_way': route_way, 'route': route, 'route_order': 5 - 1 - car_list[0][
            'enter_station']})  # 5 代表的是總站數，如果站數更改，此處也要更改
    station_list = [
        {'sid': row[0], 'sName': row[1], 'english_name': row[2], 'facility_type': row[3], 'facility_way': row[4],
         'relative_position': row[5]} for row in result]
    final_result['station'] = station_list

    # Get Station Exit
    exit_sql = text(
        'SELECT * FROM `station_exit` '
        'WHERE sid=:sid '
        'ORDER BY ePosition'
    )

    exit_result = db.session.execute(exit_sql, {'sid': station_list[0]['sid']})
    exit_list = [{'idx': row[0], 'sid': row[1], 'eNo': row[2], 'eName': row[3], 'eName_en': row[4], 'ePosition': row[5]}
                 for row in exit_result]
    final_result['station_exit'] = exit_list

    return jsonify(final_result)


@app.route('/SubwayEaseUp/car/car_on_move_platform', methods=['GET'])  # 裝飾器
def car_on_move_platform():
    c_id = request.args.get('cid')  # car id(車次)
    d_no = request.args.get('dNo')  # door number(車門號)
    c_no = (int(d_no) // 4) + 1  # carriage number(車廂號)
    now = datetime.datetime.now()
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    return render_template('car_on_move_platform.html', cid=c_id, cNo=c_no, dNo=d_no, hour=hour, minute=minute)


@app.route('/get_station_data', methods=['POST'])
def get_station_data():
    cid = request.json.get('cid')

    final_arr = {}
    # Get Car Info
    car_sql = text(
        'SELECT cid, route_way, leave_station, enter_station, timestamp '
        'FROM access_signal '
        'WHERE cid=:cid '
        'ORDER BY timestamp '
        'DESC LIMIT 1'
    )

    car_result = db.session.execute(car_sql, {'cid': cid})
    car_list = [
        {'cid': row[0], 'route_way': row[1], 'leave_station': row[2], 'enter_station': row[3], 'timestamp': row[4]} for
        row in car_result]
    route_way = car_list[0]['route_way']
    route = route_way[0]
    # Get Station Info
    if route_way == "OT1" or route_way == "R24" or route_way == "C37":
        sql = text(
            'SELECT * FROM station '
            'WHERE route=:route '
            'ORDER BY route_order'
        )

    else:
        sql = text(
            'SELECT * FROM station '
            'WHERE route=:route '
            'ORDER BY route_order DESC'
        )

    result = db.session.execute(sql, {'route': route})
    station_list = [
        {'idx': row[0], 'sid': row[1], 'sName': row[2], 'route': row[3], 'route_order': row[4], 'english_name': row[5]}
        for row in result]
    final_arr['car'] = car_list
    final_arr['station'] = station_list
    return jsonify(final_arr)


@app.route('/get_car_data', methods=['POST'])
def get_car_data():
    c_id = request.json.get('cid')  # car id(車次)
    d_no = request.json.get('dNo')
    c_no = int(d_no) // 4 + 1  # carriage number(車廂號)
    final_arr = {}

    # Get Car Info
    car_sql = text(
        'SELECT ci.cid, ci.cNo, ci.pNum, ci.air, ci.volume, '
        '       accs.leave_station, accs.enter_station, accs.route_way, accs.timestamp '
        'FROM carriage_info AS ci '
        'JOIN ( '
        '       SELECT cid, leave_station, enter_station, route_way, timestamp '
        '       FROM access_signal '
        '       WHERE cid=:cid '
        '       ORDER BY timestamp DESC LIMIT 1 '
        ') AS accs ON ci.cid=accs.cid '
        'WHERE ci.cid=:cid AND ci.cNo=:cNo  AND ci.dNo=:dNo '
        'ORDER BY ci.timestamp DESC LIMIT 1;')
    car_result = db.session.execute(car_sql, {'cid': c_id, 'cNo': c_no, 'dNo': d_no})
    car_list = [{'cid': row[0], 'cNo': row[1], 'pNum': row[2], 'air': row[3], 'volume': row[4], 'leave_station': row[5],
                 'enter_station': row[6], 'route_way': row[7], 'timestamp': row[8]} for row in car_result]

    # Get Warning about air and volume
    all_carr_info_sql = text(
        'SELECT cid, cNo, dNo, pNum, air, volume, timestamp '
        'FROM carriage_info AS ci '
        'WHERE (ci.cid, ci.cNo, ci.dNo, ci.timestamp) IN ( '
        '    SELECT ci2.cid, ci2.cNo, ci2.dNo, MAX(ci2.timestamp) '
        '    FROM carriage_info AS ci2 '
        '    WHERE ci2.cid = :cid '
        '    GROUP BY ci2.cid, ci2.cNo, ci2.dNo '
        ');'
    )
    all_carr_info_result = db.session.execute(all_carr_info_sql, {'cid': c_id})
    all_carr_info_list = [{'cid': row[0], 'cNo': row[1], 'dNo': row[2], 'pNum': row[3], 'air': row[4], 'volume': row[5],
                           'timestamp': row[6]} for row in all_carr_info_result]

    final_arr['car_info'] = car_list
    final_arr['all_carriage_info'] = all_carr_info_list

    return jsonify(final_arr)


@app.route('/get_arrivedTimeInterval', methods=['GET', 'POST'])
def get_arrived_time_interval():
    with open('../Car_Panel/static/json/arrivedTimeInterval.json') as json_file:  # windows vscode
        # with open('Car_Panel/static/json/arrivedTimeInterval.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


# async def send_access_signal_to_station(access_signal_param):
#     url = 'http://127.0.0.1:5001/access_signal'  # 替换成目标服务器的URL
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, params=access_signal_param) as response:
#             return await response.text()


# 車廂內進站訊號api
# @app.route('/access_signal', methods=['POST'])
# async def access_signal():
#     c_id = request.form.get('c_id')  # 車次
#     route_way = request.form.get('route_way')  # 路線方向
#     leave_station = request.form.get('leave_station')  # 離站數
#     enter_station = request.form.get('enter_station')  # 進站數
#     timestamp = int(datetime.datetime.now().timestamp())
#
#     insert_sql = text(
#         'INSERT INTO `access_signal`(`cid`, `route_way`, `leave_station`, `enter_station`, `timestamp`) '
#         'VALUES (:cid, :route_way, :leave, :enter, :timestamp);')
#
#     db.session.execute(insert_sql, {
#         'cid': c_id,
#         'route_way': route_way,
#         'leave': leave_station,
#         'enter': enter_station,
#         'timestamp': timestamp})
#
#     db.session.commit()
#     access_signal_param = {'cid': c_id, 'route_way': route_way, 'leave_station': leave_station,
#                            'enter_station': enter_station, 'timestamp': timestamp}
#     target_response = await send_access_signal_to_station(access_signal_param)
#     return f'Target Server Response: {target_response}'
#
#
# async def send_carriage_info_to_station(carriage_info_param):
#     url = 'http://127.0.0.1:5001/carriage_info'  # 替换成目标服务器的URL
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, params=carriage_info_param) as response:
#             return await response.text()
#
#
# # 車廂內部資訊api
# @app.route('/carriage_info', methods=['POST'])
# async def carriage_info():
#     c_id = request.args.get('c_id')  # 車次
#     c_no = request.args.get('c_no')  # 車廂號
#     d_no = request.args.get('d_no')  # 車廂號
#     p_num = request.args.get('pNum')  # 壅擠程度
#     air = request.args.get('air')  # 有毒氣體
#     volume = request.args.get('volume')  # 異常聲音
#     timestamp = int(datetime.datetime.now().timestamp())
#
#     insert_sql = text(
#         'INSERT INTO `carriage_info`(`cid`, `cNo`, `dNo`, `pNum`, `air`, `volume`, `timestamp`) '
#         'VALUES (:cid, :cNo, :dNo, :pNum, :air, :volume, :timestamp);')
#
#     db.session.execute(insert_sql, {
#         'cid': c_id,
#         'cNo': c_no,
#         'dNo': d_no,
#         'pNum': p_num,
#         'air': air,
#         'volume': volume,
#         'timestamp': timestamp})
#
#     db.session.commit()
#
#     carriage_info_param = {'cid': c_id, 'c_no': c_no, 'd_no': d_no, 'p_num': p_num, 'air': air, 'volume': volume,
#                            'timestamp': timestamp}
#     target_response = await send_carriage_info_to_station(carriage_info_param)
#     return f'Target Server Response: {target_response}'


# demo_insert insert access signal
@app.route('/demo_insert', methods=['POST'])
def demo_insert():
    c_id = request.json.get('cid')

    # Get Car Info
    car_sql = text(
        'SELECT cid, leave_station, enter_station, route_way '
        'FROM access_signal '
        'WHERE cid=:cid '
        'ORDER BY timestamp '
        'DESC LIMIT 1'
    )

    car_result = db.session.execute(car_sql, {'cid': c_id})
    car_list = [{'cid': row[0], 'leave_station': row[1], 'enter_station': row[2], 'route_way': row[3]} for row in
                car_result]

    # It has been to final station(stop station)
    if car_list[0]['enter_station'] == 2:
        return jsonify({'message': 'Final Station'})

    # Insert access_signal
    pro_sql = text(
        'INSERT INTO `access_signal`(`cid`, `leave_station`, `enter_station`, `route_way`) '
        'VALUES (:cid, :leave, :enter, :route_way);')
    if car_list[0]['leave_station'] == car_list[0]['enter_station']:
        db.session.execute(pro_sql, {
            'cid': c_id, 'leave': car_list[0]['leave_station'] + 1,
            'enter': car_list[0]['enter_station'],
            'route_way': car_list[0]['route_way']})
    elif car_list[0]['leave_station'] != car_list[0]['enter_station']:
        db.session.execute(pro_sql, {
            'cid': c_id, 'leave': car_list[0]['leave_station'],
            'enter': car_list[0]['enter_station'] + 1,
            'route_way': car_list[0]['route_way']})
    db.session.commit()

    return jsonify({'message': 'Insert Success'})


@app.route('/demo_insert_carriage_info', methods=['POST'])
def demo_insert_carriage_info():
    c_id = request.json.get('cid')

    # Insert carriage_info
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
        'cid': c_id,
        'cNo': 1,
        'dNo': 1,
        'pNum': p_num,
        'air': random.random() * 2.5,
        'volume': random.random() * 2.5})

    db.session.commit()

    return jsonify({'message': 'Insert carriage_info successfully'})


if __name__ == '__main__':
    # asyncio.run(run_flask())
    app.debug = True
    app.run(port=5000, host="0.0.0.0")  # 允許外部設備連接
    # app.run(port=5000)
