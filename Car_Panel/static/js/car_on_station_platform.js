const url_string = window.location.href;
const url = new URL(url_string);
const cid = url.searchParams.get("cid");
const dNo = url.searchParams.get("dNo");
let route_way = "";
let route = "";

function present_car(all_carriage_info) {

    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    let hoursContainer = document.getElementById('hoursContainer');
    let minutesContainer = document.getElementById('minutesContainer');
    hoursContainer.innerText = `${hours}`;
    minutesContainer.innerText = `${minutes}`;

    let warningContainer_1 = document.getElementById('warning-container-1');
    warningContainer_1.style.display = "none";
    let warningContainer_2 = document.getElementById('warning-container-2');
    warningContainer_2.style.display = "none";
    let warningContainer_3 = document.getElementById('warning-container-3');
    warningContainer_3.style.display = "none";

    // Show warning
    for (let i = 0; i < all_carriage_info.length; i++) {
        let dNoContainer = document.getElementById(`dNo-${all_carriage_info[i]['dNo']}`);

        // Open carriage warning
        if (all_carriage_info[i]['air'] === 1 || all_carriage_info[i]['volume'] === 1) {
            dNoContainer.style.backgroundColor = "rgba(255, 0, 0, 0.9)";
            if (all_carriage_info[i]['dNo'] >= 1 && all_carriage_info[i]['dNo'] <= 4) {
                warningContainer_1.style.display = "";
            } else if (all_carriage_info[i]['dNo'] >= 5 && all_carriage_info[i]['dNo'] <= 8) {
                warningContainer_2.style.display = "";
            } else {
                warningContainer_3.style.display = "";
            }


        } else {
            dNoContainer.style.backgroundColor = "inherit";

        }
    }

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
            console.log(data['car_info']);
            if (data['car_info'][0]['leave_station'] !== (data['car_info'][0]['enter_station'])) {
                window.location.href = '/SubwayEaseUp/car/car_on_move_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
            }
            present_car(data['all_carriage_info']);
            setTimeout(worker, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Present Data
function present_station(data, exit_data) {
    // Add exit
    const exitGroup_1 = document.getElementById('exitGroup-1');
    const exitGroup_2 = document.getElementById('exitGroup-2');
    exitGroup_1.innerHTML = "";
    exitGroup_2.innerHTML = "";
    exit_data.forEach((item) => {
        let exitBlock = document.createElement('div');
        exitBlock.className = "col-3 d-flex flex-row m-1 border-0";
        exitBlock.style.height = "40%";
        let chineseChars = item['eName'].match(/[\u4e00-\u9fa5]/gu);
        let englishChars = item['eName_en'].match(/[a-zA-Z]/g);
        if (chineseChars.length > 7 || englishChars.length > 24 || item['eName_en'].length > 20) {
            exitBlock.innerHTML = `<div
                                class="exit-icon d-flex justify-content-center align-items-center bg-primary rounded-2 border-0">
                                <p class="h40 text-center">${item['eNo']}</p>
                                </div>
                                <div class="ms-3 d-flex flex-column">
                                    <p class="h20">${item['eName']}</p>
                                    <p class="h15 mt-2">${item['eName_en']}</p>
                                </div>`;
        } else {
            exitBlock.innerHTML = `<div
                                class="exit-icon d-flex justify-content-center align-items-center bg-primary rounded-2 border-0">
                                <p class="h40 text-center">${item['eNo']}</p>
                                </div>
                                <div class="ms-3 d-flex flex-column">
                                    <p class="h25">${item['eName']}</p>
                                    <p class="h20">${item['eName_en']}</p>
                                </div>`;
        }

        if (item['ePosition'] < 3) {
            exitGroup_1.appendChild(exitBlock);
        } else {
            exitGroup_2.appendChild(exitBlock);
        }
    });


    // Add current position mark
    let carriageGroup_1 = document.getElementById('carriageGroup-1');
    let carriageGroup_2 = document.getElementById('carriageGroup-2');
    let carriageGroup_3 = document.getElementById('carriageGroup-3');
    let positionMark = document.createElement('div');
    positionMark.className = "translate-middle position-absolute";
    positionMark.innerHTML = `<div class="position-mark-jump position-relative py-2 px-4 text-bg-primary border border-primary rounded-pill">
    現在位置 <svg width="1em" height="1em" viewBox="0 0 16 16" class="position-absolute top-100 start-50 translate-middle mt-1" fill="var(--bs-primary)" xmlns="http://www.w3.org/2000/svg"><path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/></svg>
  </div>`;
    let dNoRem = dNo % 4;
    if (dNoRem === 0) {
        positionMark.classList.add(`positionMark-4`)
    } else {
        positionMark.classList.add(`positionMark-${dNoRem}`)
    }

    if (dNo >= 1 && dNo <= 4) {
        carriageGroup_1.appendChild(positionMark)
    } else if (dNo >= 5 && dNo <= 8) {
        carriageGroup_2.appendChild(positionMark)
    } else if (dNo >= 9 && dNo <= 12) {
        carriageGroup_3.appendChild(positionMark)
    }

    //Add facility
    let facilityGroup_1 = document.getElementById('facilityGroup-1')
    let facilityGroup_2 = document.getElementById('facilityGroup-2')
    let facilityGroup_3 = document.getElementById('facilityGroup-3')
    let facilityGroup_4 = document.getElementById('facilityGroup-4')
    let facilityList = Array(5).fill(null).map(() => Array(9).fill(null));

    data.forEach((item) => {
        let facility = document.createElement('div');
        facility.classList.add('facility-icon');

        //Set innerHTML
        if (item['facility_type'] === 'display_panel') {
            facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/display_panel.svg"
            alt="display-panel">`;

        } else if (item['facility_type'] === 'stairs') {
            if (item['facility_way'] === route_way) {
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

        } else if (item['facility_type'] === 'elevator') {
            facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/elevator.svg"
            alt="elevator">`;
        } else if (item['facility_type'] === 'escalator') {
            if (item['facility_way'] === route_way) {
                facility.innerHTML = `<img
            class="img-fluid"
            src="${baseStaticUrl}images/escalator.svg"
            alt="escalator">`;
            } else {
                facility.innerHTML = `<img
            class="img-fluid svg-reversed"
            src="${baseStaticUrl}images/escalator.svg"
            alt="escalator">`;
            }

        }

        //Set class
        let relativePosition = item['relative_position'];
        if (relativePosition >= 0 && relativePosition < 4) {
            const index = 2 * Math.floor(relativePosition % 4) + 1;
            if (facilityList[1][index] === null) {
                facilityList[1][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[1][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }

            facilityGroup_1.appendChild(facility);
        } else if (relativePosition >= 4 && relativePosition < 8) {
            const index = 2 * Math.floor(relativePosition % 4) + 1;
            if (facilityList[2][index] === null) {
                facilityList[2][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[2][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }
            facilityGroup_2.appendChild(facility);
        } else if (relativePosition >= 8 && relativePosition < 12) {
            const index = 2 * Math.floor(relativePosition % 4) + 1;
            if (facilityList[3][index] === null) {
                facilityList[3][index] = item['facility_type'];
                facility.classList.add(`facility-${index}`);
            } else {
                facilityList[3][index + 1] = item['facility_type'];
                facility.classList.add(`facility-${index + 1}`);
            }
            facilityGroup_3.appendChild(facility);
        } else if (relativePosition === 12) {
            facilityGroup_4.appendChild(facility);
        }
    });

    return true;
}

// Get Station Data
$(document).ready(get_initial_on_station_data);

function get_initial_on_station_data() {
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
    fetch('/get_initial_on_station_data', requestOptions) // 使用 fetch API 發送 GET 請求到 /get_data 路由
        // 處理伺服器回傳的響應（response）。這裡使用 then 方法處理 Promise 物件，並將響應的內容轉換為文字格式（使用 response.text() 方法）
        .then(response => response.json())
        .then(data => {
            console.log(data);
            route_way = data['route_way'][0];
            route = route_way[0]
            if (data['car'][0]['leave_station'] !== (data['car'][0]['enter_station'])) {
                window.location.href = '/SubwayEaseUp/car/car_on_move_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
            }
            let route_icon_container = document.getElementById('route_icon_container');

            if (data['station'].length > 0) {
                if (route === 'O') {
                    route_icon_container.innerHTML = `<div class="route-icon rounded-3 mx-2"
                    style="background-color: orange;">
                    <p
                        class="h75 text-center ms-2 arrived_station_sid">${data['station'][0]['sid']}</p>
                    <!--sName-->
                </div>
                <div class="col-12 mx-1">
                    <p
                        class="h50 my-2 p-0 text-center arrived_station_ch">${data['station'][0]['sName']}</p>
                    <!--sid-->
                    <p
                        class="my-2 p-0 fs-5 text-center arrived_station_en">${data['station'][0]['english_name']}</p>
                    <!--english_name-->
                </div>`;
                } else if (route === 'R') {
                    route_icon_container.innerHTML = `<div class="route-icon rounded-3 mx-2"
                    style="background-color: red;">
                    <p
                        class="h75 text-center ms-2 arrived_station_sid">${data['station'][0]['sid']}</p>
                    <!--sName-->
                </div>
                <div class="col-12 mx-1">
                    <p
                        class="h50 my-2 p-0 text-center arrived_station_ch">${data['station'][0]['sName']}</p>
                    <!--sid-->
                    <p
                        class="my-2 p-0 fs-5 text-center arrived_station_en">${data['station'][0]['english_name']}</p>
                    <!--english_name-->
                </div>`;
                } else if (route === 'C') {
                    route_icon_container.innerHTML = `<div class="route-icon rounded-3 mx-2"
                    style="background-color: greenyellow;">
                    <p
                        class="h75 text-center ms-2 arrived_station_sid">${data['station'][0]['sid']}</p>
                    <!--sName-->
                </div>
                <div class="col-12 mx-1">
                    <p
                        class="h50 my-2 p-0 text-center arrived_station_ch">${data['station'][0]['sName']}</p>
                    <!--sid-->
                    <p
                        class="my-2 p-0 fs-5 text-center arrived_station_en">${data['station'][0]['english_name']}</p>
                    <!--english_name-->
                </div>`;
                }

            } else {
                route_icon_container.innerHTML = `<div class="route-icon rounded-3 mx-2">
                    <p
                        class="h75 text-center ms-2 arrived_station_sid">--</p>
                    <!--sName-->
                </div>
                <div class="col-12 mx-1">
                    <p
                        class="h50 my-2 p-0 text-center arrived_station_ch">--</p>
                    <!--sid-->
                    <p
                        class="my-2 p-0 fs-5 text-center arrived_station_en">--</p>
                    <!--english_name-->
                </div>`;

            }
            present_station(data['station'], data['station_exit']); // relative_position of facility(0~11)
            worker();
            // setTimeout(worker, 5000);
            // setTimeout(demo_insert, 30000);
            // setTimeout(demo_insert, 10000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Insert Data For Demo or Test(start from get_initial_on_station_data())
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
            console.log(data['message']);

        })
        .catch(error => {
            console.error('Error:', error);
        });
}