async function getProducts() {
    return fetch('/antar/get-product/').then((res) => res.json())
}

function addProduct(id_buku) {
    fetch(`/antar/antar-buku-ajax/${id_buku}`, {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(response => {
            if (response.ok) {
                // Redirect setelah produk berhasil ditambahkan
                console.log("redirecting")
                window.location.href = '/antar/show-list-checkout-all/';
            } else {
                // Tangani kesalahan jika permintaan gagal.
                console.error("Gagal menambahkan produk.");
            }
        })
        .catch(error => {
            console.error("Terjadi kesalahan: " + error);
        });

    document.getElementById("form").reset();
    return false;
}
