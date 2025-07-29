let first = true;
let printQrCode = false;
let cont = 0;
fetch('indicacoes.json')
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('livros-container');

        Object.entries(data).forEach(([idade, livros]) => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'age-group';
            if(first) {
                first = false;
            } else {
                groupDiv.classList.add("page-break");
            }

            let title = "";
            if(idade) {
                title = document.createElement('h2');
                title.textContent = idade;
                groupDiv.appendChild(title);
            }

            const grid = document.createElement('div');
            grid.className = 'book-grid';

            livros.forEach(livro => {
                const bookDiv = document.createElement('div');
                bookDiv.className = 'book';

                const bookTitle = `<a class="nome" href="${livro.url}" target="_blank">${livro.title}</a>`;
                const bookLink = `<div class="link-full"><a class="link truncate-lines" href="${livro.url}" target="_blank">${livro.url}</a></div>`;
                let qrCode = `<img class="qrcode" src="https://api.qrserver.com/v1/create-qr-code/?size=90x90&data=${encodeURIComponent(livro.url)}" alt="QR Code">`;

                if(!printQrCode) {
                    qrCode = "";
                }

                let bookImage = "";
                if (livro.imageUrl) {
                    bookImage = `<div class="bookImage"><img src="${livro.imageUrl}"/></div>`;
                }
                let bookText = `<div>${bookTitle}${bookLink}</div>`
                let bookContainer = `<div class="bookContainer">${bookImage}<div class="bookText">${bookText}</div></div>`

                bookDiv.innerHTML = bookContainer;
                grid.appendChild(bookDiv);
                cont = cont + 1;
            });

            groupDiv.appendChild(grid);
            container.appendChild(groupDiv);
        });
    })
    .then(() => {
        console.log("Total de livros: " + cont);
    })
    .catch(err => {
    document.getElementById('livros-container').innerHTML = `<p>Erro ao carregar o JSON: ${err}</p>`;
    console.error(err);
});
