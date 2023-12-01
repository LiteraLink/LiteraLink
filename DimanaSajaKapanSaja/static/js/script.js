async function getProducts() {
    return fetch('/dimanasajakapansaja/get-station/').then((res) => res.json())
}

async function renderStation() {
    let stations = await getProducts();
    document.getElementById("station-container").innerHTML = ""
    let htmlContent = '';
    let userRole = document.getElementById('userRole').getAttribute('data-role');

    stations.forEach(station => {
        htmlContent += `
            <div class="card-cont">
                <div style="display: flex; justify-content: center; flex-direction: column; width: 50%;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                        <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/>
                    </svg>
                    <div>${station.fields.name}</div>
                </div>
                <div style="width: 30px;"></div>
                <div style="display: flex; justify-content: space-around; flex-direction: column; width: 50%;">
                    Alamat
                    <div>${station.fields.address}</div>
                    <a href="/dimanasajakapansaja/detail/${station.pk}" class="custom-button">Lihat Detail</a>
                </div>
        `;
        if (userRole === 'A') {
        htmlContent += `
            <div style="display: flex; flex-direction: row;">
                <a style="color: #0C6DFD; text-decoration: none;" href="/dimanasajakapansaja/edit_station/${station.pk}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                    </svg>
                </a>
                <div style="width: 10px;"></div>
                <a style="color: #FF0000; text-decoration: none;" href="/dimanasajakapansaja/del_station/${station.pk}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                        <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                    </svg>
                </a>
            </div>
        `;
    }
    htmlContent += `</div>`;
    });

    document.getElementById('station-container').innerHTML = htmlContent;
}

renderStation()

function addStation() {
    fetch("/dimanasajakapansaja/add-station-ajax/", {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(renderStation)

    document.getElementById("form").reset()
    return false
}

document.getElementById("button_add").onclick = addStation