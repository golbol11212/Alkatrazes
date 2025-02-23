from flask import Flask, render_template, redirect, url_for, session, request
from dbscripts import *
import bcrypt

app = Flask(__name__, template_folder='web/templates', static_folder='web/static' )
app.config["SECRET_KEY"] = "gndpdfzmlvkxnfbklgvloxdnfv.g,xnmcbj"

db = Database("database.db")


def is_authorized():
    return session.get("account_login") is not None


@app.route('/lod_out', methods=['GET', 'POST'])
def lod_out():
    session.clear()
    return redirect(url_for("open"))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', is_authorized=is_authorized())


@app.route('/open', methods=['GET', 'POST'])
def open():
    if request.method == "POST":
        login = request.form["name"]
        password = request.form["password"]

        hashed_password_from_db = db.get_user_data_by_login_self(login)
        if hashed_password_from_db and bcrypt.checkpw(password.encode(), hashed_password_from_db.encode()):
            session["account_login"] = login
            return redirect(url_for("logindex"))

    return render_template("open.html", is_authorized=is_authorized())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        login = request.form["name"]
        password = request.form["password"]
        img = request.files["imges"]
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        

        if not db.check_is_user_exists(login):
            session["account_login"] = login
            
            img.save("web/static/img/" +img.filename) #не сохраняэт !!!!!!!!!!!!!!!! решить            
            db.add_user(login, hashed_password, img.filename)
            
            return redirect(url_for("logindex"))

    return render_template('register.html', is_authorized=is_authorized())




@app.route('/logindex', methods=['GET', 'POST'])
def logindex():
    if not is_authorized():
        return redirect(url_for("open"))
    
    selected_category = None
          
    if request.method == "POST":
        # Обробка вибору категорії
        if 'category' in request.form:
            selected_category = request.form.get("category")
        
        # Обробка кліку на товар
        if 'product-name' in request.form:
            product_name = request.form.get("product-name")
            session['item'] = product_name
            return redirect(url_for("items"))


    
    sell = db.sell()
    login = session.get("account_login", "Гість")
    user_data = db.get_user_data_by_login(login)
    return render_template('logindex.html', 
                         is_authorized=is_authorized(), 
                         sell=sell, 
                         user=user_data, 
                         login=login, 
                         selected_category=selected_category)




@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if not is_authorized():
        return redirect(url_for("open"))
    

    
    login = session.get("account_login", "Гість")
    user_data = db.get_user_data_by_login(login)
    return render_template('profil.html', 
                            is_authorized=is_authorized(), 
                            user=user_data, 
                            login=login)



@app.route('/add_shop', methods=['GET', 'POST'])
def add_shop():
    if not is_authorized():
        return redirect(url_for("open"))
    
    login = session.get("account_login", "Гість")

    if request.method == "POST":

        name= request.form["product-name"]
        inform = request.form["product-description"]
        prise = request.form["product-price"]
        categories = request.form["categories"]
        com = request.form["com"]
        img = request.files["product-image"]
        img.save("web/static/img/"+img.filename)

        
        db.add_shop(login, name, inform, categories, prise, img.filename, com)


    
    user_data = db.get_user_data_by_login(login)
    return render_template('add_shop.html', 
                            is_authorized=is_authorized(),
                            user=user_data,
                            login=login)


@app.route('/items', methods=['GET', 'POST'])
def items():
    if not is_authorized():
        return redirect(url_for("open"))
    
    login = session.get("account_login", "Гість")
    item_name = session.get("item")  # Назва товару з сесії
    
    # Отримуємо список товарів
    all_items = db.sell()
    
    # Шукаємо конкретний товар за назвою
    item = next((post for post in all_items if post[2] == item_name), None)
    
    if not item:
        return redirect(url_for("logindex"))
    
    # Обробка коментарів
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        if comment_text and comment_text.strip():
            # Зберігаємо коментар з назвою товару
            db.add_comment(item_name, login, comment_text.strip())

    
    
    # Отримуємо всі коментарі
    all_comments = db.get_comments()
    
    # Фільтруємо коментарі за назвою товару
    filtered_comments = [c for c in all_comments if c[1] == item_name]
    
    # Дані продавця
    seller_login = item[1]
    seller_data = db.get_user_data_by_login(seller_login)
    
    user_data = db.get_user_data_by_login(login)
    
    return render_template('items.html', 
                         is_authorized=is_authorized(), 
                         item=item,
                         user=user_data, 
                         login=login,
                         seller=seller_data,
                         comen=filtered_comments)
    
if __name__ == "__main__":
    app.run(debug=True)

