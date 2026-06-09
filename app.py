from flask import Flask
import psycopg2

app = Flask(__name__)
VERSION = "3.0.0"

@app.route("/")
def inicio():
    try:
        # Nos conectamos al contenedor 'db'
        conexion = psycopg2.connect(
            host="db",
            database="empresa",
            user="admin",
            password="admin123"
        )
        cursor = conexion.cursor()

        # Obtener versión de la Base de Datos
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        # Actividad 5: Intentar leer los clientes de la tabla
        cursor.execute("SELECT id, nombre FROM clientes;")
        clientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        # Formatear la lista de clientes en HTML
        lista_html = ""
        for cliente in clientes:
            lista_html += f"<li><strong>ID:</strong> {cliente[0]} - <strong>Nombre:</strong> {cliente[1]}</li>"

        if not lista_html:
            lista_html = "<li>No hay clientes registrados aún.</li>"

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p style="color: green;"><strong>Conexión exitosa a PostgreSQL</strong></p>
        <p><strong>DB Info:</strong> {db_version[0]}</p>
        <hr>
        <h3>Lista de Clientes (Actividad 5):</h3>
        <ul>
            {lista_html}
        </ul>
        """
    except Exception as e:
        # Si la tabla aún no está creada, nos avisará amigablemente
        return f"""
        <h1>Aplicación Flask (Versión {VERSION})</h1>
        <p style="color: orange;"><strong>Conectado a PostgreSQL, pero falta crear la tabla o hay un detalle:</strong></p>
        <p>{str(e)}</p>
        <p><em>Ve a pgAdmin (localhost:8080) para ejecutar el script de las Actividades 3 y 4.</em></p>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)