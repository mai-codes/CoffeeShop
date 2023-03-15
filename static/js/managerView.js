function ManagerView(numDrinks) {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateDrinks(data);
    }

    this.updateDrinks = (drinks) => {
        $('#drinktable').empty();
        const table = $('<div class="w3-container drinkCards"></div>');

        for (let i = 0; i < numDrinks && i < drinks.length; i++) {
            const drink = drinks[i];

            const drinkRow = $(`
            <div class="card-column">
                <div class="w3-card-2">
                    <header class="w3-container w3-sand">
                        <h3>${drink.name}</h3>
                    </header>
                    <div class="w3-container">
                        <img class="w3-image drinkImage" src="/static/img/${drink.image}">
                        <button class="w3-btn">S</button>
                        <button class="w3-btn">M</button>
                        <button class="w3-btn">L</button>
                    </div>
                
                    <footer class="w3-container w3-sand">
                        <h5>${drink.price}</h5>
                        <button class="w3-btn delete-button">Delete</button>
                    </footer>
                </div>
            </div>
            `);

            $(drinkRow).find('.delete-button').on('click', _ => {
                this.delete(drink);
            });

            $(table).append(drinkRow);
        }

        $('#drinktable').append(table);
        const closing = $(`</table></div>`);
        $('#drinktable').append(closing);
    }

    this.delete = (drink) => {
        $.post('/api/deleteItem', {
            id: drink.id
        }, (data) => {
            this.update(data);
            this.load();
        });
    }

    this.load = () => {
        $.get('/api/getItems', {}, (data) => {
            this.update(data);
        });
    }
}