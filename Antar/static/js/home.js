async function getProducts() {
    return fetch('/antar/get-product/').then((res) => res.json())
}

async function refreshProducts() {
    const books = await getProducts()
    const bookContainer = document.getElementById("bookContainer");
    const role = bookContainer.getAttribute("data-role");
    console.log(role)

    books.forEach(book => {
        const card = document.createElement("div");
        card.className = "card";
        card.style = "width: 250px; height: 400px;color: #0B7377;";

        if (role === 'A') {
            card.innerHTML = `
                <div style="text-align: center;">
                    <img class="card-img-top" src="${book.fields.thumbnail}" alt="Card image cap" style="max-width: 150px; max-height: 200px; border-radius: 0; margin-top: 15px;">
                </div>
                <div class="card-body">
                    <div>
                        <h5 class="card-title" style="font-size: 15px; text-align: center; font-weight: 700;">${book.fields.title}</h5>
                        <p class="card-text" style="font-size: 15px; text-align: center;">Author: ${book.fields.display_authors}</p>
                    </div>
                    <div class="container">
                        <a>
                            <button class="btn custom-bg" type="button" disabled> Antar Buku Ini</button>
                        </a>
                        
                    </div>
                </div>
            `;
        } else {
            card.innerHTML = `
                <div style="text-align: center;">
                    <img class="card-img-top" src="${book.fields.thumbnail}" alt="Card image cap" style="max-width: 150px; max-height: 200px; border-radius: 0; margin-top: 15px;">
                </div>
                <div class="card-body">
                    <div>
                        <h5 class="card-title" style="font-size: 15px; text-align: center; font-weight: 700;">${book.fields.title}</h5>
                        <p class="card-text" style="font-size: 15px; text-align: center;">Author: ${book.fields.display_authors}</p>
                    </div>
                    <div class="container">
                        <a href="/antar/pemesanan-buku/${book.pk}">
                            <button class="btn" style="background-color: #CEDD00;color: #0B7377;" type="button"> Antar Buku Ini</button>
                        </a>     
                    </div>
                </div>
            `;
        }
        bookContainer.appendChild(card);
    });
}

refreshProducts()