var url_string = window.location.href;
var url = new URL(url_string);
var cid = url.searchParams.get("cid");
var dNo = url.searchParams.get("dNo");
var route = url.searchParams.get("route");
var route_way = url.searchParams.get("route_way");


function present_car(data) {

    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');;
    const minutes = now.getMinutes().toString().padStart(2, '0');;
    currTime = document.getElementsByClassName('currTime');
    currTime[0].innerText = `${hours}:${minutes}`;
    return true;
}

function worker() {
    const requestData = {
        'cid': cid,
        'dNo': dNo,
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
            if (data[0]['leave_station'] == (data[0]['enter_station'] + 1)) {
                const redirectUrl = '/SubwayEaseUp/car/car_onmove_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
                window.location.href = redirectUrl;
            }
            present_car(data);
            // setTimeout(worker, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Present Data
function present_station(data) {
    // Add current position mark
    let carriageGroup_1 = document.getElementById('carriageGroup-1')
    let carriageGroup_2 = document.getElementById('carriageGroup-2')
    let carriageGroup_3 = document.getElementById('carriageGroup-3')
    let positionMark = document.createElement('div');
    positionMark.className = "translate-middle position-absolute";
    positionMark.innerHTML = `<div class="position-mark-jump position-relative py-2 px-4 text-bg-primary border border-primary rounded-pill">
    現在位置 <svg width="1em" height="1em" viewBox="0 0 16 16" class="position-absolute top-100 start-50 translate-middle mt-1" fill="var(--bs-primary)" xmlns="http://www.w3.org/2000/svg"><path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/></svg>
  </div>`;
    dNoRem = dNo % 4;
    if (dNoRem == 0) {
        positionMark.classList.add(`positionMark-4`)
    } else {
        positionMark.classList.add(`positionMark-${dNoRem}`)
    }

    if (dNo >= 1 && dNo <= 4) {
        carriageGroup_1.appendChild(positionMark)
    }
    else if (dNo >= 5 && dNo <= 8) {
        carriageGroup_2.appendChild(positionMark)
    }
    else if (dNo >= 9 && dNo <= 12) {
        carriageGroup_3.appendChild(positionMark)
    }


    let facilityGroup_1 = document.getElementById('facilityGroup-1')
    let facilityGroup_2 = document.getElementById('facilityGroup-2')
    let facilityGroup_3 = document.getElementById('facilityGroup-3')
    let facilityGroup_4 = document.getElementById('facilityGroup-4')
    let facilityList = Array(5).fill(null).map(() => Array(9).fill(null));

    data.forEach((item) => {
        let facility = document.createElement('div');
        facility.classList.add('facility-icon');

        //Set innerHTML
        if (item['facility_type'] == 'display_panel') {
            facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/display_panel.svg"
            alt="display-panel">`;

        } else if (item['facility_type'] == 'stairs') {
            if (item['facility_way'] == route_way) {
                facility.innerHTML = `<img
                class="img-fluid"
                src="${baseStaticUrl}images/stairs.svg"
                alt="stairs">`;
            } else {
                facility.innerHTML = `<img
                class="img-fluid svg-reversed"
                src="${baseStaticUrl}images/stairs.svg"
                alt="stairs">`;
            }

        } else if (item['facility_type'] == 'elevator') {
            facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/elevator.svg"
            alt="elevator">`;
        } else if (item['facility_type'] == 'escalator') {
            if (item['facility_way'] == route_way) {
                facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/escalator.svg"
            alt="escalator">`;
            }
            else {
                facility.innerHTML = `<img
            class="img-fluid svg-reversed"
            src="${baseStaticUrl}images/escalator.svg"
            alt="escalator">`;
            }

        }

        //Set class
        let relativePosition = item['relative_position'];
        if (relativePosition >= 0 && relativePosition < 4) {
            const index = 2 * (item.relative_position % 4) + 1;
            if (facilityList[1][index] == null) {
                facilityList[1][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[1][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }

            facilityGroup_1.appendChild(facility);
        }
        else if (relativePosition >= 4 && relativePosition < 8) {
            const index = 2 * (item.relative_position % 4) + 1;
            if (facilityList[2][index] == null) {
                facilityList[2][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[2][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }
            facilityGroup_2.appendChild(facility);
        }
        else if (relativePosition >= 8 && relativePosition < 12) {
            const index = 2 * (item.relative_position % 4) + 1;
            if (facilityList[3][index] == null) {
                facilityList[3][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[3][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }
            facilityGroup_3.appendChild(facility);
        }
        else if (relativePosition == 12) {
            facilityGroup_4.appendChild(facility);
        }
    });

    return true;
}

// Get Station Data
$(document).ready(get_initial_onstation_data);
function get_initial_onstation_data() {
    const requestData = {
        'cid': cid,
        'dNo': dNo,
        'route': route,
        'route_way': route_way
    };
    const requestOptions = {
        method: 'POST', // 或 'GET'，視伺服器端需求而定
        headers: {
            'Content-Type': 'application/json' // 指定資料格式為 JSON
        },
        body: JSON.stringify(requestData) // 將要傳送的資料轉換為 JSON 格式
    };
    fetch('/get_initial_onstation_data', requestOptions) // 使用 fetch API 發送 GET 請求到 /get_data 路由
        // 處理伺服器回傳的響應（response）。這裡使用 then 方法處理 Promise 物件，並將響應的內容轉換為文字格式（使用 response.text() 方法）
        .then(response => response.json())
        .then(data => {
            if (data['car'][0]['leave_station'] == (data['car'][0]['enter_station'] + 1)) {
                const redirectUrl = '/SubwayEaseUp/car/car_onmove_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
                window.location.href = redirectUrl;
            }
            arrived_station_sid = document.getElementsByClassName('arrived_station_sid');
            arrived_station_ch = document.getElementsByClassName('arrived_station_ch');
            arrived_station_en = document.getElementsByClassName('arrived_station_en');
            if (data['station'].length > 0) {
                arrived_station_sid[0].innerText = data['station'][0]['sid'];
                arrived_station_ch[0].innerText = data['station'][0]['sName'];
                arrived_station_en[0].innerText = data['station'][0]['english_name'];
            } else {
                arrived_station_sid[0].innerText = '--';
                arrived_station_ch[0].innerText = '--';
                arrived_station_en[0].innerText = '--';
            }
            present_station(data['station']);
            setTimeout(worker, 5000);
            // setTimeout(demo_insert, 10000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function demo_insert() {
    const requestData = {
        'cid': cid,
        'dNo': dNo,
    };
    const requestOptions = {
        method: 'POST', // 或 'GET'，視伺服器端需求而定
        headers: {
            'Content-Type': 'application/json' // 指定資料格式為 JSON
        },
        body: JSON.stringify(requestData) // 將要傳送的資料轉換為 JSON 格式
    };
    fetch('/demo_insert', requestOptions) // 使用 fetch API 發送 GET 請求到 /get_data 路由
        // 處理伺服器回傳的響應（response）。這裡使用 then 方法處理 Promise 物件，並將響應的內容轉換為文字格式（使用 response.text() 方法）
        .then(response => response.json())
        .then(data => {
            if (data['message'] == 2) {
                console.log("Final Station");
            } else if (data['message'] == 1) {
                console.log("Insert Success");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
