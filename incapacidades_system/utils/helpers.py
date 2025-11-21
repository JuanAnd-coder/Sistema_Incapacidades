def identificar_tipo_documento(nombre):
    """
    Identifica el tipo de documento basándose en el nombre del archivo.
    Retorna uno de: Epicrisis, FURIPS, Registro Civil, Certificado Nacido Vivo, Soporte incapacidad
    """
    nombre_lower = nombre.lower()
    
    # Priorizar búsquedas más específicas primero
    if "epicrisis" in nombre_lower or "epic" in nombre_lower:
        return "Epicrisis"
    if "furips" in nombre_lower or "furip" in nombre_lower:
        return "FURIPS"
    if "registro civil" in nombre_lower or ("registro" in nombre_lower and "civil" in nombre_lower):
        return "Registro Civil"
    if "certificado nacido vivo" in nombre_lower or ("certificado" in nombre_lower and "nacido" in nombre_lower):
        return "Certificado Nacido Vivo"
    if "nacido vivo" in nombre_lower or ("nacido" in nombre_lower and "vivo" in nombre_lower):
        return "Certificado Nacido Vivo"
    
    # Si contiene palabras clave de soporte/incapacidad, es soporte
    if "soporte" in nombre_lower or "incapacidad" in nombre_lower or "incap" in nombre_lower:
        return "Soporte incapacidad"
    
    # Por defecto, asumir que es soporte de incapacidad
    return "Soporte incapacidad"
