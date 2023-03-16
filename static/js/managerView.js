function ManagerView(numDrinks) {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("data: ", data)
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
                        <div class="w3-container w3-cell-row">
                            <div class="drink-radio-btn w3-cell">
                                <input class="invisible" type="radio" id="drinkItemSmall_${i}" name="drinkItem_${i}" value="Small" checked>
                                <label class="w3-button" for="drinkItemSmall_${i}">S</label>
                            </div>
                            <div class="drink-radio-btn w3-cell">
                                <input class="invisible" type="radio" id="drinkItemMedium_${i}" name="drinkItem_${i}" value="Medium">
                                <label class="w3-button" for="drinkItemMedium_${i}">M</label>
                            </div>
                            <div class="drink-radio-btn w3-cell">
                                <input class="invisible" type="radio" id="drinkItemLarge_${i}" name="drinkItem_${i}" value="Large">
                                <label class="w3-button" for="drinkItemLarge_${i}">L</label>
                            </div>
                        </div>
                    </div>
                
                    <footer class="w3-container w3-sand">
                        <h5> $ ${drink.smallprice}</h5>
                        <button class="w3-btn delete-button w3-text-red">Delete<i class="w3-margin-left fa fa-trash"></i></button>
                    </footer>
                </div>
            </div>
            `);

            $(drinkRow).find(`#drinkItemSmall_${i}`).on('click', function(e) {
                $(drinkRow).find('h5').text(`$ ${drink.smallprice}`)
            });
            $(drinkRow).find(`#drinkItemMedium_${i}`).on('click', function(e) {
                $(drinkRow).find('h5').text(`$ ${drink.mediumprice}`)
            });
            $(drinkRow).find(`#drinkItemLarge_${i}`).on('click', function(e) {
                $(drinkRow).find('h5').text(`$ ${drink.largeprice}`)
            });

            $(drinkRow).find('.delete-button').on('click', _ => {
                this.delete(drink);
                if (confirm('Are you sure you want to delete this drink?')) {
                    console.log('Thing was deleted from the database.');
                } else {
                    console.log('Thing was not deleted from the database.');
                }
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