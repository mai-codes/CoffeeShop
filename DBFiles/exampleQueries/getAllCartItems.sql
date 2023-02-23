-- Lists all the items in the cart and their count along with their images as well
-- Same as the getAllOrdersFromUser but just for the cart
-- Not runnable directly but after inserting userID, it works
SELECT CartItem.Count, Item.Name, Item.Image
FROM CartItem
INNER JOIN Item ON Item.ID=CartItem.ItemID
WHERE CartItem.UserID='{INSERT UserID HERE}';