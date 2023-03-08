function DrinkView(numDrinks) {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateDrinks(data);
    }

    this.updateDrinks = (drinks) => {
        $('#drinktable').empty();
        const table = $('<div class="drinkTable w3-responsive">');
        const columnLabels = $(`
                <table class="w3-table">
                    <tr>
                        <th>Name</th>
                        <th>Image</th>
                        <th>Price</th>
                    </tr>
        `);
        $('#drinktable').append(columnLabels);

        for (let i = 0; i < numDrinks && i < drinks.length; i++) {
            const drink = drinks[i];

            const drinkRow = $(`
                <tr>
                    <td>${drink.name}</td>
                    <td><img class="w3-image drinkImage" src="/static/img/${drink.image}"></td>
                    <td>${drink.price}</td>
                </tr>
            `);

            $(drinkRow).find('.dec-button').on('click', _ => {
                this.decrement(drink);
            });
            $(drinkRow).find('.inc-button').on('click', _ => {
                this.increment(drink);
            });

            $(table).append(drinkRow);
        }

        $('#drinktable').append(table);
        const closing = $(`</table></div>`);
        $('#drinktable').append(closing);
    }

    this.load = () => {
        $.get('/api/getItems', {}, (data) => {
            this.update(data);
        });
    };
}