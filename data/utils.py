
class ErrorSistemaTickets(Exception):
    pass

prioridad={"alta", "media", "baja"}

class CampoVacio(ErrorSistemaTickets):
    def __str__(self):
        return f"Este campo no puede estar vacio"
class FormatoEmailInvalido(ErrorSistemaTickets):
    def __str__(self):
        return f"Formato de email no valido"
class OpcionNoValida(ErrorSistemaTickets):
    def __str__(self):
        return f"Error, la prioridad debe ser [alta, media, baja]"

def cadena_no_vacia(campo:str):
    while True:
        valor=input(campo).strip().lower()
        if not valor:
            print("Este campo no puede estar vacio.")
            continue
        else:
            return valor

def cadena_no_vacia_tk(valor:str):
    if not valor.strip():
        raise ValueError("No se permiten campos vacios.")

def validar_email(valor:str):
    if not valor.strip():
        raise ValueError("El campo email no puede estar vacio.")
    if "@" not in valor or '.' not in valor:
        raise ValueError("Email no valido.")
    return True

def validar_prioridad(campo:str):
    while True:
        pri=input(campo).strip().lower()
        if pri not in prioridad:
            print("Debes elegir una prioridad valida: 'alta'  'media'   'baja'")
            continue
        elif not pri:
            print("Este campo no puede estar vacio.")
            continue
        else:
            return pri

def id_no_vacio(campo):
    while True:
        try:
            num=int(input(campo))
            return num
        except ValueError:
            print("La ID debe constar unicamente de numeros")
