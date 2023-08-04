var url_string = window.location.href;
var url = new URL(url_string);
var cid = url.searchParams.get("cid");
var dNo = url.searchParams.get("dNo");
var route = url.searchParams.get("route");
var route_way = url.searchParams.get("route_way");

const stationBlockWidth = 60;
const arrowContainerWidth = 50;
const stationNameWidth = 90;
const arrivedTimeBlockWidth = 90;
var arrowPositionArr = []; //Record arrow position for the animation
var arrivedTimeArr = {};

//Start arrow animation, opacity change(start from present_car())
function startAnimation(arrowGroupCount) {
    const arrowLeftGroupElement = document.getElementById(`arrow-left-group-${arrowGroupCount}`);
    const arrowRightGroupElement = document.getElementById(`arrow-right-group-${arrowGroupCount}`);

    if (arrowLeftGroupElement && arrowRightGroupElement) {
        arrowLeftGroupElement.style.setProperty('--initial-translateX', `${arrowPositionArr[arrowGroupCount][0]}px`);
        arrowLeftGroupElement.style.setProperty('--initial-move-distance', `${arrowPositionArr[arrowGroupCount][2]}px`);
        arrowLeftGroupElement.classList.add('flashing-icon');
        arrowRightGroupElement.style.setProperty('--initial-translateX', `${arrowPositionArr[arrowGroupCount][1]}px`);
        arrowRightGroupElement.style.setProperty('--initial-move-distance', `${arrowPositionArr[arrowGroupCount][2]}px`);
        arrowRightGroupElement.classList.add('flashing-icon');
    }

    if ((arrowGroupCount - 1) >= 0) {
        for (let i = 0; i <= arrowGroupCount; i++) {
            const subwayMapStationName = document.getElementById(`subway-map-station-name-${i}`);
            const subwayMapBlock = document.getElementById(`subway-map-block-${i}`);
            const arrivedTimeBlock = document.getElementById(`arrivedTime-block-${i}`);
            subwayMapStationName.style.opacity = 0.5;
            subwayMapBlock.style.opacity = 0.5;
            arrivedTimeBlock.style.opacity = 0.5;
            const prevArrowLeftGroupElement = document.getElementById(`arrow-left-group-${i}`);
            const prevArrowRightGroupElement = document.getElementById(`arrow-right-group-${i}`);
            prevArrowLeftGroupElement.style.opacity = 0.5;
            prevArrowRightGroupElement.style.opacity = 0.5;
        }
        const prevArrowLeftGroupElement = document.getElementById(`arrow-left-group-${arrowGroupCount - 1}`);
        const prevArrowRightGroupElement = document.getElementById(`arrow-right-group-${arrowGroupCount - 1}`);
        if (prevArrowLeftGroupElement && prevArrowRightGroupElement) {
            prevArrowLeftGroupElement.classList.remove('flashing-icon');
            prevArrowRightGroupElement.classList.remove('flashing-icon');

        }
    } else {
        let subwayMapStationName = document.getElementById(`subway-map-station-name-0`);
        let subwayMapBlock = document.getElementById(`subway-map-block-0`);
        let arrivedTimeBlock = document.getElementById(`arrivedTime-block-0`);
        subwayMapStationName.style.opacity = 0.5;
        subwayMapBlock.style.opacity = 0.5;
        arrivedTimeBlock.style.opacity = 0.5;
    }
}

// Present state in car and make sure whether entering thenstation(start from worker())
function present_car(data) {
    if (data[0]['leave_station'] != (data[0]['enter_station'])) {
        startAnimation(data[0]['enter_station']);
    } else if (data[0]['leave_station'] == (data[0]['enter_station'])) {
        const redirectUrl = '/SubwayEaseUp/car/car_onstation_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
        window.location.href = redirectUrl;
    }
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    currTime = document.getElementsByClassName('currTime');
    currTime[0].innerText = `${hours}:${minutes}`;

    degree_of_congestion = document.getElementById('degree-of-congestion');
    air_quality = document.getElementById('air-quality');
    volumn = document.getElementById('volumn');
    degree_of_congestion.innerText = data[0]['pNum'];
    air_quality.innerText = data[0]['air'];
    volumn.innerText = data[0]['volumn'];

}

