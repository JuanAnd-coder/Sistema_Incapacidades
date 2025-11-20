def identificar_tipo_documento(nombre):
    nombre = nombre.lower()

    if "epic" in nombre:
        return "Epicrisis"
    if "furip" in nombre:
        return "FURIPS"
    if "registro" in nombre:
        return "Registro Civil"
    if "nac" in nombre or "cert" in nombre:
        return "Certificado Nacido Vivo"

    return "Soporte incapacidad"
