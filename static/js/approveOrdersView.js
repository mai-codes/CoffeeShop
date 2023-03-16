document.onload = function() {
    orderLoader = new ApproveView();
    orderLoader.load();
};

function reloadHistory() {
    orderLoader = new ApproveView();
    orderLoader.load();
}


function ApproveView() {
    this.update = (data) => {
        if (!Array.isArray(data)) {
            console.error("Invalid data format, expected an array of drinks");
            return;
        }

        this.updateOrderHistory(data);
    }

    this.updateOrderHistory = (items) => {
        $('#pendingOrdersList').empty();
        const table = $('<div class="w3-container pendingOrdersList"></div>');
        
        //Need a container for the order ID
        //Then a list for the items that belong to that orderID

        var orderDiv = null;
        var knownOrderID = null;
        var knownTotal = 0;

        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            console.log(item);
            if(knownOrderID == null)
            {
                //create new orderDiv
                orderDiv = $('<div class="w3-container w3-left-align"></div>');
                orderDiv.append( $(`<h3>OrderID: ${item.orderID}</h3>`) );
                orderDiv.append( $(`<h3>Date: ${item.orderDate}</h3>`) );
                orderDiv.append( $(`<h3>OrderStatus: ${item.orderStatus}</h3>`) );
                orderDiv.append( $(`<h3 id='price_${item.orderID}'>Total: </h3>`));
                if(item.orderStatus == 'Pending')
                {
                    orderDiv.append( $(`<button class='w3-btn w3-green w3-round'>Approve</button>`));
                    $(orderDiv).find(`button`).on('click', function(e) {
                        $.post('/api/approveOrder', {
                            orderID: item.orderID
                        }, (data) => {
                            console.log(data);
                            reloadHistory();
                        });
                    });
                }
                else if(item.orderStatus == 'Canceled')
                {
                    orderDiv.append( $(`<h4>Reason: ${item.statusMessage}</h4>`))
                }
            }
            else if(item.orderID != knownOrderID)
            {
                //add previous orderDiv to table
                $(orderDiv).find(`#price_${knownOrderID}`).text(`Total: $${knownTotal}`);
                $(table).append(orderDiv);
                knownTotal = 0;
                //create new orderDiv
                orderDiv = $('<br><br><div class="w3-container w3-left-align"></div>');
                orderDiv.append( $(`<h3>OrderID: ${item.orderID}</h3>`) );
                orderDiv.append( $(`<h3>Date: ${item.orderDate}</h3>`) );
                orderDiv.append( $(`<h3>OrderStatus: ${item.orderStatus}</h3>`) );
                orderDiv.append( $(`<h3 id='price_${item.orderID}'>Total: </h3>`));
                if(item.orderStatus == 'Pending')
                {
                    orderDiv.append( $(`<button class='w3-btn w3-green w3-round'>Approve</button>`));
                    $(orderDiv).find(`button`).on('click', function(e) {
                        $.post('/api/approveOrder', {
                            orderID: item.orderID
                        }, (data) => {
                            console.log(data);
                            reloadHistory();
                        });
                    });
                }
                else if(item.orderStatus == 'Canceled')
                {
                    orderDiv.append( $(`<h4>Reason: ${item.statusMessage}</h4>`))
                }
            }

            knownOrderID = item.orderID;
            knownTotal += item.itemPrice;

            const itemRow = $(`
            <li class="w3-row">
                <div class="w3-third w3-container">
                    <img class="w3-image drinkImage" src="./static/img/${item.itemImage}"/>
                </div>
                <div class="w3-third w3-container">
                    <h3>${item.itemName}</h3>
                </div>
                <div class="w3-third w3-container">
                    <p>Amount: ${item.itemCount}</p>
                    <p>Size: ${item.itemSize}</p>
                    <p>Price: $ ${item.itemPrice}</p>
                </div>
            </li>
            `);

            $(orderDiv).append(itemRow);
        }
        
        //add last order to table
        $(orderDiv).find(`#price_${knownOrderID}`).text(`Total: $${knownTotal}`);
        $(table).append(orderDiv);
        knownTotal = 0;

        $('#pendingOrdersList').append(table);
    }

    this.load = () => {
        $.get('/api/getAllOrders', {}, (data) => {
            this.update(data);
        });
    };
}

