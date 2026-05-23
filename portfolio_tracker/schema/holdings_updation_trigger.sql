DELIMITER $$
CREATE TRIGGER update_holdings_on_transaction
AFTER INSERT ON TRANSACTIONS
FOR EACH ROW

BEGIN 
-- BUY PART
	IF NEW.transaction_type ='Buy' THEN 
		IF EXISTS (SELECT 1 FROM HOLDINGS
		WHERE user_id =NEW.user_id 
        AND stock_id =NEW.stock_id) THEN  -- ALREADY OWNS STOCK
	
	UPDATE HOLDINGS -- OWNS ALREADY
	SET quantity = quantity + NEW.quantity, 
		avg_buy_price = (quantity * avg_buy_price + NEW.quantity * NEW.price) / (quantity + NEW.quantity)
	WHERE user_id = NEW.user_id 
	AND stock_id = NEW.stock_id;
    
    ELSE -- DOESNT OWN ANYTHING YET

    INSERT INTO HOLDINGS (user_id, stock_id, quantity, avg_buy_price)
    VALUES (NEW.user_id, NEW.stock_id, NEW.quantity, NEW.price);
  END IF; 
  
   ELSE -- SELL PART
	UPDATE HOLDINGS 
        SET quantity = quantity - NEW.quantity
        WHERE user_id = NEW.user_id 
        AND stock_id = NEW.stock_id;
        -- IF QUANTITY = 0, THEN DELETE ROW
        DELETE FROM HOLDINGS
        WHERE user_id = NEW.user_id 
        AND stock_id = NEW.stock_id
        AND quantity = 0;
    END IF;
   


END $$


DELIMITER ; 