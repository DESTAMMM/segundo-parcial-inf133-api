from flask import Blueprint, request, jsonify
from models.tarea_model import Task
from views.tarea_view import render_task_list, render_task_detail
from utils.decorator import jwt_required, roles_required

task_bp = Blueprint("task", __name__)


@task_bp.route("/taks", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "member"])
def get_tasks():
    tasks = Task.get_all()
    return jsonify(render_task_list(tasks))

@task_bp.route("/taks/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "member"])
def get_task(id):
    task = Task.get_by_id(id)
    if task:
        return jsonify(render_task_detail(task))
    return jsonify({"error": "tarea no encontrado"}), 404

@task_bp.route("/taks", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_task():
    data = request.json
    title= data.get("title")
    description= data.get("description")
    status= data.get("status")
    created_at=data.get("created_at")
    assigned_to =data.get("assigned_to")


    if not title or not description or status or created_at or assigned_to is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    task = Task(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    task.save()

    return jsonify(render_task_detail(task)), 201


@task_bp.route("/taks/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_task(id):
    task = Task.get_by_id(id)

    if not task:
        return jsonify({"error": "tarea no encontrada"}), 404

    data = request.json
    title= data.get("title")
    description= data.get("description")
    status= data.get("status")
    created_at=data.get("created_at")
    assigned_to =data.get("assigned_to")

    task.update(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)

    return jsonify(render_task_detail(task))

@task_bp.route("/taks/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarea no encontrado"}), 404
    task.delete()
    return "", 204