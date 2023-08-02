var url_string = window.location.href;
var url = new URL(url_string);
var sid = url.searchParams.get("sid");
var route_order = url.searchParams.get("route_order");
var route_way = url.searchParams.get("route_way");
var arrivedTimeArr = {};

function present_car(data) {

    // Present time
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    currTime = document.getElementsByClassName('currTime');
    currTime[0].innerText = `${hours}:${minutes}`;

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
    let intervalMinute = arrivedTimeArr.timeInterval[data[0]['enter_station']][route_order]; //error
    let remain = Math.ceil((intervalMinute * 60 - nowInterval) / 60);
    if (nowInterval >= 0 && remain >= 0) {
        arrivedTimeContainer.innerText = `${remain}`;
    } else {
        arrivedTimeContainer.innerText = '--';
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
            presentArrivedTime(data['access_signal']);
            present_car(data['car_info']);
            setTimeout(worker, 5000);
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

