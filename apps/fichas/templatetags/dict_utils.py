from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a un valor de diccionario usando una llave dinámica"""
    return dictionary.get(key)

from django import template

register = template.Library()

@register.filter
def iniciales(usuario_obj):
    # Convertimos el objeto a string por si acaso
    nombre_completo = str(usuario_obj).strip()
    
    if not nombre_completo or nombre_completo == "None":
        return "??"

    # Dividimos el nombre por espacios
    partes = nombre_completo.split()
    
    if len(partes) >= 2:
        # Si tiene nombre y apellido: Primera letra de ambos
        return f"{partes[0][0]}{partes[1][0]}".upper()
    elif len(partes) == 1:
        # Si solo hay un nombre: Las dos primeras letras
        return partes[0][:2].upper()
    
    return "??"