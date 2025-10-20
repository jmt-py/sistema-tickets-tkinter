
from models import GestorTickets, GestorUsuarios, GestorTecnicos
from utils import CampoVacio, FormatoEmailInvalido, OpcionNoValida, validar_prioridad, cadena_no_vacia, id_no_vacio


def main():

    gestor_usuarios=GestorUsuarios()
    gestor_usuarios.cargar_usuarios_json()
    gestor_tecnicos=GestorTecnicos()
    gestor_tecnicos.cargar_json_tecnicos()
    gestor = GestorTickets(gestor_usuarios, gestor_tecnicos)
    gestor.cargar_json()
    print("Bienvenido")
    while True:


        print("\n1- Crear nuevo ticket.")
        print("2- Crear nuevo Usuario.")
        print("3- Crear nuevo Tecnico.")
        print("4- Listar tickets.")
        print("5- Listar Usuarios.")
        print("6- Listar Tecnicos")
        print("7- Buscar ticket por ID.")
        print("8- Cambiar estado de un ticket.")
        print("9- Asginar Tecnico a un Ticket")
        print("0- Salir")
        try:
            op=int(input(": "))
            match op:
                case 1:
                    if len(gestor_usuarios.lista_usuarios)<=0:
                        print("Se requiere registrar al menos un usuario para poder generar un ticket.")
                        continue

                    id_usuario=id_no_vacio("ID del usuario: ")
                    descripcion=cadena_no_vacia("Descripcion del ticket(motivo): ")
                    prioridad=validar_prioridad("Prioridad del ticket [alta, media, baja] : ")

                    if gestor.crear_ticket(id_usuario, descripcion, prioridad):
                        print(f"Ticket creado exitosamente. ")
                    else:
                        print(f"No se pudo crear el ticket. ")
                case 2:
                    nombre_u=cadena_no_vacia("Nombre del usuario: ")
                    email_u=cadena_no_vacia("Email del usuario: ")
                    nuevo_usuario=gestor_usuarios.crear_usuario(nombre_u, email_u)
                    print(f"Usuario creado con ID: {nuevo_usuario.id}")

                case 3:
                    nombre_t=cadena_no_vacia("Nombre del tecnico: ")
                    especialidad=cadena_no_vacia("Area de especialidad del tecnico: ")
                    nuevo_tecnico=gestor_tecnicos.crear_tecnico(nombre_t, especialidad)
                    print(f"Tecnico creado con ID: {nuevo_tecnico.id}")

                case 4:
                    print(gestor.listar_tickets())
                case 5:
                    print(gestor_usuarios.listar_usuarios())
                case 6:
                    print(gestor_tecnicos.listar_tecnicos())
                case 7:
                    id_ticket=id_no_vacio("ID del ticket: ")
                    ticket=gestor.buscar_ticket(id_ticket)
                    if ticket:
                        print(ticket)
                    else:
                        print(f"El ticket con ID: '{id_ticket}' no fue encontrado.")
                case 8:
                    id_ticket=id_no_vacio("ID del ticket: ")
                    ticket=gestor.buscar_ticket(id_ticket)

                    if not ticket:
                        print(f"No se encontró un ticket con ese ID.")
                        continue
                    print(f"Estado actual del ticket con ID: {id_ticket}    | {ticket.estado}"  )
                    est=cadena_no_vacia("Desea cambiar el estado actual del ticket? Y/N: ")
                    if est=="y":
                        if gestor.cambiar_estado(id_ticket):
                            print(f"Se cambio el estado del ticket.")
                        else:
                            print(f"No se pudo cambiar el estado del ticket.")
                    else:
                        print(f"Se cancelo el cambio de estado del ticket. ")

                case 9:
                    id_ticket=id_no_vacio("ID del ticket: ")
                    id_tecnico=id_no_vacio("ID del Tecnico: ")
                    if gestor.asignar_tecnico(id_ticket, id_tecnico):
                        print(f"Se asigno al tecnico con ID:{id_tecnico} al ticket con ID: {id_ticket}")
                    else:
                        print(f"No se pudo realizar esta accion")

                case 0:
                    print("Adios...")
                    break
                case _:
                    print("Opcion no valida, intente de nuevo.")
        except (CampoVacio, FormatoEmailInvalido, OpcionNoValida, Exception) as e:
            print(f"Error {e}")

if __name__=="__main__":
    main()