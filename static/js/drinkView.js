function updateCart(){
    $.get('/api/getCart', {
    }, (data) => {
        let totalCount = 0;
        for (let itemCount in data){
            totalCount = totalCount + 1;
        }
        console.log(totalCount);
        $('#cart').text(`View Cart (${totalCount})`);
    });

}

function DrinkView(numDrinks) {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateDrinks(data);
    }

    this.loadCart = (data) => {
        let totalCount = 0;
        for (let itemCount in data){
            totalCount = totalCount + 1;
        }
        console.log(totalCount);
        $('#cart').text(`View Cart (${totalCount})`);
    }

    this.updateDrinks = (drinks) => {
        $('#drinktable').empty();
        const table = $('<div class="w3-container drinkCards"></div>');

        const popUp = $(`<script>
        // When the user clicks on div, open the popup
        function myFunction() {
          var popup = document.getElementById("myPopup");
          popup.classList.toggle("show");
          setTimeout(function(){
            popup.classList.toggle("show");
            }, 2000);
            }
        </script>`)

        $('#drinktable').append(popUp);

        const itemAddedMessage = $(`<div class="popup"><span class="popuptext" id="myPopup">Item Added</span></div>`)

        $('#drinktable').append(itemAddedMessage);

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
                        <h5>$ ${drink.smallprice}</h5>
                        <button class="popup w3-button" id="addToCart" onclick="myFunction()">Add to Cart
                        </button>
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

            $(drinkRow).find('button').on('click', function(e) {
                console.log("click");
                var sizeName = $(drinkRow).find(`input[name="drinkItem_${i}"]:checked`).val();
                
                $.post('/api/addToCart', {
                    itemID: drink.id,
                    size: sizeName,
                    count: 1
                }, (data) => {
                    //probably should do something. Just print the json or something
                    console.log(data);
                    localStorage.setItem("message","Sucessfully added");
                    updateCart();
                });
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
        $.get('/api/getCart', {
        }, (data) => {
            this.loadCart(data);
        });
    };
}