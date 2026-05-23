from flask import Flask , render_template ,request, redirect, url_for
import bcrypt
from connection import get_connected_sql
app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('index.html')

#create user
@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        name = request.form['user_name']
        email_id=request.form['email']
        password=request.form['password']
        conn= get_connected_sql()
        cursor = conn.cursor()

        #password hashing
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
        cursor.execute("INSERT INTO USERINFO (user_name, email, password) VALUES (%s, %s, %s)", 
        (name, email_id, hashed)) 

        conn.commit()
        conn.close() 
        return redirect(url_for('user_added', name=name))
    return render_template('signup.html')


@app.route('/user_added') 
def user_added():
    name = request.args.get('name')
    return render_template('user_added.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['user_name']
        password = request.form['password']
        conn = get_connected_sql()
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM USERINFO WHERE user_name = %s", (name,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')): #password hashing
            return redirect(url_for('user_dashboard', name=name))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/user/<name>')
def user_dashboard(name):
    conn = get_connected_sql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERINFO WHERE user_name = %s", (name,))
    row = cursor.fetchone()
    if row:
        user = {
            'user_id': row[0],
            'user_name': row[1],
            'email': row[2]
        }
        cursor.execute("""
            SELECT s.stock_name, s.ticker, h.quantity, h.avg_buy_price
            FROM HOLDINGS h
            JOIN STOCKS s ON h.stock_id = s.stock_id
            WHERE h.user_id = %s
        """, (row[0],))
        holdings = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('user_details.html', user=user, holdings=holdings)
    cursor.close()
    conn.close()
    return "User not found", 404


@app.route('/buy/<name>', methods=['GET', 'POST'])
def buy_stock(name):
    conn = get_connected_sql()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        stock_id = request.form['stock_id']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cursor.execute("SELECT user_id FROM USERINFO WHERE user_name = %s", (name,))
        user = cursor.fetchone()
        #call buy stock procedure 
        cursor.callproc('buy_stock', [user[0], stock_id, quantity, price])
        conn.commit()
        conn.close()
        return redirect(url_for('user_dashboard', name=name))
    
    cursor.execute("SELECT * FROM STOCKS")
    stocks = cursor.fetchall()
    conn.close()
    return render_template('buy.html', stocks=stocks, name=name)


@app.route('/sell/<name>', methods=['GET', 'POST'])
def sell_stock(name):
    conn = get_connected_sql()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        stock_id = request.form['stock_id']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cursor.execute("SELECT user_id FROM USERINFO WHERE user_name = %s", (name,))
        user = cursor.fetchone()
        #call sell stock procedure
        cursor.callproc('sell_stock', [user[0], stock_id, quantity, price])
        conn.commit()
        conn.close()
        return redirect(url_for('user_dashboard', name=name))
    
    cursor.execute("""
        SELECT s.stock_id, s.stock_name, s.ticker 
        FROM HOLDINGS h
        JOIN STOCKS s ON h.stock_id = s.stock_id
        WHERE h.user_id = (SELECT user_id FROM USERINFO WHERE user_name = %s)
    """, (name,))
    stocks = cursor.fetchall()
    conn.close()
    return render_template('sell.html', stocks=stocks, name=name)

@app.route('/watchlist/<name>', methods=['GET', 'POST'])
def watchlist(name):
    conn = get_connected_sql()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM USERINFO WHERE user_name = %s", (name,))
    user = cursor.fetchone()
    user_id = user[0]
    
    if request.method == 'POST':
        stock_id = request.form['stock_id']
        action = request.form['action']

        #procedure to add and remove from watchlist

        if action == 'add':
            cursor.callproc('add_to_watchlist', [user_id, stock_id])
            for result in cursor.stored_results():
                result.fetchall()
        elif action == 'remove':
            cursor.callproc('remove_from_watchlist', [user_id, stock_id])
            for result in cursor.stored_results():
                result.fetchall()
        conn.commit()
    
    cursor.execute("""
    SELECT s.stock_name, s.ticker, w.stock_id,
           p.close_
    FROM WATCHLIST w
    JOIN STOCKS s ON w.stock_id = s.stock_id
    JOIN PRICES p ON s.stock_id = p.stock_id
    WHERE w.user_id = %s
    AND p.date_ = (SELECT MAX(date_) FROM PRICES WHERE stock_id = s.stock_id) """, (user_id,))
    watchlist_data = cursor.fetchall() 

    #get watchlist stocks with close price and join watchlist, stock & price table
     
    cursor.execute("SELECT * FROM STOCKS")
    all_stocks = cursor.fetchall() 
    
    conn.close()
    return render_template('watchlist.html', watchlist=watchlist_data, all_stocks=all_stocks, name=name)


@app.route('/transactions/<name>')
def transactions(name):
    conn = get_connected_sql()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM USERINFO WHERE user_name = %s", (name,))#get userid from username
    user = cursor.fetchone()
    user_id = user[0]
    
    cursor.execute("""
        SELECT s.stock_name, s.ticker, t.quantity, t.price, 
               t.transaction_type, t.transaction_time
        FROM TRANSACTIONS t
        JOIN STOCKS s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        ORDER BY t.transaction_time DESC """, (user_id,))
    transactions = cursor.fetchall() #transaction history 
    
    conn.close()
    return render_template('transactions.html', transactions=transactions, name=name)

@app.route('/dashboard')
def dashboard():
    conn = get_connected_sql()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.stock_name, s.ticker, p.close_, p.date_,
               RANK() OVER (ORDER BY p.close_ DESC) as price_rank,
               AVG(p.close_) OVER (PARTITION BY p.stock_id 
               ORDER BY p.date_ ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg 
        FROM STOCKS s
        JOIN PRICES p ON s.stock_id = p.stock_id
        WHERE p.date_ = (SELECT MAX(date_) FROM PRICES WHERE stock_id = s.stock_id)
    """) #7 day moving average calculation & price and rank from closing price
    stocks = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', stocks=stocks)


if __name__=='__main__':
    app.run(debug=True)

