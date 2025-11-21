from controllers.incapacidad_controller import IncapacidadController

def init_incapacidad_routes(app):

    app.add_url_rule("/incapacidades", view_func=IncapacidadController.index, endpoint="incapacidades_list")

    app.add_url_rule(
        "/nuevo",
        view_func=IncapacidadController.nuevo,
        methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/ver/<int:id>",
        view_func=IncapacidadController.ver,
        endpoint="ver_incapacidad"
    )

    app.add_url_rule(
        "/descargar/<nombre>",
        view_func=IncapacidadController.descargar
    )

    app.add_url_rule(
        "/editar/<int:id>",
        view_func=IncapacidadController.editar,
        methods=["GET", "POST"],
        endpoint="editar_incapacidad"
    )

    app.add_url_rule(
        "/transcribir/<int:id>",
        view_func=IncapacidadController.transcribir
    )
