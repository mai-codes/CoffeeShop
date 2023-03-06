function DrinkView(numRows, drinksPerRow) {
    const DRINKS_PER_PAGE = numRows * drinksPerRow;


    this.updateDrinks = (items) => {
        $('#drinktable').empty();

        const table = $('<div class="drinktable">');
        const columnLabels = $(`
            <div>
                <table class="w3-table">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                    </tr>
        `);
        $('#drinktable').append(columnLabels);

        for(let i = 0; i < 3; i++){
            const drink = items[i];

            const drinkRow = $(`
                <tr>
                <td>${drink.id}</td>
                <td>${drink.name}</td>
                </tr
            `);

            $(table).append(drinkRow);

        }
        $('#drinktable').append(table);

        const closing = $(`</table></div></div>`);
        $('#drinktable').append(closing);
    }

    this.update = (data) => {
        this.updateDrinks(data.items);
    }

    this.load = () => {
        $.get('/api/get_items', {
            n: DRINKS_PER_PAGE,
            offset: 20 //TODO
        }, (data) => {
            this.update(data);
        });
    }
  
}

