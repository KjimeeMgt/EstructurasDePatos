from ..database.database import get_connection, init_db
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

def create_app():
    app = Flask(__name__)
    init_db()
    
    def check_api_key():
        api_key = request.headers.get("X-API-KEY")
        return api_key != os.getenv("API_KEY")

    def get_user_from_token():
        token = request.headers.get("Authorization")
        if not token:
            return None

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM tokens WHERE token = ?", (token,))
        row = cursor.fetchone()

        return row["user_id"] if row else None
    
    @app.route("/")
    def index():    
        if check_api_key():
            return jsonify({"error": "API key inválida"}), 401
        return jsonify({"message": "API de TODOs funcionando"})


    # ----------------------------
    # Crear usuario
    # POST /users
    # { "username": "admin", "password": "1234" }
    # ----------------------------
    @app.post("/users")
    def create_user():
        data = request.json
        username = data.get("username")
        password = data.get("password")


        if not username or not password:
            return jsonify({"error": "username y password requeridos"}), 400

        hashed = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()
        except:
            return jsonify({"error": "El usuario ya existe"}), 400

        return jsonify({"message": "Usuario creado"}), 201


    # ----------------------------
    # Login
    # POST /login
    # { "username": "admin", "password": "1234" }
    # ----------------------------
    @app.post("/login")
    def login():
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        print("Login attempt:", username)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        cursor.execute("SELECT token FROM tokens WHERE user_id = ?", (user["id"],))
        existing_token = cursor.fetchone()

        if existing_token:
            token = existing_token["token"]
        else:
            token = secrets.token_hex(32)

            cursor.execute(
            "INSERT INTO tokens (user_id, token) VALUES (?, ?)",
            (user["id"], token)
            )
            conn.commit()

        return jsonify({"token": token})
    
    @app.post("/logout")
    def logout():
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401

        token = request.headers.get("Authorization")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tokens WHERE token = ?", (token,))
        conn.commit()

        return jsonify({"message": "Logout exitoso"})
    
    @app.post("/register")
    def register():
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "username y password requeridos"}), 400

        hashed = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()
        except:
            return jsonify({"error": "El usuario ya existe"}), 400

        return jsonify({"message": "Usuario registrado"}), 201


    # ----------------------------
    # Obtener todos del usuario autenticado
    # GET /todos
    # ----------------------------
    @app.get("/todos")
    def list_todos():
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM todos WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

        todos = [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"])
            }
            for row in rows
        ]

        return jsonify(todos)


    # ----------------------------
    # Crear
    # POST /todos
    # ----------------------------
    @app.post("/todos")
    def create_todo():
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401

        title = request.json.get("title")
        if not title:
            return jsonify({"error": "title requerido"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO todos (user_id, title) VALUES (?, ?)",
            (user_id, title)
        )
        conn.commit()

        return jsonify({"message": "TODO creado"}), 201


    # ----------------------------
    # Actualizar
    # PUT /todos/<id>
    # ----------------------------
    @app.put("/todos/<int:todo_id>")
    def update_todo(todo_id):
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401

        data = request.json
        title = data.get("title")
        done = data.get("done")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()

        if not todo:
            return jsonify({"error": "TODO no encontrado"}), 404

        if todo["user_id"] != user_id:
            return jsonify({"error": "No autorizado"}), 403

        cursor.execute(
            "UPDATE todos SET title = ?, done = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (title, int(done), todo_id)
        )
        conn.commit()

        return jsonify({"message": "TODO actualizado"})


    # ----------------------------
    # Borrar
    # DELETE /todos/<id>
    # ----------------------------
    @app.delete("/todos/<int:todo_id>")
    def delete_todo(todo_id):
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({"error": "Token inválido"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()

        if not todo:
            return jsonify({"error": "TODO no encontrado"}), 404

        if todo["user_id"] != user_id:
            return jsonify({"error": "No autorizado"}), 403

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()

        return jsonify({"message": "TODO eliminado"})

    return app
