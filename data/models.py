
import json
import os.path

from utils import CampoVacio, FormatoEmailInvalido
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
archivo=os.path.join(BASE_DIR,"src","SistemaTickets.json")
usuariosJSON=os.path.join(BASE_DIR, "src","usuarios.json")
tecnicosJSON=os.path.join(BASE_DIR,"src", "tecnicos.json")

class Usuario:
    def __init__(self, nombre:str, email:str, id:int):
        self.nombre=nombre
        self.email=email
        self.id=id

    def to_dict(self):
        datos_usuario={"nombre":self.nombre,
                       "email":self.email,
                       "id":self.id}
        return datos_usuario

    def __str__(self):
        return f"Nombre: {self.nombre}  | Email: {self.email}    | ID: {self.id}"

    @classmethod
    def from_dict(cls, data):
        usuario=Usuario(data["nombre"], data["email"], int(data["id"]))
        return usuario

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        if len(value)<3 or not value:
            raise CampoVacio("El nombre debe contar con mas de 3 letras y debe estar compuesto de letras.")
        self._nombre=value
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value or len(value)<3 or not value:
            raise FormatoEmailInvalido("Email ingresado no valido.")
        self._email=value

class GestorUsuarios:
    def __init__(self):
        self.lista_usuarios=[]
        self.contadorIDU=0


    def crear_usuario(self, nombre, email):
        nuevo_usuario=Usuario(nombre, email, self.contadorIDU)
        self.lista_usuarios.append(nuevo_usuario)
        self.contadorIDU+=1
        self.guardar_usuarios_json()
        return nuevo_usuario


    def buscar_usuario(self, id_usuario):
        for user in self.lista_usuarios:
            if user.id==id_usuario:
                return user
        return None

    def eliminar_usuario(self, id_usuario):
        usuario=self.buscar_usuario(id_usuario)
        if not usuario:
            return False
        self.lista_usuarios.remove(usuario)
        self.guardar_usuarios_json()
        return True

    def listar_usuarios(self):
        reporte=""
        for usuario in self.lista_usuarios:
            reporte+=f"{usuario}\n"
        return reporte

    def guardar_usuarios_json(self):
        dict_usuarios={
            "usuario":[u.to_dict() for u in self.lista_usuarios],
            "contadorIDU":self.contadorIDU
        }

        if not os.path.exists(os.path.join(BASE_DIR, "src")):
            os.makedirs(os.path.join(BASE_DIR, "src"))

        with open(usuariosJSON, "w") as file:
            json.dump(dict_usuarios, file ,indent=4)

    def cargar_usuarios_json(self):
        if not os.path.exists(usuariosJSON) or os.path.getsize(usuariosJSON)==0:
            self.lista_usuarios=[]
            self.contadorIDU=0
            return

        with open(usuariosJSON, "r") as file:
            datos=json.load(file)
            self.contadorIDU=datos["contadorIDU"]
            self.lista_usuarios=[Usuario.from_dict(u) for u in datos["usuario"]]

class Tecnico:
    def __init__(self, nombre:str, especialidad:str, id:int):
        self.nombre=nombre
        self.especialidad=especialidad
        self.id=id
    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Especialidad: {self.especialidad} "


    def to_dict(self):
        tecnico={"nombre":self.nombre,
                 "especialidad":self.especialidad,
                 "id":self.id}
        return tecnico
    @classmethod
    def from_dict(cls, data):
        tecnico=Tecnico(data["nombre"], data["especialidad"], int(data["id"]))
        return tecnico

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        if len(value)<3 or not value:
            raise CampoVacio("El nombre debe contar con mas de 3 letras y debe estar compuesto de letras.")
        self._nombre=value
    @property
    def especialidad(self):
        return self._especialidad
    @especialidad.setter
    def especialidad(self, value):
        if len(value)<3 or not value:
            raise CampoVacio("Este campo requiere minimo 3 caracteres.")
        self._especialidad=value

class Ticket:
    def __init__(self, id:int ,descripcion:str, prioridad:str, id_usuario:int, id_tecnico:int ,estado:str="pendiente"):
        self.id=id
        self.descripcion=descripcion
        self.prioridad=prioridad
        self.id_usuario=id_usuario
        self.id_tecnico=id_tecnico
        self.estado = estado

    def cambiar_estado(self):
        if self.estado=="pendiente":
            self.estado="completado"
        elif self.estado=="completado":
            self.estado="pendiente"

    def to_dict(self):
        ticket={"id":self.id,
                "descripcion":self.descripcion,
                "prioridad":self.prioridad,
                "id_usuario":self.id_usuario,
                "id_tecnico":self.id_tecnico,
                "estado": self.estado
                }
        return ticket

    @classmethod
    def from_dict(cls, data):

        ticket=Ticket(int(data["id"]),
                      data["descripcion"],
                      data["prioridad"],
                      int(data["id_usuario"]),
                      #int(data["id_tecnico"]) if data["id_tecnico"] is not None else None,
                      int(data["id_tecnico"]) if data.get("id_tecnico") is not None else None,
                      data["estado"]
                      )

        return ticket

    def __str__(self):
        return f"ID ticket: {self.id} | ID Usuario: {self.id_usuario} | ID Tecnico:{self.id_tecnico if self.id_tecnico else 'Sin asignar'} | Estado: {self.estado} | Prioridad: {self.prioridad} | Descripcion: {self.descripcion}"


