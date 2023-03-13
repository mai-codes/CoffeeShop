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
                        <button class="w3-btn">Add to Cart </button>
                    </footer>
                </div>
            </div>
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