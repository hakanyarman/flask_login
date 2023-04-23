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
app.config['MYSQL_DB'] = 'pythonlogin'

#MySQL veritabanına bağlanmak için gerekli olan bağlantı bilgilerini belirler.



mysql = MySQL(app)
#Flask uygulaması ve MySQL bağlantısı arasında bir bağlantı kurar. Bu şekilde uygulama, MySQL veritabanındaki verileri okuyabilir ve yazabilir.

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    return render_template('index.html', msg='')

# Bu Flask fonksiyonu, /pythonlogin/ URL yoluna GET ve POST isteklerini işler.

# GET isteği, kullanıcının uygulamanın belirli bir URL'sine gitmesini sağlar. Bu durumda /pythonlogin/ URL'sine gitmek demektir.

# POST isteği, kullanıcının belirli bir eylem gerçekleştirmesi için sunucuya bilgi göndermesini sağlar. Bu durumda, kullanıcının giriş yapmak için kullanıcı adı ve parola bilgilerini göndermesi amaçlanmaktadır.

# Bu fonksiyon, msg değişkenine bir boş dize atar ve index.html şablonunu renderlayarak kullanıcıya gösterir. render_template fonksiyonu, Flask uygulamasının /templates klasöründeki HTML dosyalarını renderlamak için kullanılır. Bu durumda, index.html dosyası kullanıcının görüntüleyeceği HTML dosyasıdır ve msg değişkeni bu dosyada kullanılmak üzere aktarılır.