var url_string = window.location.href;
var url = new URL(url_string);
var sid = url.searchParams.get("sid");
var route_order = url.searchParams.get("route_order");
var route_way = url.searchParams.get("route_way");
var arrivedTimeArr = {};

function present_car(data) {

    // Present degree of congestion
    carriage_1 = document.getElementById('carriage-1');
    carriage_2 = document.getElementById('carriage-2');
    carriage_3 = document.getElementById('carriage-3');

    carriage_1.innerHTML = '';
    carriage_2.innerHTML = '';
    carriage_3.innerHTML = '';

    data.forEach((data) => { //stationContainer(stationName, routeBlock)
        let perFillContainer = document.createElement('div');
        // perFillContainer.className = "mt-1 d-flex flex-row justify-content-center";
        if (data['pNum'] < 20) {
            perFillContainer.innerHTML = `<img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-green.svg"
            alt="person-fill">`;
        } else if (data['pNum'] >= 20 && data['pNum'] < 40) {
            perFillContainer.innerHTML = `<img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-yellow.svg"
            alt="person-fill">
            <img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-yellow.svg"
            alt="person-fill">`;

        } else if (data['pNum'] >= 40) {
            perFillContainer.innerHTML = `<img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-red.svg"
            alt="person-fill">
            <img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-red.svg"
            alt="person-fill">
            <img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-red.svg"
            alt="person-fill">`;
        }

        if (data.cNo == 1) {
            carriage_1.appendChild(perFillContainer)
        } else if (data.cNo == 2) {
            carriage_2.appendChild(perFillContainer)
        } else if (data.cNo == 3) {
            carriage_3.appendChild(perFillContainer)
        }

    });
    return
}

function presentArrivedTime(data) {
    let arrivedTimeContainer = document.getElementById('arrived-time-interval');

    const now = new Date().getTime();
    const timestamp = new Date(data[0]['timestamp']).getTime() - (8 * 60 * 60 * 1000);;
    let nowInterval = (now - timestamp) / 1000;
    let intervalMinute = null;

    if (data[0]['route_way'] == 'OT1' || data[0]['route_way'] == 'R24' || data[0]['route_way'] == 'C37') {
        intervalMinute = arrivedTimeArr.timeInterval[data[0]['enter_station']][route_order];
    } else {
        // 5=number of station, if the number of station changes, remember to change the number on the line below
        intervalMinute = arrivedTimeArr.timeInterval[5 - 1 - data[0]['enter_station']][5 - 1 - route_order];

    }
    if (data[0]['leave_station'] != data[0]['enter_station']) {
        let remain = Math.ceil((intervalMinute * 60 - nowInterval) / 60);
        if (nowInterval >= 0 && remain >= 0) {
            arrivedTimeContainer.innerText = `${remain}`;
        } else {
            arrivedTimeContainer.innerText = '未發車';
        }
    } else {
        if (data[0]['leave_station'] != route_order) {
            arrivedTimeContainer.innerText = `${intervalMinute}`;
        } else {
            arrivedTimeContainer.innerText = '已到站';
        }

    }


    return
}


function worker() {
    const requestData = {
        // 'sid': sid,
        'route_order': route_order,
        'route_way': route_way
    };
    const requestOptions = {
        method: 'POST', // 或 'GET'，視伺服器端需求而定
        headers: {
            'Content-Type': 'application/json' // 指定資料格式為 JSON
        },
        body: JSON.stringify(requestData) // 將要傳送的資料轉換為 JSON 格式
    };
    fetch('/get_car_data', requestOptions) // 使用 fetch API 發送 GET 請求到 /get_data 路由
        // 處理伺服器回傳的響應（response）。這裡使用 then 方法處理 Promise 物件，並將響應的內容轉換為文字格式（使用 response.text() 方法）
        .then(response => response.json())
        .then(data => {
            // Present time
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            currTime = document.getElementsByClassName('currTime');
            currTime[0].innerText = `${hours}:${minutes}`;
            console.log(data['access_signal']);
            if (data['access_signal'].length == 0 && data['car_info'].length == 0) {
                setTimeout(worker, 5000);
            } else {
                presentArrivedTime(data['access_signal']);
                present_car(data['car_info']);
                setTimeout(worker, 5000);
            }


        })
        .catch(error => {
            console.error('Error:', error);
        });
}


$(document).ready(get_arrivedTimeInterval);
function get_arrivedTimeInterval() {
    fetch('/get_arrivedTimeInterval')
        .then(response => response.json())
        .then(data => {
            // 在這裡使用data，它是解析後的JSON物件
            arrivedTimeArr = data;
            worker();
        })
        .catch(error => {
            // 處理錯誤
            console.error('Error:', error);
        });
}

//get-car-data: access_signal_sql
// SELECT cid, leave_station, enter_station, timestamp, route_way
// FROM (SELECT a1.*
//       FROM access_signal AS a1
//       INNER JOIN (
//           SELECT cid, MAX(timestamp) AS max_timestamp
//           FROM access_signal
//           WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 50 MINUTE)
//           GROUP BY cid )
//      AS a2 ON a1.cid = a2.cid AND a1.timestamp = a2.max_timestamp
//      WHERE route_way = 'OT1' AND leave_station <= 1) AS filtered_data
//      ORDER BY ABS(leave_station - 1), ABS(enter_station - 1) LIMIT 1;