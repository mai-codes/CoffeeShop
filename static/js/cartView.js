document.onload = function() {
    cartLoader = new loadCart();
    cartLoader.load();
};

function loadCart() {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateCart(data);
    }

    this.updateCart = (items) => {
        $('#cartList').empty();
        
        for (let i = 0; i < items.length; i++) {
            const drink = items[i];

            const itemRow = $(`
            <li class="w3-row">
                <div class="w3-third w3-container">
                    <img class="w3-image drinkImage" src="/static/img/${drink.image}">
                </div>
                <div class="w3-third w3-container">
                    <h3>${drink.name}</h3>
                </div>
                <div class="w3-third w3-container">
                    <p>${drink.count}</p>
                    <p>${drink.price}</p>
                </div>
                <span onclick="this.parentElement.style.display='none'" class="w3-button w3-display-right">&times;</span>
            </li>
            `);

            $('#cartList').append(itemRow);
        }
    }

    this.load = () => {
        $.get('/api/getCart', {}, (data) => {
            this.update(data);
        });
    };
}