async function getPersons() {
    return fetch('/antar/get-person/').then((res) => res.json())
}

async function refreshPersons() {
  const persons = await getPersons();
  const personCheckout = document.getElementById("personCheckout");
  const role = personCheckout.getAttribute("data-role");
  
  if (persons.length === 0) {
      // Jika persons kosong, tampilkan pesan "Belum ada pengantaran buku"
      const emptyMessage = document.createElement("p");
      emptyMessage.style= "text-align: center;"
      emptyMessage.className= "container"
      emptyMessage.textContent = "";
      personCheckout.appendChild(emptyMessage);
  } else {
      // Jika ada persons, tampilkan daftar pengantaran buku
      persons.forEach(person => {
          console.log(person)
          const card = document.createElement("div");
          card.className = "card";
          card.style="color: #0B7377;"

          if (role === 'A') {
                card.innerHTML = `
                <h5 class="card-header" style="text-align: center;">${person.fields.status_pesanan}</h5>
                <div class="card-body" style="text-align: center;">
                    <h5 class="card-title" style="text-align: center;">${person.fields.nama_lengkap}</h5>
                    <p class="card-text">
                        Memesan buku ${person.fields.nama_buku_dipesan}
                        <div class=container style="margin-bottom: 10px;">
                        Jumlah Buku:
                        </div>
                        <div class=container>
                        <a >
                                <button type="submit" class="btn" style="background-color: #CEDD00;color: #0B7377;" disabled>
                                    -
                                </button>
                            </a>
                        <div style="margin-left: 20px; margin-right: 20px;">
                                ${person.fields.jumlah_buku_dipesan}
                        </div> 
                        <a >
                                <button type="submit" class="btn" style="background-color: #CEDD00;color: #0B7377;" disabled>
                                    +
                                </button>
                            </a>
                        </div>
                        <br>
                        <div class=container>
                            Total Biaya Ongkir = ${person.fields.total_payment}
                        </div>
                    </p>
                    <a href="/antar/show-detail/${person.pk}" >
                            <button class="btn" style="background-color: #CEDD00;color: #0B7377; type="button"> Detail</button>
                        </a>
                    <br>
                    <a>
                            <button class="btn" style="background-color: #CEDD00;color: #0B7377; type="button" disabled> Batalkan Pesanan</button>
                    </a>
                </div>
            `;
          } else {
              card.innerHTML = `
                  <h5 class="card-header" style="text-align: center;">${person.fields.status_pesanan}</h5>
                  <div class="card-body" style="text-align: center;">
                      <h5 class="card-title" style="text-align: center;">${person.fields.nama_lengkap}</h5>
                      <p class="card-text">
                          Memesan buku ${person.fields.nama_buku_dipesan}
                          <div class=container style="margin-bottom: 10px;">
                            Jumlah Buku:
                          </div>
                          <div class=container>
                            <a href="/antar/sub_stock/${person.pk}">
                                    <button type="submit" class="btn" style="background-color: #CEDD00;color: #0B7377;">
                                        -
                                    </button>
                                </a>
                            <div style="margin-left: 20px; margin-right: 20px;">
                                    ${person.fields.jumlah_buku_dipesan}
                            </div> 
                            <a href="/antar/add_stock/${person.pk}">
                                    <button type="submit" class="btn" style="background-color: #CEDD00;color: #0B7377;">
                                        +
                                    </button>
                                </a>
                          </div>
                          <br>
                          <div class=container>
                          Total pembayaran = ${person.fields.total_payment}
                          </div>
                      </p>
                      <a href="/antar/show-detail/${person.pk}" >
                              <button class="btn" style="background-color: #CEDD00;color: #0B7377; type="button"> Detail</button>
                          </a>
                      <br>
                        <a href="/antar/delete-product-ajax/${person.pk}">
                              <button class="btn" style="background-color: #CEDD00;color: #0B7377; type="button"> Batalkan Pesanan</button>
                        </a>
                  </div>
              `;

          }


          personCheckout.appendChild(card);
      });
    }
    
  } // Mengambil nilai 'role' dari template
  refreshPersons()