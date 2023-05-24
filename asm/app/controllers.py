from flask import Response, request, flash, render_template
from flask_login import login_required

from app.forms import CreatePoolForm, DeletePoolForm
from app.services import crear_instancia, eliminar_instancia
from app.repositories import agregar_pool, agregar_instancia, buscar_pool, instancias_por_pool_id


@login_required
def crear_pool(pool_name):
    form = CreatePoolForm(request.form)
    if form.validate_on_submit():
        # crear pool en bd
        pool = agregar_pool(pool_name)
        # crear instancias iniciales
        instance_1 = crear_instancia()
        instance_2 = crear_instancia()
        # agregar instancias a bd
        agregar_instancia(pool_id=pool.id, instance_id=instance_1.instanceId)
        agregar_instancia(pool_id=pool.id, instance_id=instance_2.instanceId)

        return Response(status=200, response=f"pool creado con 2 nodos, {instance_1.instanceId} y {instance_2.instanceId}")
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')

    return render_template('crear-pool.html', form=form)


@login_required
def eliminar_pool(pool_name):
    form = DeletePoolForm(request.form)
    if form.validate_on_submit():
        pool = buscar_pool(pool_name)
        instances = instancias_por_pool_id(pool.id)
        for instance in instances:
            eliminar_instancia(instance_id=instance.id)
        return Response(status=200, response="pool eliminado")
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('eliminar-pool.html', form=form)
