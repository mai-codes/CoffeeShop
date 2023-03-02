-- Lists all the items in the order and their count along with their images as well
-- Not runnable directly but after inserting userID, it works
SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, Item.Price, Item.Image
FROM OrderInfo
INNER JOIN OrderItem ON OrderInfo.ID=OrderItem.OrderID
INNER JOIN Item ON Item.ID=OrderItem.ItemID
WHERE OrderInfo.UserID='{INSERT UserID HERE}';