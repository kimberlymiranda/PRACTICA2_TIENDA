from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app=Flask(__name__)

#conectamos con mi base de datos tienda
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tienda"
    )

#empezemos con las rutas
@app.route("/", methods=["GET", "POST"])
def home():
    errores = {}
# esto es para el 1.html validaciones 
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contraseña = request.form.get("contraseña", "").strip()

        #la validacion
        if not usuario:
            errores["usuario"] = "El usuario es un dato requerido"
        elif usuario !="LA CHINITA":
            errores["usuario"] = "El usuario es incorrecto"
        

        if not contraseña:
            errores["contraseña"] = "La contraseña es un dato requerido"
        elif contraseña != "12345":
            errores["contraseña"] = "La contraseña es incorrecta"

        
        if not errores:
            return redirect(url_for('home1'))  
    
    return render_template("inicio.html", errores = errores)




#ruta de la segunda ventana principal
@app.route("/principal")
def home1():
    return render_template("principal.html")



#ruta para la tercera ventana de los multipls botones
@app.route("/ventasvender")
def home2():
    return render_template("ventasvender.html")




#aqui va las funciones que estoy haciendo en inventario
@app.route("/inventario")
def home3():
    return render_template("inventario.html")




#aqui va las funciones que estoy haciendo en registrar preventistas
@app.route("/preventistas")
def home4():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ver_preventistas")
    ver_preventistas = cursor.fetchall()
    conn.close()
    return render_template("preventistas.html", ver_preventistas=ver_preventistas)


@app.route("/add_preventistas", methods=["POST"])
def add_preventistas():
    if request.method=="POST":
        preve_nombre = request.form['preve']
        total_pago = request.form['total_pago']
        fecha_entrada = request.form['fecha_entrada']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO ver_preventistas (nombre, total_pago, fecha_entrada) 
                        VALUES (%s, %s, %s)""", (preve_nombre, total_pago, fecha_entrada))
        conn.commit()
        conn.close()

        return redirect('/preventistas')
    return render_template("add_preventistas.html", preve="")




#aqui va las funciones que estoy haciendo en ver preventistas
@app.route("/verpreventistas", methods=["GET", "POST"])
def home5():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ver_preventistas")
    ver_preventistas = cursor.fetchall()
    conn.close()
    return render_template("verpreventistas.html", preve=ver_preventistas)
@app.route('/delete_preventistas/<int:id>', methods=['POST'])
def delete_preventistas(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ver_preventistas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/verpreventistas')









#aqui va las funciones que estoy haciendo en ver ventas
@app.route("/verventas", methods=["GET"])
def home6():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ver_ventas")
    ver_ventas = cursor.fetchall()
    conn.close()
    return render_template("verventas.html", ven=ver_ventas)

@app.route('/delete_ventas/<int:id>', methods=['POST'])
def delete_ventas(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ver_ventas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/verventas')












if __name__ == "__main__":
    app.run(debug=True)