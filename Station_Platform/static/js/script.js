const url_string = window.location.href;
const url = new URL(url_string);
const sid = url.searchParams.get("sid");
const route_order = url.searchParams.get("route_order");
const route_way = url.searchParams.get("route_way");
let arrivedTimeArr = {};

function present_car(data) {

    // Present degree of congestion
    let carriage_1 = document.getElementById('carriage-1');
    let carriage_2 = document.getElementById('carriage-2');
    let carriage_3 = document.getElementById('carriage-3');

    carriage_1.innerHTML = '';
    carriage_2.innerHTML = '';
    carriage_3.innerHTML = '';

    data.forEach((data) => { //stationContainer(stationName, routeBlock)
        let perFillContainer = document.createElement('div');
        // perFillContainer.className = "mt-1 d-flex flex-row justify-content-center";
        if (data['pNum'] === "不壅擠") {
            perFillContainer.innerHTML = `<img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-green.svg"
            alt="person-fill">`;
        } else if (data['pNum'] === "尚可") {
            perFillContainer.innerHTML = `<img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-yellow.svg"
            alt="person-fill">
            <img
            class="img-fluid person-fill"
            src="${baseStaticUrl}images/person-yellow.svg"
            alt="person-fill">`;

        } else if (data['pNum'] === "壅擠") {
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

        if (data["cNo"] === 1) {
            carriage_1.appendChild(perFillContainer)
        } else if (data["cNo"] === 2) {
            carriage_2.appendChild(perFillContainer)
        } else if (data["cNo"] === 3) {
            carriage_3.appendChild(perFillContainer)
        }

    });
}

function presentArrivedTime(data) {
    let arrivedTimeContainer = document.getElementById('arrived-time-interval');

    const now = new Date().getTime();
    const timestamp = new Date(data[0]['timestamp']).getTime() - (8 * 60 * 60 * 1000);
    let nowInterval = (now - timestamp) / 1000;
    let intervalMinute;

    if (data[0]['route_way'] === 'OT1' || data[0]['route_way'] === 'R24' || data[0]['route_way'] === 'C37') {
        intervalMinute = arrivedTimeArr.timeInterval[data[0]['enter_station']][route_order];
    } else {
        // 5=number of station, if the number of station changes, remember to change the number on the line below
        intervalMinute = arrivedTimeArr.timeInterval[5 - 1 - data[0]['enter_station']][5 - 1 - route_order];

    }
    if (data[0]['leave_station'] !== data[0]['enter_station']) {
        let remain = Math.ceil((intervalMinute * 60 - nowInterval) / 60);
        if (nowInterval >= 0 && remain >= 0) {
            arrivedTimeContainer.innerText = `${remain}`;
        } else {
            arrivedTimeContainer.innerText = '未發車';
        }
    } else {
        if (data[0]['leave_station'] !== route_order) {
            arrivedTimeContainer.innerText = `${intervalMinute}`;
        } else {
            arrivedTimeContainer.innerText = '已到站';
        }

    }
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
            let hoursContainer = document.getElementById('hoursContainer');
            let minutesContainer = document.getElementById('minutesContainer');
            hoursContainer.innerText = `${hours}`;
            minutesContainer.innerText = `${minutes}`;

            console.log(data['access_signal']);
            if (data['access_signal'].length === 0 && data['car_info'].length === 0) {
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
    fetch('/get_arrived_time_interval')
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
