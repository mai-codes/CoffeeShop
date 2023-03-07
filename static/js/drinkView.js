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
        const table = $('<div class="drinktable">');
        const columnLabels = $(`
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 40%">Name</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        `);
        $('#drinktable').append(columnLabels);

        for (let i = 0; i < numDrinks && i < drinks.length; i++) {
            const drink = drinks[i];

            const drinkRow = $(`
                <tr>
                    <td class="tableItem" style="width: 40%">${drink.name}</td>
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
        const closing = $(`</tbody></table></div></div>`);
        $('#drinktable').append(closing);
    }

    this.load = () => {
        $.get('/api/getItems', {}, (data) => {
            this.update(data);
        });
    };
}