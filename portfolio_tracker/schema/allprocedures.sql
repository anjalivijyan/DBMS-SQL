
DELIMITER $$
CREATE PROCEDURE buy_stock(
IN param_user_id INT,
IN param_stock_id INT,
IN param_quantity INT,
IN param_price DECIMAL (15,4) 
)
BEGIN
INSERT INTO TRANSACTIONS (user_id,stock_id,quantity,price,transaction_type)
VALUES (param_user_id,param_stock_id,param_quantity,param_price,'Buy');

END $$

CREATE PROCEDURE sell_stock(
IN param_user_id INT,
IN param_stock_id INT,
IN param_quantity INT,
IN param_price DECIMAL (15,4) 
)
BEGIN
INSERT INTO TRANSACTIONS (user_id,stock_id,quantity,price,transaction_type)
VALUES (param_user_id,param_stock_id,param_quantity,param_price,'Sell');


END $$

CREATE PROCEDURE add_to_watchlist(
IN param_user_id INT,
IN param_stock_id INT
)

BEGIN
INSERT INTO WATCHLIST (user_id,stock_id)
VALUES(param_user_id,param_stock_id);


END $$
CREATE PROCEDURE remove_from_watchlist(
IN param_user_id INT,
IN param_stock_id INT
)

BEGIN
DELETE FROM  WATCHLIST
WHERE user_id = param_user_id
AND stock_id = param_stock_id;


END $$

DELIMITER ; 


