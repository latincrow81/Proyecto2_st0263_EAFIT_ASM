from flask import Response, request, flash, render_template
from flask_login import login_required

from app.forms import CreatePoolForm, DeletePoolForm
from app.services import crear_instancia, eliminar_instancia
from app.repositories import agregar_pool, agregar_instancia, buscar_pool, instancias_por_pool_id
from app.views import main_blueprint