// Present arrived time block(start from worker())
function present_arrivedTime(data) {

    const now = new Date().getTime();
    const timestamp = new Date(data[0]['timestamp']).getTime() - (8 * 60 * 60 * 1000);;
    let nowInterval = (now - timestamp) / 1000;
    if (data[0]['route_way'] == 'OT1' || data[0]['route_way'] == 'R24' || data[0]['route_way'] == 'C37') {
        for (let i = data[0]['leave_station']; i < stationNum; i++) {
            const arrivedTimeBlockText = document.querySelectorAll(`#arrivedTime-block-${i} p`);
            let intervalMinute = arrivedTimeArr.timeInterval[data[0]['enter_station']][i];
            let remain = Math.ceil((intervalMinute * 60 - nowInterval) / 60);

            if (nowInterval >= 0 && remain >= 0) {
                arrivedTimeBlockText[0].innerText = `${remain}`;
            }
        }
    } else {
        for (let i = data[0]['leave_station']; i < stationNum; i++) {
            const arrivedTimeBlockText = document.querySelectorAll(`#arrivedTime-block-${i} p`);
            let remain = Math.ceil((intervalMinute * 60 - nowInterval) / 60);
            if (nowInterval >= 0 && remain >= 0) {
                arrivedTimeBlockText[0].innerText = `${remain}`;
            }
        }
    }


    return
}

