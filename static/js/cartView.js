document.onload = function() {
    cartLoader = new loadCart();
    cartLoader.load();
};

function checkout() {
    //add an alert or something to avoid cases where the user misclicks and ensures that the user knows that they actually ordered something.
    $.post('/api/createOrder', {}, (data) => {
        reloadCart();
    });
}

function reloadCart() {
    cartLoader = new loadCart();
    cartLoader.load();
}

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
        var totalPrice = 0.00;
        
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            console.log(item);

            const itemRow = $(`
            <li class="w3-row">
                <div class="w3-third w3-container">
                    <img class="w3-image drinkImage" src="./static/img/${item.itemImage}"/>
                </div>
                <div class="w3-third w3-container">
                    <h3>${item.itemName}</h3>
                </div>
                <div class="w3-third w3-container">
                <button class="w3-btn w3-red w3-round w3-right">&times;</button>
                    <p>Amount: ${item.itemCount}</p>
                    <p>Size: ${item.itemSize}</p>
                    <p>Price: $ ${item.itemPrice}</p>
                </div>
            </li>
            `);

            totalPrice += item.itemPrice;

            //Note that this is the only button in the item row so it is okay
            $(itemRow).find('button').on('click', function(e) {
                $.post('/api/removeFromCart', {
                    cartItemID: item.id
                }, (data) => {
                    reloadCart()
                });
            });

            $('#cartList').append(itemRow);
        }

        $('#cart-total-id').text(`Total: $${totalPrice}`);
    }

    this.load = () => {
        $.get('/api/getCart', {}, (data) => {
            this.update(data);
        });
    };
}