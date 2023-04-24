from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
import MySQLdb.cursors # mySQL veritabanına ulaşmak için.
import re
from flask_bootstrap import Bootstrap


# request: Flask uygulamasına gelen HTTP isteklerini işlemek için 
# render_template : HTML sayfalarını görüntülemek için kullanılan bir Flask fonksiyonudur.
# session: Flask uygulaması içinde kullanıcının oturumunu saklamak için kullanılan bir Flask fonksiyonudur.
# url_for: Flask uygulaması içinde sayfa URL'lerini oluşturmak için kullanılan bir Flask fonksiyonudur.


# redirect: Flask uygulaması içinde yönlendirme işlemleri gerçekleştirmek için kullanılan bir Flask fonksiyonudur.
    # @app.route('/dashboard')
    # @login_required   ---->>>> @login_required bir Flask dekoratörüdür ve kullanıcının bir sayfaya erişmeden önce giriş yapması gerektiğini belirtir.
    # def dashboard():
    #     # Kullanıcı oturumu açmışsa, kontrol paneline yönlendir
    #     return render_template('dashboard.html')

    # @app.route('/login')
    # def login():
    #     # Kullanıcıyı oturum açma sayfasına yönlendir
    #     return redirect(url_for('login_page'))


app = Flask(__name__) # __name__, Python'da bulunan özel bir değişkendir ve mevcut modülün adını tutar.
Bootstrap(app)


app.secret_key = 'your secret key' #Flask uygulamasının şifreleme anahtarını belirler. Bu anahtar, kullanıcı oturumlarının güvenliği için kullanılır.


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_login'

#MySQL veritabanına bağlanmak için gerekli olan bağlantı bilgilerini belirler.



mysql = MySQL(app)
#Flask uygulaması ve MySQL bağlantısı arasında bir bağlantı kurar. Bu şekilde uygulama, MySQL veritabanındaki verileri okuyabilir ve yazabilir.

@app.route('/flasklogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Requested methodun POST olup olmadağını kontrol ediyor, ve kullanıcının gönderdiği formda
        #username ve password alanları varsa burdan gelecek değerleri flask içinde username ve password
        #değişkenleri oluşturarak bunlara atıyor.
        
        username = request.form['username']
        password = request.form['password']
         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) : MySQL veritabanı bağlantısı üzerinde bir cursor objesi oluşturulur.
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        #cursor.execute() : veritabanı sorgusu çalıştırılır. Bu durumda, 'SELECT * FROM accounts WHERE username = %s AND password = %s' sorgusu çalıştırılır. %s, sorguda yer tutucu olarak kullanılır ve sonradan tuple ile yer değiştirir. Sorguda yer tutucuların yerine username ve password değişkenleri gelir.
        #(username, password,) : veritabanı sorgusunda yer tutucuların yerine bu değişkenler yerleştirilir.
        
        #Örneğin, cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,)) sorgusu, username ve password değişkenlerinin gerçek değerleriyle yer tutucuları değiştirir ve sonuç olarak SELECT * FROM accounts WHERE username = 'johndoe' AND password = 'password123' gibi bir sorgu oluşur.
        #Burada, %s sembolleri, Python değişkenlerine karşılık gelen username ve password değerleri ile değiştirilir. Yani, sorgu çalıştırılmadan önce, username ve password değerleri, sorgudaki %s sembollerinin yerine geçer.
        #Bu, SQL enjeksiyon saldırılarına karşı koruma sağlar. SQL enjeksiyonu, bir saldırganın kullanıcı tarafından girilen verileri manipüle etmesine ve kötü amaçlı SQL sorguları çalıştırmasına neden olabilir. Ancak, yer tutucular kullanarak, değişkenlerin değeri önceden belirlenir ve kullanıcı tarafından girilen veriler sadece bu değerlerin yerine yerleştirilir. Bu, kötü amaçlı SQL sorgularının çalıştırılmasını önler.

        account = cursor.fetchone()
        #cursor.fetchone() : Veritabanında sorgu sonucu tek bir kayıt döndürülecek şekilde yapılandırılmıştır. Bu nedenle, fetchone() fonksiyonu kullanılır ve sonucu döndürür. Sorgu sonucunda eşleşen kayıt varsa account değişkenine atar. Kayıt bulunmazsa None değerine atanır.
        #belirtilen kullanıcı adı ve şifreyle eşleşen bir hesap varsa, veritabanından bu hesaba ait tüm bilgileri çeker ve bir sözlük olarak account değişkenine atar. Eğer eşleşen bir hesap yoksa, account değişkeni None değerini alır.
        #account değişkeninin değeri, kullanıcının girilen kullanıcı adı ve şifresi ile eşleşen bir hesap varsa, bu hesaba ilişkin bilgileri içeren bir dictionary olacaktır. Bu sözlük, SQL sorgusunda seçilen sütun adlarına göre anahtarlar ve kaydın değerlerine göre ise değerler içerir. Eğer hiçbir hesap eşleşmiyorsa, account değeri None olacaktır.
        # ör: account = {'id': 1, 'username': 'johndoe', 'password': '123456'}


        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            
            return 'Logged in successfully!'
            #Anasayfaya yönlendirir.
        else:
            # 
            msg = 'Incorrect username/password!'


        #MySQL veritabanındaki hesapların kontrolünü yapar. Eğer kullanıcının girdiği kullanıcı adı ve şifre veritabanındaki bir hesapla eşleşiyorsa, kullanıcının oturum bilgilerini kaydeder ve "Logged in successfully!" mesajı ile ana sayfaya yönlendirir. Eğer hesap yoksa veya kullanıcı adı/şifre hatalıysa, "Incorrect username/password!" mesajını verir.    
        #session bir sözlük veri yapısıdır ve kullanıcının giriş yapmış olması durumunda bir dizi anahtar-değer çifti içerir. Bu anahtar-değer çiftleri, bir sonraki HTTP isteği yapıldığında veya uygulama içinde başka bir sayfaya yönlendirildiğinde kullanılabilir.

    return render_template('index.html', msg=msg)

# Bu Flask fonksiyonu, /flasklogin/ URL yoluna GET ve POST isteklerini işler.

# GET isteği, kullanıcının uygulamanın belirli bir URL'sine gitmesini sağlar. Bu durumda /flasklogin/ URL'sine gitmek demektir.

# POST isteği, kullanıcının belirli bir eylem gerçekleştirmesi için sunucuya bilgi göndermesini sağlar. Bu durumda, kullanıcının giriş yapmak için kullanıcı adı ve parola bilgilerini göndermesi amaçlanmaktadır.

# Bu fonksiyon, msg değişkenini ve index.html şablonunu renderlayarak kullanıcıya gösterir. render_template fonksiyonu, Flask uygulamasının /templates klasöründeki HTML dosyalarını renderlamak için kullanılır. Bu durumda, index.html dosyası kullanıcının görüntüleyeceği HTML dosyasıdır ve msg değişkeni bu dosyada kullanılmak üzere aktarılır.    