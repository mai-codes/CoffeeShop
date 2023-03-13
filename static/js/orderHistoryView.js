function orderHistoryView() {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateOrderHistory(data);
    }

    this.updateOrderHistory = (items) => {
        $('#pastOrdersList').empty();
        const table = $('<div class="w3-container pastOrdersList"></div>');
        
        for (let i = 0; i < items.length; i++) {
            const item = items[i];

            const itemRow = $(`
            <li class="w3-row">
                <div class="w3-third w3-container">
                    <img class="w3-image drinkImage" src="/static/img/${drink.image}"/>
                </div>
                <div class="w3-third w3-container">
                    <h3>${drink.name}</h3>
                </div>
                <div class="w3-third w3-container">
                    <p>${drink.count}</p>
                    <p>$${drink.price}</p>
                </div>
            </li>
            `);

            $(table).append(itemRow);
        }
        $('#drinktable').append(table);
    }

    this.load = () => {
        $.get('/api/getAllOrders', {}, (data) => {
            this.update(data);
        });
    };
}

