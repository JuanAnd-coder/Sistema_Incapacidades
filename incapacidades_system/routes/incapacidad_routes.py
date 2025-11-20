from controllers.incapacidad_controller import IncapacidadController

def init_incapacidad_routes(app):

    app.add_url_rule("/", view_func=IncapacidadController.index)

    app.add_url_rule(
        "/nuevo",
        view_func=IncapacidadController.nuevo,
        methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/ver/<int:id>",
        view_func=IncapacidadController.ver
    )

    app.add_url_rule(
        "/descargar/<nombre>",
        view_func=IncapacidadController.descargar
    )

    app.add_url_rule(
        "/transcribir/<int:id>",
        view_func=IncapacidadController.transcribir
    )
