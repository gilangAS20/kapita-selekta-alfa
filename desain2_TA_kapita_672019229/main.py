from flask import Flask, render_template, request, session, redirect, url_for,json
from connectdb import Database
app = Flask(__name__)
app.secret_key = 'ini rahasia!'

@app.route("/login",methods=['GET', 'POST'])
def login():
    message = ""
    type = ""

    if 'username' in session.keys():
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = Database('ksb-2022')

        user = request.form['formUsername']
        passw = request.form['formPassword']
        status, data = conn.select("SELECT * FROM admin_672019229 WHERE username = '{}' AND password = '{}'".format(user, passw))
        if status:
            session['username'] = user
            return redirect(url_for('index'))

        else:
            message = "username atau password salah"
            type = "error"
            return render_template('login.html', message=message, type=type)

    return render_template('login.html', message=message, type=type)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    username = session['username']
    message = ""
    type = ""

    syntax = conn.select("select * from barang_672019229 ORDER BY id_barang ASC")

    return render_template('index.html', message=message, type=type, username=username, data=syntax[1])

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    message = ""
    type = ""

    if request.method == 'POST':
        conn = Database('ksb-2022')

        ID = request.form['formID_daftar']
        user = request.form['formUsername_daftar']
        passw = request.form['formPassword_daftar']
        status, data = conn.crud("INSERT INTO admin_672019229(id_admin, username, password) VALUES ('{}', '{}', '{}')".format(ID, user, passw))
        if status:
            return redirect(url_for('login'))

        else:
            message = "ID, username atau password tidak pas atau sudah terdaftar"
            type = "error"
            return render_template('admin.html', message=message, type=type)

    return render_template('admin.html', message=message, type=type)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    message = ""
    type = ""

    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    username = session['username']


    if request.method == 'POST':
        conn = Database('ksb-2022')

        ID_barangs = request.form['formID_barang']
        nama_barangs = request.form['formNama_barang']
        harga_barangs = request.form['formHarga_barang']
        jumlah_barangs = request.form['formJumlah_barang']
        status, data = conn.crud("INSERT INTO barang_672019229(id_barang, nama_barang, harga_barang, jumlah_barang) VALUES('{}', '{}', '{}', '{}')".format(ID_barangs, nama_barangs, harga_barangs, jumlah_barangs))
        if status:
            return redirect(url_for('insert'))

        else:
            message= "ada kesalahan input"
            type = "error"
            return redirect(url_for('insert'))

    #return render_template('index.html', message=message, type=type, username = session['username'])
    syntax = conn.select("select * from barang_672019229 ORDER BY id_barang ASC")

    return render_template('insert.html', message=message, type=type, username=username, data=syntax[1])


@app.route('/update', methods=['GET', 'POST'])
def update():
    message = ""
    type = ""

    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    username = session['username']

    if request.method == 'POST':
        conn = Database('ksb-2022')

        ID_barang = request.form['formID_barang']
        nama_barang = request.form['formNama_barang']
        harga_barang = request.form['formHarga_barang']
        jumlah_barang = request.form['formJumlah_barang']
        status, data = conn.crud("UPDATE barang_672019229 SET nama_barang='{}', harga_barang='{}', jumlah_barang='{}' WHERE id_barang='{}'".format(nama_barang, harga_barang, jumlah_barang, ID_barang))
        if status:
            return redirect(url_for('update'))

        else:
            message = "data tidak pas atau sudah ada"
            type = "error"
            return render_template('index', message=message, type=type)
    syntax = conn.select("select * from barang_672019229 ORDER BY id_barang ASC")
    return render_template('update.html', message=message, type=type, username=username, data=syntax[1])


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    message = ""
    type = ""

    if 'username' not in session.keys():
        return redirect(url_for('login'))
    conn = Database('ksb-2022')
    username = session['username']

    if request.method == 'POST':
        conn = Database('ksb-2022')

        ID_barang = request.form['formID_barang']

        status, data = conn.crud("DELETE from barang_672019229 WHERE id_barang = '{}'".format(ID_barang))
        if status:
            return redirect(url_for('delete'))

        else:
            message = "data tidak sesuai"
            type = "error"
            return render_template('index', message=message, type=type)
    syntax = conn.select("select * from barang_672019229 ORDER BY id_barang ASC")
    return render_template('delete.html', message=message, type=type, username=username, data=syntax[1])



if __name__ == "__main__":
    app.run(port=5000,debug=True)