class GestorTecnicos:

    def __init__(self):
        self.lista_tecnicos=[]
        self.contadorIDT=0

    def buscar_tecnico(self, id_tecnico):
        for tecnico in self.lista_tecnicos:
            if tecnico.id==id_tecnico:
                return tecnico
        return None

    def crear_tecnico(self, nombre, especialidad):
        nuevo_tecnico=Tecnico(nombre, especialidad, self.contadorIDT)
        self.lista_tecnicos.append(nuevo_tecnico)
        self.contadorIDT+=1
        self.guardar_json_tecnicos()
        return nuevo_tecnico

    def listar_tecnicos(self):
        reporte=""
        for tecnico in self.lista_tecnicos:
            print(tecnico)

    def eliminar_tecnico(self, id_tecnico):
       tecnico=self.buscar_tecnico(id_tecnico)
       if not tecnico:
           return False
       else:
           self.lista_tecnicos.remove(tecnico)
           self.guardar_json_tecnicos()
           return True

    def guardar_json_tecnicos(self):
        dict_tecnicos={
            "tecnico":[t.to_dict() for t in self.lista_tecnicos],
            "contadorIDT":self.contadorIDT
        }

        if not os.path.exists(os.path.join(BASE_DIR, "src")):
            os.makedirs(os.path.join(BASE_DIR, "src"))
        
        with open(tecnicosJSON, "w") as file:
            json.dump(dict_tecnicos,file, indent=4)

    def cargar_json_tecnicos(self):
        if not os.path.exists(tecnicosJSON) or os.path.getsize(tecnicosJSON)==0:
            self.lista_tecnicos=[]
            self.contadorIDT=0
            return
        with open(tecnicosJSON, "r")as file:
            datos=json.load(file)
            self.contadorIDT=datos["contadorIDT"]
            self.lista_tecnicos=[Tecnico.from_dict(t) for t in datos["tecnico"]]


class GestorTickets:

    def __init__(self, gestor_usuarios:GestorUsuarios, gestor_tecnicos:GestorTecnicos):
        gestor_usuarios.cargar_usuarios_json()
        gestor_tecnicos.cargar_json_tecnicos()
        self.usuarios = gestor_usuarios
        self.tecnicos = gestor_tecnicos
        self.lista_tickets=[]
        self.contador=0



    def crear_ticket(self, id_usuario:int, descripcion, prioridad, id_tecnico=None):
        if not self.usuarios.buscar_usuario(id_usuario):
            return False
        nuevo_ticket=Ticket(self.contador,descripcion, prioridad, id_usuario, id_tecnico)
        self.lista_tickets.append(nuevo_ticket)
        self.contador+=1
        self.guardar_json()
        return True

    def listar_tickets(self):
        if len(self.lista_tickets)==0:
            return f"Aun no se generaron tickets. "
        reporte=""
        reporte+=f"{'ID|':<7}{'Usuario':<20}{'Email':<20}{'Prioridad':<15}{'Estado':<25}{'Tecnico':<20}{'Descripcion'}\n"
        reporte+=f"-"*170+"\n"

        for ticket in self.lista_tickets:

            user=self.usuarios.buscar_usuario(ticket.id_usuario)
            tecni=self.tecnicos.buscar_tecnico(ticket.id_tecnico)
            nombre_tecnico=tecni.nombre if tecni else 'sin asignar'
            nombre_usuario=user.nombre if user else 'usuario eliminado'
            mail_usuario=user.email if user else 'no encontrado'
            reporte+=f"{ticket.id:<5}|{nombre_usuario:<20}{mail_usuario:<20}{ticket.prioridad:<15}{ticket.estado:<25}{nombre_tecnico:20}{ticket.descripcion}\n"
        reporte+=f"-"*170
        return reporte

    def buscar_ticket(self, id:int):
        for ticket in self.lista_tickets:
            if ticket.id==id:
                return ticket
        return None


    def cambiar_estado(self, id:int):
        ticket=self.buscar_ticket(id)
        if ticket.estado=="pendiente":
           ticket.estado="completado"
           self.guardar_json()
           return True
        if ticket.estado=="completado":
            ticket.estado="pendiente"
            self.guardar_json()
            return True
        return False

    def cambiar_prioridad(self, id:int, nueva_prioridad):
        ticket=self.buscar_ticket(id)
        if ticket:
           ticket.prioridad=nueva_prioridad
           self.guardar_json()
           return True
        return False

    def asignar_tecnico(self, id_ticket:int, id_tecnico:int):
        ticket=self.buscar_ticket(id_ticket)
        tecnico=self.tecnicos.buscar_tecnico(id_tecnico)
        if ticket and tecnico:
            ticket.id_tecnico=tecnico.id
            self.guardar_json()
            return True
        return False


    def guardar_json(self):

        dict_tickets={
            "ticket":[t.to_dict() for t in self.lista_tickets],
            "contador":self.contador
        }

        if not os.path.exists(os.path.join(BASE_DIR, "src")):
            os.makedirs(os.path.join(BASE_DIR, "src"))

        with open(archivo, "w" ) as file:
            json.dump(dict_tickets, file, indent=4)

    def cargar_json(self):
        if not os.path.exists(archivo) or os.path.getsize(archivo)==0:
            self.contador=0
            self.lista_tickets=[]
            return
        with open(archivo, "r") as file:
            datos=json.load(file)
            self.contador=datos["contador"]
            self.lista_tickets=[Ticket.from_dict(t) for t in datos["ticket"]]