//Update Data every 5 seconds(start from get_arrivedTimeInterval())
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

            present_car(data);
            present_arrivedTime(data);
            setTimeout(worker, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

var stationNum = 0;
// Present Station Data(sid block, sName block, arrived time, arrow)(start from get_station())
function present_station(data) { //data['station']
    // Calculate position of station name 
    const stationNameContainer = document.getElementById('stationNameContainer');
    const totalstationNameWidth = stationNameWidth + 2 * 10; // 假設每個區塊寬度是 100px，左右邊距各為 10px
    stationNum = data.length;
    const totalstationNameSpacing = (stationNameContainer.clientWidth - 30) - (totalstationNameWidth * (stationNum - 1) + stationNameWidth + 2 * 10);
    const stationNamespacing = totalstationNameSpacing / (stationNum - 1);

    // Calculate position of sid block 
    const subwayMap = document.getElementById('subway-map');
    // 計算區塊間的等間距間距（包括區塊本身的寬度和邊距）
    const totalBlockWidth = stationBlockWidth + 2 * 10 + arrowContainerWidth * 2; // 假設每個區塊寬度是 100px，左右邊距各為 10px
    const totalSpacing = (subwayMap.clientWidth - 60) - (totalBlockWidth * (stationNum - 1) + stationBlockWidth + 2 * 10); //50是左右padding
    // 計算每個區塊之間的間距
    const spacing = totalSpacing / (stationNum - 1);

    // Calculate position of station name 
    const arrivedTimeContainer = document.getElementById('arrivedTimeContainer');
    const totalArrivedTimeWidth = arrivedTimeBlockWidth + 2 * 10; // 假設每個區塊寬度是 100px，左右邊距各為 10px
    const totalArrivedTimeSpacing = (arrivedTimeContainer.clientWidth - 30) - (totalArrivedTimeWidth * (stationNum - 1) + arrivedTimeBlockWidth + 2 * 10);
    const arrivedTimeSpacing = totalArrivedTimeSpacing / (stationNum - 1);

    var arrowGroupCount = 0;

    // 在<div id="subway-map">裡動態生成區塊並呈現
    data.forEach((data, index) => { //stationContainer(stationName, routeBlock)
        //station name
        const stationName = document.createElement('div');
        stationName.classList.add('subway-map-station-name');
        stationName.setAttribute('id', `subway-map-station-name-${index}`);
        stationName.style.width = `${stationNameWidth}px`;
        stationName.innerHTML = `<p class="h30 text-center">${data.sName}</p>`;
        const stationNametranslateX = index * (stationNamespacing);
        stationName.style.transform = `translateX(${stationNametranslateX}px)`;
        stationNameContainer.appendChild(stationName);

        //Station Block
        const block = document.createElement('div');
        block.classList.add('subway-map-block');
        block.setAttribute('id', `subway-map-block-${index}`);
        block.innerHTML = `<p class="h30 text-center">${data.sid}</p>`;
        block.style.width = `${stationBlockWidth}px`;
        if (route == "O") {
            block.style.borderColor = 'orange';
        } else if (route == "R") {
            block.style.borderColor = 'red';
        } else {
            block.style.borderColor = 'greenyellow';
        }
        // 設定區塊的位置，使用 transform 屬性平移區塊
        const translateX = index * spacing; //totalBlockWidth + spacing
        // transform: css屬性，對元素進行平移、縮放、旋轉和斜切等
        // translateX: 對元素進行水平方向上的平移（移動），
        //      元素的起始位置是元素自身的原始位置，也就是未應用任何平移之前的位置
        block.style.transform = `translateX(${translateX}px)`;
        // Add block to the map
        subwayMap.appendChild(block);

        //Arrived Time
        const arrivedTime = document.createElement('div');
        arrivedTime.classList.add('arrivedTime-block');
        arrivedTime.setAttribute('id', `arrivedTime-block-${index}`);
        arrivedTime.style.width = `${arrivedTimeBlockWidth}px`;
        arrivedTime.innerHTML = `<p class="h30 text-center">已到達</p>`;
        const arrivedTimeTranslateX = index * (arrivedTimeSpacing);
        arrivedTime.style.transform = `translateX(${arrivedTimeTranslateX}px)`;
        arrivedTimeContainer.appendChild(arrivedTime);

        //Arrow
        if (arrowGroupCount < stationNum - 1) {
            arrow = document.createElement('i')
            arrow.setAttribute('id', `arrow-left-group-${arrowGroupCount}`);
            arrow.classList.add(`arrow-group`);
            arrow.classList.add(`bi`);
            arrow.classList.add(`bi-caret-right`);
            // arrowContainer.innerHTML = `<i class="bi bi-caret-right"></i>
            // <i class="bi bi-caret-right-fill"></i>`;
            arrow.style.width = `${arrowContainerWidth}px`;
            const arrowTranslateX = (index + 0.5) * (spacing) + arrowContainerWidth / 2;
            arrowPositionArr.push([]);
            arrowPositionArr[index][0] = arrowTranslateX - spacing / 4;
            arrow.style.transform = `translateX(${arrowTranslateX}px)`;
            subwayMap.appendChild(arrow);
            arrowFill = document.createElement('i')
            arrowFill.setAttribute('id', `arrow-right-group-${arrowGroupCount}`);
            arrowFill.classList.add(`arrow-group`);
            arrowFill.classList.add(`bi`);
            arrowFill.classList.add(`bi-caret-right-fill`);
            // arrowContainer.innerHTML = `<i class="bi bi-caret-right"></i>
            // <i class="bi bi-caret-right-fill"></i>`;
            arrowFill.style.width = `${arrowContainerWidth}px`;
            const arrowFillTranslateX = (index + 0.5) * (spacing) + arrowContainerWidth / 2;
            arrowPositionArr[index][1] = arrowFillTranslateX - spacing / 4;
            arrowPositionArr[index][2] = spacing / 2;
            arrowFill.style.transform = `translateX(${arrowFillTranslateX}px)`;
            subwayMap.appendChild(arrowFill);
            arrowGroupCount++;

        }
    });

    return true;
}

//Get arrivedTimeInterval.json(start from get_station())
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
// Get Station Data
$(document).ready(get_station);
function get_station() {
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
    fetch('/get_station_data', requestOptions) // 使用 fetch API 發送 GET 請求到 /get_data 路由
        // 處理伺服器回傳的響應（response）。這裡使用 then 方法處理 Promise 物件，並將響應的內容轉換為文字格式（使用 response.text() 方法）
        .then(response => response.json())
        .then(data => {
            if (data['car'][0]['leave_station'] == data['station'][0]['enter_station']) {
                const redirectUrl = '/SubwayEaseUp/car/car_onstation_platform?cid=' + cid + '&dNo=' + dNo + '&route=' + route + '&route_way=' + route_way;
                window.location.href = redirectUrl;
            }
            final_sation_ch = document.getElementById('final_sation_ch');
            final_sation_en = document.getElementById('final_sation_en');
            if (data['station'].length > 0) {
                final_sation_ch.innerText = data['station'][data['station'].length - 1]['sName'];
                final_sation_en.innerText = data['station'][data['station'].length - 1]['english_name'];
            } else {
                final_sation_ch.innerText = '---';
                final_sation_en.innerText = '---';
            }
            present_station(data['station']);
            get_arrivedTimeInterval();

            // Insert Data For Demo or Test
            // setTimeout(demo_insert, 120000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Insert Data For Demo or Test(start from get_station())
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

