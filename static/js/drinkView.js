function DrinkView(numDrinks) {

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
        `);
        $('#drinktable').append(columnLabels);

        

        for(let i = 0; i < numDrinks; i++){
            const drink = drinks[i];

            const drinkRow = $(`
                    <td class="tableItem" style="width: 40%">${Item.name}</td>
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

    this.update = (data) => {
        this.updateDrinks(data.drinks);
    }

    this.load = () => {
        $.get('/api/getItems', {
        }, (data) => {
            this.update(data);
        });
    }
  
}

