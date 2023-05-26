from flask import Blueprint
from flask import Response, request, flash, render_template
from flask_login import login_required

from app.forms import CreatePoolForm, DeletePoolForm
from app.services import crear_instancia, eliminar_instancia
from app.repositories import agregar_pool, agregar_instancia, buscar_pool, instancias_por_pool_id

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return render_template('index.html')

@login_required
@main_blueprint.route('/crear-pool', methods=['GET', 'POST'])
def crear_pool():
    form = CreatePoolForm(request.form)
    if form.validate_on_submit():
        # crear pool en bd
        pool = agregar_pool(form.pool_name.data)
        # crear instancias iniciales
        instance_1 = crear_instancia()
        instance_2 = crear_instancia()
        # agregar instancias a bd
        agregar_instancia(pool_id=pool.id, instance_id=instance_1[0].instanceId)
        agregar_instancia(pool_id=pool.id, instance_id=instance_2[0].instanceId)

        return Response(status=200, response=f"pool creado con 2 nodos, {instance_1[0].instanceId} y {instance_2[0].instanceId}")
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')

    return render_template('crear-pool.html', form=form)


@login_required
@main_blueprint.route('/eliminar-pool', methods=['GET', 'POST'])
def eliminar_pool():
    form = DeletePoolForm(request.form)
    if form.validate_on_submit():
        pool = buscar_pool(form.pool_name.data)
        instances = instancias_por_pool_id(pool.id)
        for instance in instances:
            eliminar_instancia(instance_id=instance.id)
        return Response(status=200, response="pool eliminado")
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('eliminar-pool.html', form=form)
