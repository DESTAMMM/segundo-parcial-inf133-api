from flask import Blueprint, request, jsonify
from models.user_model import Worker
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

worker_bp = Blueprint("worker", __name__)


@worker_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    roles = data.get("roles")

    if not name or not password or not email:
        return jsonify({"error": "Se requieren nombre de usuario, email y contraseña"}), 400

    existing_worker = Worker.find_by_name(name)
    if existing_worker:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_worker = Worker(name, email,  password, roles)
    new_worker.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@worker_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    worker = Worker.find_by_email(email)
    if worker and check_password_hash(worker.password_hash, password):
        access_token = create_access_token(
            identity={"email": email, "roles": worker.roles}
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401