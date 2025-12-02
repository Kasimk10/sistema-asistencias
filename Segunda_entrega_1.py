import json
import os
#Menús--------------------------------------

def menu_inicial():

    """Muestra el menú principal del sistema con las opciones para alumno, profesor y administrador."""

    print()
    print("-----Menú Principal-----")
    print()
    print("1- Ingresar como Alumno")
    print("2- Ingresar como Profesor")
    print("3- Ingresar como Administrador")
    print()
    print("-------------------------")

def menu_profesor():

    """Muestra el menú específico para profesores con opciones de crear clase y ver asistencias."""

    print()
    print("-----Menú Profesor-----")
    print()
    print("1- Pasar lista")
    print("2- Ver asistencia de una clase")
    print("3- Ver asistencia de un alumno")
    print("4- Modificar asistencia de un alumno")
    print("5- Ver mis clases asignadas")
    print("0- Salir")
    print()
    print("-----------------------")

def menu_administrador():

    """Muestra el menú específico para administradores con opciones de gestión de alumnos y visualización de asistencias."""

    print()
    print("-----Menú Administrador-----")
    print()
    print("1- Cargar alumno")
    print("2- Eliminar alumno")
    print("3- Modificar alumno (Datos y/o inscripcion)")
    print("4- Visualizar asistencia por cursos")
    print("5- Reiniciar sistema")
    print("0- Salir")
    print()
    print("----------------------------")

def menu_estudiante():

    print()
    print("----Menú Estudiante----")
    print()
    print("1- Ver asistencias de todas mis materias")
    print("2- Ver asistencia de una materia")
    print("0- Salir")
    print()
    print("------------------------")
    print()    

def menu_login(uso):

    '''
    Muestra el menú del login
    '''

    print()
    print("-----Inicie Sesion-----")
    print()

    if uso == 1:
        usuario = input("Ingrese su usuario o 0 para ir atras: ").strip()

    else:

        while True:

            try:
                
                usuario = int(input("Ingrese su legajo o 0 para ir atras: "))

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break

    if usuario != "0" and usuario != 0:
        contrasena = input("Ingrese su contraseña 0 para ir atras: ").strip()

    else: 
        contrasena = "0"
    
    print()
    print("------------------------")
    print()

    return usuario, contrasena

#Validaciones----------------------------------

def validar_entre(num, minimo, maximo):
    
    '''
    Valida que un numero se encuentre entre dos valores (min, max).
    Si esta por fuera lo vuelve a solicitar.
    
    '''

    while num < minimo or num > maximo:

        while True:
            try:
                print(f"ERROR! El numero debe estar entre {minimo} y {maximo}.")
                num = int(input("Intentelo nuevamente: "))
            
            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break     

    return num

def validacion_log_in(usuario, contrasena): #usuario ingresado, contraseña ingresada

    
    registro = False
    archivo = open("contrasena.json", "r")
    datos = json.load(archivo)

    if usuario in datos:

        if contrasena == datos[usuario]:

            registro = True
        
        else:
            registro = False
    
    else:
        registro = False
    
    archivo.close()
    return registro

def validar_id_clase(id_clase, estudiantes, legajo):

    clases = estudiantes[legajo]["Clases Mañana"] + estudiantes[legajo]["Clases Tarde"] + estudiantes[legajo]["Clases Noche"]

    if id_clase in clases:
        return True
    
    else:
        return False

def validar_string(palabra, lista):

    '''
    Valida que una palabra este en una lista
    '''

    while palabra not in lista:
        print("ERROR! Ingrese una opcion valida.")
        print("Opciones validas: ", end="| ")
        for elementos_validos in lista:
            print(f"{elementos_validos} |", end=" ")
        palabra = input("Intentelo nuevamente: ").title().strip()
    
    return palabra

def validar_nuevo_nombre(nombre):

    caracteres = list(nombre)
    validacion = True

    for caracter in caracteres:

        if caracter.isdigit():
            validacion = False
            break
    
    return validacion

#Funciones especificas--------------------------

def mostrar_asistencia_todas(legajo):

    '''
    Muestra las asistencias de todas las materias a la cual el estudiante esta anotado.
    En formato de tabla
    '''

    asistencia_alumno = leer_archivo(legajo, "asistencia_alumnos")
    
    clases = list(asistencia_alumno.keys()) #Lista con los ids de las clases a las que el alumno esta anotado

    if len(clases) == 0:
        print("No estas anotado a ninguna materia")
        return
    
    cant_filas = len(asistencia_alumno[clases[0]]) #Cantidad de filas que va a tener la tabla (cantidad de dias precargdos)

    print("-" * (30 * len(clases) + len(clases)))  # Línea divisora
    for materia in clases: #Recorre cada id de clase
        
        info_clase = leer_archivo(materia, "ids_clases")
        nombre_materia = info_clase[0]  # Obtiene el nombre de la materia de la clase.
        print(f"{nombre_materia:^30}|", end="")

    print() #Para que el proximo print vaya una linea abajo
    print("-" * (30 * len(clases) + len(clases)))  # Línea divisora

    for fila in range (cant_filas):
        
        for id_clase in clases: #Recorre cada id de clase (materia)

            fecha = asistencia_alumno[id_clase][fila][0]    # Obtener fecha
            estado = asistencia_alumno[id_clase][fila][1]   # Obtener estado
            
            print(f"{fecha:^14}->{estado:^14}|", end="")  # Imprimir fecha y estado

        print() #Para que el proximo print vaya una linea abajo
    
    print("-" * (30 * len(clases) + len(clases)))  # Línea divisora
    print()

def mostrar_clases_anotadas(datos_estudiante):
    '''
    Muestra las clases a las que el alumno esta anotado
    '''

    print()
    cont=1
    clases = []
    print("-" * 54)
    print(f"|{'Opcion N°':^10}|{'ID Clase':^10}|{'Materia':^30}|")
    print("-" * 54)

    for turno in ["Clases Mañana", "Clases Tarde", "Clases Noche"]: #Recorre los turnos

        for id_clase in datos_estudiante[turno]: #Recorre los ids de clase en cada turno

            info_clase = leer_archivo(id_clase, "ids_clases")
            nombre_materia = info_clase[0]  # Obtiene el nombre de la materia de la clase.

            print(f"|{cont:^10}|{id_clase:^10}|{nombre_materia:^30}|")
            print("-" * 54)
            cont += 1
            clases.append(id_clase) #Guarda los ids de las clases en una lista para despues validar que la opcion ingresada este entre las clases anotadas
    print()
    return clases

def mostrar_asistencia_simple(nombre, id_clase, legajo):

    asistencia_alumno = leer_archivo(legajo, "asistencia_alumnos")


    print(f"Imprimiendo asistencias de {nombre} en la clase {id_clase}...")
    print()
    encabezados = ["Fecha", "Estado"]
    
    print("-" * 26)
    print(f"|{encabezados[0]:^12}|{encabezados[1]:^12}|")

    print("-" * 27)

    for fila in asistencia_alumno[id_clase]:

        print(f"|{fila[0]:^12}|{fila[1]:^12}|")
        print("-" * 27)
    print()

def mostrar_clases_asignadas(lista):

    print()
    print("Clases asignadas: ")
    print()

    print("-" * 85)
    print(f"{'Opcion N°':^10}|{'ID Clase':^10}|{'Materia':^30}|{'Dia':^15}|{'Turno':^15}|")
    print("-" * 85)
    contador = 1
    for id in lista:

        info_clase = leer_archivo(str(id), "ids_clases")

        print (f"{contador:^10}|{id:^10}|{info_clase[0]:^30}|{info_clase[2]:^15}|{info_clase[1]:^15}|")
        print("-" * 85)
        contador += 1
        
    print()

def mostrar_fechas_cargadas(cupos_clase, id_clase):

    if len(cupos_clase) == 0:  # Verificar si hay alumnos
            print("No hay alumnos inscritos en esta clase aún.")
            return []

    print("-" * 37) 
    cont= 1
    fechas = []
    print(f"{'Opcion N°':^10}|{'Fecha':^25}|")
    print("-" * 37)

    modelo_fechas = leer_archivo(cupos_clase[0], "asistencia_alumnos")

    for fecha in  modelo_fechas[id_clase]: #Toma la lista de asistencias del primer alumno anotado a la clase
        print(f"{cont:^10}|{fecha[0]:^25}|")
        print("-" * 37)
        cont+= 1
        fechas.append(fecha[0]) #Guarda las fechas en una lista para despues validar que la opcion ingresada este entre las fechas cargadas
    
    return fechas #Retorna todas las fechas

def pasar_lista(clase_id): #cupos_clases,asistencias_alumnos, estudiantes

    cupos_clase = leer_archivo(clase_id, "cupos_clases")
    cantidad_fechas = mostrar_fechas_cargadas(cupos_clase, clase_id)
    
    if len(cantidad_fechas) == 0:
        return

    while True:
        try:

            opcion_num = int(input("Ingrese el N° correspondiente a la fecha a la cual desea pasar lista: "))
            opcion_num = validar_entre(opcion_num, 0, len(cantidad_fechas)) #Esto es igual al indice de la fecha en la lista + 1

        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero!")

        except KeyboardInterrupt:
            print()
            print(" Usa '0' para salir del menú.")
            continue

        else:
            break

    fecha_clase = cantidad_fechas[opcion_num - 1] #Toma la fecha seleccionada

    if opcion_num != 0:

        for id in cupos_clase: #Recorre los legajos de los alumnos anotados a la clase

            asistencia_alumno = leer_archivo(id, "asistencia_alumnos")

            estado_actual = asistencia_alumno[clase_id][opcion_num - 1][1] #Toma el estado actual del alumno en la fecha seleccionada

            if estado_actual == "No cargada": #Solo lo muestra si no le cargo asistencia anteriormente

                estudiante = leer_archivo(id, "estudiantes")

                print()
                print(f"Alumno: {estudiante['Nombre']} | Legajo N°: {estudiante['Legajo']}")
                
                estado = input("Ingrese 'P' (presente) o 'A' (ausente) o 'T' (tarde): ").title().strip()
                estado = validar_string(estado, ['P', 'A', 'T'])
                print()
                if estado == "P":

                    estado = "Presente"

                elif estado =="A":

                    estado="Ausente"
                
                else:
                    estado = "Tarde"

                escribir_archivo_log("asistencia", "MODIFICAR", {
                    "legajo": str(estudiante["Legajo"]),
                    "id_clase": clase_id,
                    "fecha": fecha_clase,
                    "estado": estado
                })

def mostrar_asistencia_clase(id_clase):

    cupos_clase = leer_archivo(clase_id, "cupos_clases")

    cantidad_fechas = mostrar_fechas_cargadas(cupos_clase, clase_id)

    if len(cantidad_fechas) == 0:
        return
    
    print()
    while True:
        try:
            opcion_num = int(input("Ingrese el N° correspondiente a la fecha a la cual desea pasar lista o 0 para volver al menú de profesor: "))
            opcion_num = validar_entre(opcion_num, 0, len(cantidad_fechas)) #Esto es igual al indice de la fecha en la lista + 1
        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero!")
        except KeyboardInterrupt:
            print()
            print(" Usa '0' para salir del menú.")
            continue
        else:
            break

    if opcion_num != 0:
        print()
        print("-" * 58)
        print(f"{'Legajo':^10}|{'Nombre':^30}|{'Estado':^15}|")
        print("-" * 58)

        for legajo in cupos_clase:

            datos_estudiante = leer_archivo(legajo, "estudiantes")
            asistencia_alumno = leer_archivo(legajo, "asistencia_alumnos")

            nombre = datos_estudiante["Nombre"]
            estado = asistencia_alumno[id_clase][opcion_num -1][1] #Toma el estado del alumno en la fecha seleccionada
            print(f"{legajo:^10}|{nombre:^30}|{estado:^15}|")
            print("-" * 58)
        print()

def mostrar_alumnos_clase(clase_id):

    '''
    
    '''
    cupos_clase = leer_archivo(clase_id, "cupos_clases") #Lista con los legajos de los alumnos anotados a la clase.

    cont = 1
    print("-" * 53)
    print(f"{'Opcion N°':^10}|{'Legajo':^10}|{'Nombre':^30}|")
    print("-" * 53)

    for legajo in cupos_clase: 

        datos_estudiante = leer_archivo(legajo, "estudiantes")

        nombre = datos_estudiante["Nombre"]

        print(f"{cont:^10}|{legajo:^10}|{nombre:^30}|")
        print("-" * 53)
        cont +=1

    return cupos_clase

def modificar_asistencia(legajo_mostrar, id_clase):
    
    estudiante = leer_archivo(legajo_mostrar, "estudiantes")
    nombre = estudiante["Nombre"]

    asistencia_alumno = leer_archivo(legajo_mostrar, "asistencia_alumnos")
    valor_diccionario = asistencia_alumno[id_clase]

    print(f"Modificando asistencia del alumno {nombre} | Legajo N°:{legajo_mostrar}")

    cupos_clase = leer_archivo(clase_id, "cupos_clases")
    cantidad_fechas = mostrar_fechas_cargadas(cupos_clase, clase_id)

    if len(cantidad_fechas) == 0:
        return

    print()
    while True:
        try:
            opcion_num = int(input("Ingrese el N° correspondiente a la fecha a la cual desea pasar lista o 0 para volver al menú de profesor: "))
            opcion_num = validar_entre(opcion_num, 0, len(cantidad_fechas)) #Esto es igual al indice de la fecha en la lista + 1

        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero!")

        except KeyboardInterrupt:
            print()
            print(" Usa '0' para salir del menú.")
            continue

        else:
            break

    while opcion_num !=0:

        fecha_clase = cantidad_fechas[opcion_num - 1] #Toma la fecha seleccionada
        
        nuevo_estado = input("Ingrese 'P' (presente), 'A' (ausente), 'T' (tarde) o '0' para salir: ").title().strip()
        nuevo_estado = validar_string(nuevo_estado, ['P', 'A', 'T', '0'])
        print()

        if nuevo_estado == "P":

            nuevo_estado = "Presente"
            
        elif nuevo_estado == "A":

            nuevo_estado="Ausente"
            
        elif nuevo_estado == "T":

            nuevo_estado = "Tarde"

        else:
            break
        while True:
            try:

                confirmacion = int(input(f"Confirma la modificacion? Nuevo estado: {nuevo_estado} \n 1- Si \n 2- No \n 0- Salir \n Ingrese la opcion: "))
                confirmacion= validar_entre(confirmacion,0,2)

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break

        valor_diccionario[opcion_num - 1] = [fecha_clase, nuevo_estado] #Actualiza la asistencia del alumno en la fecha selccionada
            
        if confirmacion == 1:


            escribir_archivo_log("asistencia", "MODIFICAR", {
                "legajo": str(legajo_mostrar),
                "id_clase": id_clase,
                "fecha": fecha_clase,
                "estado": nuevo_estado
            })

            print()
            print(f"Modicacion realizada con exito. Nuevo estado: {nuevo_estado}")
            break

        elif confirmacion == 2:
            continue

        else:
            break

        #PONER AUXILIAR REMPLAZO VER

def alta_alumno(nombre, materias_disponibles):
        
    legajos_historiocos = leer_archivo(0, "legajos_historicos")
    legajo_nuevo = legajos_historiocos[-1] + 1

    while True:

        try:


            contrasena = int(input("Ingrese una contraseña numerica de 4 digitos para el alumno: "))
            contrasena = validar_entre(contrasena, 1000, 9999)

        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero de 4 digitos!")
        
        except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue
        
        else:
            break    
    
    nuevo_legajo = {

        "Nombre" : nombre,
        "Contraseña": contrasena,
        "Clases Mañana" : [],
        "Clases Tarde" : [],
        "Clases Noche" : [],
        }
    
    materias_inscriptas = []
    cantidad_inscripto = (len(nuevo_legajo["Clases Mañana"]) + len(nuevo_legajo["Clases Tarde"]) + len(nuevo_legajo["Clases Noche"]))
    todas_clases_actuales = nuevo_legajo["Clases Mañana"] + nuevo_legajo["Clases Tarde"] + nuevo_legajo["Clases Noche"]
    
    while cantidad_inscripto < 15: #5 por turno. Actualmente es imposible porque hay 6 materias, pero en la realidad es posible, aunque poco probable

        
        if len(materias_disponibles) == len(materias_inscriptas):
            print("\nEl alumno ya está inscripto en todas las materias disponibles.")
            break

        print(f"\nMaterias inscriptas: {cantidad_inscripto}/15")

        nombres_materias = mostrar_nombres_materias(materias_disponibles)

        opciones_dispo = len(nombres_materias)
        while True:
            try:
                opcion_ingresada = int(input("Ingrese el N° corresponidiente a la materia a la cual quiere inscribir al alumno o 0 para salir: "))
                opcion_ingresada = validar_entre(opcion_ingresada, 0, opciones_dispo)

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break
        
        if opcion_ingresada == 0:
            break

        else:

            materia_elegida = nombres_materias[opcion_ingresada - 1]

            if materia_elegida in materias_inscriptas:
                print()
                print("Error! El alumno ya está inscripto en esta materia. Elija otra.")
                print()
                continue
        
            clases_dispo = id_segun_nombre_materia(materia_elegida, 1)

            if len(clases_dispo) == 0:
                print("Error! Esta materia no tiene clases con cupos disponibles. Intente con otra materia.")
                continue

            ids_dispo = mostrar_clases_dispo(clases_dispo, materia_elegida)
            opciones_dispo = len(ids_dispo)
            while True:
                try:
                    opcion_ingresada = int(input("Ingrese el N° correspondiente a la clase a la cual quiere iscribir al alumno o 0 para volver atras: "))
                    opcion_ingresada = validar_entre(opcion_ingresada, 0, opciones_dispo)

                except ValueError:
                    print("Error! El dato a ingresar debe ser un numero entero!")

                except KeyboardInterrupt:
                    print()
                    print(" Usa '0' para salir del menú.")
                    continue

                else:
                    break
                
            if opcion_ingresada == 0:

                continue

            id_elegido = ids_dispo[opcion_ingresada - 1]

            if cantidad_inscripto > 0:
            
                conflicto_id = validar_conflicto_horario(id_elegido, todas_clases_actuales)

                if conflicto_id:

                    info_clase_conflicto = leer_archivo(conflicto_id, "ids_clases")
                    info_clase_elegida = leer_archivo(id_elegido, "ids_clases")

                    print()
                    print("Error! El alumno ya tiene una clase en ese día y turno.")
                    print(f"Clase inscripta: ID {conflicto_id} - {info_clase_conflicto[0]} - {info_clase_conflicto[1]} - {info_clase_conflicto[2]}")
                    print(f"Clase seleccionada: ID {id_elegido} - {info_clase_elegida[0]} - {info_clase_elegida[1]} - {info_clase_elegida[2]}")
                    print()
                    continue
            
            confirmacion = input(f"Esta seguro de querer inscribir al alumno a la clase {id_elegido}? (S/N) ").title().strip()
            confirmacion = validar_string(confirmacion, ["S", "N"])

            if confirmacion == "S":

                info_clase_elegida = leer_archivo(id_elegido, "ids_clases")

                match info_clase_elegida[1]:

                    case "Turno Mañana":
                        nuevo_legajo["Clases Mañana"].append(id_elegido)
                
                    case "Turno Tarde":
                        nuevo_legajo["Clases Tarde"].append(id_elegido)

                    case "Turno Noche":
                        nuevo_legajo["Clases Noche"].append(id_elegido)
                
                materias_inscriptas.append(materia_elegida)
                todas_clases_actuales = nuevo_legajo["Clases Mañana"] + nuevo_legajo["Clases Tarde"] + nuevo_legajo["Clases Noche"]
                cantidad_inscripto = (len(nuevo_legajo["Clases Mañana"]) + len(nuevo_legajo["Clases Tarde"]) + len(nuevo_legajo["Clases Noche"]))

    if cantidad_inscripto >= 1:

        confirmacion = input(f"¿Confirma el ingreso del estudiante '{nombre}'? (S/N)").title().strip()
        confirmacion = validar_string(confirmacion, ["S", "N"])

        if confirmacion == "S":

            escribir_archivo_log("estudiantes", "AGREGAR", {
                "legajo": str(legajo_nuevo),
                "nombre": nombre,
                "Clases Mañana": nuevo_legajo["Clases Mañana"],
                "Clases Tarde": nuevo_legajo["Clases Tarde"],
                "Clases Noche": nuevo_legajo["Clases Noche"]
            })

            # Registrar la contraseña en el log usando la misma clave que espera el proceso
            # de aplicación de cambios ('contrasena' sin acento) y pasar el dict correctamente
            escribir_archivo_log("contrasena", "AGREGAR", {
                "legajo": str(legajo_nuevo),
                "contrasena": str(contrasena)
            })

            diccionario = {} #Diccionario para guardar las clases y las fechas con estado "No cargada"

            for id_clase in todas_clases_actuales:

                cupos_clase = leer_archivo(id_clase, "cupos_clases")
                
                legajo_referencia = cupos_clase[0] #Tomar alumno de referencia en la clase

                asistencias_alumno =leer_archivo(legajo_referencia, "asistencia_alumnos")
                fechas_existentes = asistencias_alumno[id_clase] #Lista con las fechas ya cargadas en la clase

                lista_fechas = [] #Lista para guardar las fechas con estado "No cargada"

                for fecha_estado in fechas_existentes: #Copiar cada fecha
                    fecha = fecha_estado[0]

                    lista_fechas.append([fecha, "No cargada"])

                diccionario[id_clase] = lista_fechas

            escribir_archivo_log("asistencia", "AGREGAR", {

                "legajo": str(legajo_nuevo),
                "asistencias": diccionario
            })

            escribir_archivo_log("cupos", "AGREGAR", {

                "legajo": str(legajo_nuevo),
                "clases": todas_clases_actuales
            })

            escribir_archivo_log("legajos", "AGREGAR",{
                "legajo": str(legajo_nuevo)
            } )

            print()
            print(f"Alumno '{nombre}' agregado correctamente con legajo {legajo_nuevo}.")
        
        else: 

            print("Cancelando operacion. Volviendo al menú...")
    
    else:
    
        print("Cancelando operacion ya que el alumno no fue inscripto a ninguna materia.")

def mostrar_nombres_materias(materias_disponibles, inicio=0, opcion=1):

    """
    Muestra las materias disponibles de forma recursiva.
    Caso base: cuando inicio >= len(materias_disponibles)
    Caso recursivo: imprime la materia actual y llama recursivamente con inicio+1
    """
    if inicio == 0:  # Primera llamada: imprimir encabezado
        print()
        print("-"*34)
        print(f"| N° |{'Materia':<28}|")
        print("-"*34)
   
    if inicio < len(materias_disponibles):  # Caso recursivo    #Lo que frena a la recusividad
        materia = materias_disponibles[inicio]
        print(f"|{opcion:>3}| {materia:<28}|")
        print("-"*34)
        mostrar_nombres_materias(materias_disponibles, inicio+1, opcion+1) #Llamada recursiva ,aumenta 1
   
    if inicio == 0:  # Al volver de la recursión, retornar el resultado
        return materias_disponibles #Retorna la lista de materias disponibles

def id_segun_nombre_materia(materia_elegida, uso):

    clases_materia = leer_archivo(materia_elegida, "ids_clases")
    clases = []

    for clase in clases_materia:
        
        cupos = leer_archivo(clase[0], "cupos_clases")

        if uso == 1:

            if len (cupos) < 13:

                clases.append(clase)

            else:
                continue

        else:

            clases.append(clase)

    return clases

def mostrar_clases_dispo(clases_dispo, nombre_materia):

    turnos = {
        "Turno Mañana": [],
        "Turno Tarde": [],
        "Turno Noche": []
    }
    
    for clase in clases_dispo:
        id_clase = clase[0]
        turno = clase[1]
        dia = clase[2]
        turnos[turno].append((id_clase, dia))
    
    max_clases = 0
    for turno in turnos:
        if len(turnos[turno]) > max_clases:
            max_clases = len(turnos[turno])

    print()
    print(f"{'=' * 88}")
    print(f"|{nombre_materia:^86}|")
    print(f"{'=' * 88}")
    print(f"|{'Turno Mañana':^28}|{'Turno Tarde':^28}|{'Turno Noche':^28}|")
    print(f"{'-' * 88}")
    print(f"|{'N°':^4}{'ID':^10}{'Día':^14}|{'N°':^4}{'ID':^10}{'Día':^14}|{'N°':^4}{'ID':^10}{'Día':^14}|")
    print(f"{'-' * 88}")

    opciones_ids = []
    contador = 1

    for i in range(max_clases):

        if i < len(turnos["Turno Mañana"]):
            id_clase, dia = turnos["Turno Mañana"][i]
            print(f"|{contador:^4}{id_clase:^10}{dia:^14}", end="|")
            opciones_ids.append(id_clase)
            contador += 1
        else:
            print(f"|{' ':^28}", end="|")                             

        if i < len(turnos["Turno Tarde"]):
            id_clase, dia = turnos["Turno Tarde"][i]
            print(f"{contador:^4}{id_clase:^10}{dia:^14}", end="|")
            opciones_ids.append(id_clase)
            contador += 1
        else:
            print(f"{' ':^28}", end="|")
        

        if i < len(turnos["Turno Noche"]):
            id_clase, dia = turnos["Turno Noche"][i]
            print(f"{contador:^4}{id_clase:^10}{dia:^14}", end="|")
            opciones_ids.append(id_clase)
            contador += 1

        else:
            print(f"{' ':^28}", end="|")
        
        print()
    print(f"{'-' * 88}")
    print()

    return opciones_ids

def validar_conflicto_horario(id_nueva_clase, clases_actuales):
    """
    Verifica si hay conflicto de horario entre la nueva clase y las clases actuales del alumno.
    Retorna el id de la clase en conflicto si HAY conflicto, False si NO hay conflicto.
    """
    
    info_clase_elegida = leer_archivo(id_nueva_clase, "ids_clases")

    
    dia_nueva = info_clase_elegida[2] #Dia de la nueva clase elegida
    turno_nueva = info_clase_elegida[1] #Turno de la nueva clase elegida
    
    for id_clase in clases_actuales:

        info_clase = leer_archivo(id_clase, "ids_clases")

        dia_actual = info_clase[2]
        turno_actual = info_clase[1]
        
        # Si coinciden el día Y el turno = HAY CONFLICTO
        if dia_nueva == dia_actual and turno_nueva == turno_actual:
            return id_clase
    
    return False

def baja_de_alumno():

    while True:
        try:
            legajo=int(input("Ingrese el legajo del alumno que desea eliminar o 0 para volver al menú de administrador:"))
            print()

        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero!")

        except KeyboardInterrupt:
            print()
            print(" Usa '0' para salir del menú.")
            continue

        else:
            break
    
    legajos_actuales = leer_archivo(0, "legajos_actuales")
    
    while legajo not in legajos_actuales and legajo != 0:
        print("Error!El legajo ingresado no existe!")
        while True:
            try:
                legajo=int(input("Intente nuevamente o 0 para volver al menú de administrador: "))

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break
    
    if legajo != 0:

        info_estudiante = leer_archivo(legajo,"estudiantes")
        confirmacion = (input(f"Confirmda que desea eliminar al alumno {info_estudiante['Nombre']} con legajo N° {legajo} ? (S/N) ")).title().strip()
        confirmacion = validar_string(confirmacion,["S", "N"])

        if confirmacion == "S":

            materias_inscriptas = info_estudiante["Clases Mañana"] + info_estudiante["Clases Tarde"] + info_estudiante["Clases Noche"]

            for id_clase in materias_inscriptas:

                pass
                escribir_archivo_log("cupos", "BORRAR", {
                    "legajo": str(legajo),
                    "id_clase": id_clase
                })

            escribir_archivo_log("estudiantes", "BORRAR", {
                "legajo": str(legajo)
            })

            escribir_archivo_log("asistencia","BORRAR",{
                "legajo":str(legajo)
            })
            
            escribir_archivo_log("legajos", "BORRAR", {
                "legajo": str(legajo)
            })


            escribir_archivo_log("contrasena","BORRAR",{
                "legajo":str(legajo)
            })

            print()
            print("Alumno eliminado con exito!")

        else:
            print()
            print("Operacion cancelada, volviendo al menú...")

    else:
        print()
        print("Operacion cancelada, volviendo al menú...")

def mostrar_todas_clases(ids_clases):

    contador = 1
    clases = []

    print(f"|{'N°':^3}|{'Materia':^30}|{'ID':^8}|{'Turno':^15}|{'Dia':^15}|")
    print("-"*81)

    for clase in ids_clases:
        print(f"{contador:^3}|{ids_clases[clase][0]:^30}|{clase:^8}|{ids_clases[clase][1]:^15}|{ids_clases[clase][2]:^15}|")
        print("-"*81)

def mostrar_todos_alumnos(estudiantes):
    

    contador = 1
    legajos = []

    print(f"|{'N°':^3}|{'Legajo':^8}|{'Nombre':^30}|")
    print("-" * 46)

    for alumno in estudiantes:
        print(f"|{contador:^3}|{alumno:^8}|{estudiantes[alumno]['Nombre']:^30}|")
        print("-" * 46)
        legajos.append(alumno)
        contador += 1

    return legajos

def busqueda_alumno(lista, buscar):

    resultados = []

    for legajo in lista:

        if buscar.isdigit():

            if legajo == buscar:
                resultados.append(legajo)
            
        else:

            datos_estudiante = leer_archivo(legajo, "estudiantes")
            nombre = datos_estudiante["Nombre"]
            
            if nombre == buscar:
                resultados.append(legajo)
                    
            
    if len(resultados) == 0:
        return False
    
    elif len(resultados) > 1:

        contador = 1
        print("Resultados:")
        print()
        print("-"*42)
        print(f"|{'N°':^3}|{'LU N°':^6}|{'Nombre':^30}|")
        print("-"*42)
        for legajo in resultados:

            datos_estudiante = leer_archivo(legajo, "estudiantes")
            nombre = datos_estudiante["Nombre"]

            print(f"|{contador:^3}|{legajo:^6}|{nombre:^30}|")
            print("-"*42)
            contador += 1
        while True:
            try:
                opcion = int(input("Ingrese el numero del alumno o 0 para salir: "))
                opcion = validar_entre(opcion, 0, len(resultados))

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break
        if opcion != 0:
            legajo = resultados[opcion - 1]
        
        else: 
            legajo = opcion

    else:
        legajo = resultados[0]
    
    return legajo

def modificacion_alumno(id_alumno, nombre_actual, info_estudiante):
    
    while True:

        print()
        print("¿Que desea modificar? \n 1- Nombre y apellido \n 2- Inscripcion \n 0- Salir")
        while True:
            try:

                accion = int(input(""))
                accion = validar_entre(accion,0, 2)

            except ValueError:
                print("Error! El dato a ingresar debe ser un numero entero!")

            except KeyboardInterrupt:
                print()
                print(" Usa '0' para salir del menú.")
                continue

            else:
                break

        if accion == 0:
            break

        elif accion == 1:
            
            nuevo_nombre = input("Ingrese el nombre del nuevo estudiante o 0 para salir: ").title().strip()

            while validar_nuevo_nombre(nuevo_nombre) == False and nuevo_nombre != "0":
                print("El nombre no puede contener numeros.")
                nuevo_nombre = input("Intentelo nuevamente o 0 para salir: ")

            if nuevo_nombre == "0":
                continue

            nuevo_apellido = input("Ingrese el apellido del nuevo estudiante o 0 para salir: ").title().strip()

            while validar_nuevo_nombre(nuevo_apellido) == False and nuevo_apellido != "0":
                print("El nombre no puede contener numeros.")
                nuevo_apellido = input("Intentelo nuevamente o 0 para salir: ")

            if nuevo_apellido == "0":
                continue

            nuevo_nombre_completo =nuevo_nombre + " " + nuevo_apellido

            while nuevo_nombre_completo == nombre_actual:

                print()
                print("El nuevo nombre no puede ser igual al actual.")
                nuevo_nombre = input("Ingrese el nombre del nuevo estudiante o 0 para salir: ").title().strip()

                while validar_nuevo_nombre(nuevo_nombre) == False and nuevo_nombre != "0":
                    print("El nombre no puede contener numeros.")
                    nuevo_nombre = input("Intentelo nuevamente o 0 para salir: ")

                if nuevo_nombre == "0":
                    continue

                nuevo_apellido = input("Ingrese el apellido del nuevo estudiante o 0 para salir: ").title().strip()

                while validar_nuevo_nombre(nuevo_apellido) == False and nuevo_apellido != "0":
                    print("El nombre no puede contener numeros.")
                    nuevo_apellido = input("Intentelo nuevamente o 0 para salir: ")

                if nuevo_apellido == "0":
                    continue

                nuevo_nombre_completo =nuevo_nombre + " " + nuevo_apellido  

            confirmacion = input(f"Esta seguro de querer modificar el nombre de {nombre_actual} a {nuevo_nombre}? (S/N)").title().strip()
            confirmacion = validar_string(confirmacion, ["S", "N"])

            if confirmacion == "N":
                print("Cancelando modificacion...")
                continue

            escribir_archivo_log("estudiantes","MODIFICAR", {
                "legajo": str(id_alumno),
                "nombre": nuevo_nombre_completo
            })
            
            print(f"Cambio de nombre exitoso.")

        else:

            print()
            print("¿Que desea realizar? \n 1- Inscribir a una nueva clase \n 2- Darse de baja de una clase \n 0- Salir")
            while True:
                try:

                    accion = int(input(""))
                    accion = validar_entre(accion, 0, 2)

                except ValueError:
                    print("Error! El dato a ingresar debe ser un numero entero!")

                except KeyboardInterrupt:
                    print()
                    print(" Usa '0' para salir del menú.")
                    continue

                else:
                    break
            if accion == 0:
                continue

            elif accion == 1:


                materias_inscriptas = info_estudiante["Clases Mañana"] + info_estudiante["Clases Tarde"] + info_estudiante["Clases Noche"]
                cantidad_inscripto = len(materias_inscriptas)

                while cantidad_inscripto < 15: 

                    nombres_materias = mostrar_nombres_materias(materias_disponibles)

                    opciones_dispo = len(nombres_materias)
                    while True:
                        try:
                            opcion_ingresada = int(input("Ingrese el N° corresponidiente a la materia a la cual quiere inscribir al alumno o 0 para volver al menu de modificacion: "))
                            opcion_ingresada = validar_entre(opcion_ingresada, 0, opciones_dispo)

                        except ValueError:
                            print("Error! El dato a ingresar debe ser un numero entero!")

                        except KeyboardInterrupt:
                            print()
                            print(" Usa '0' para salir del menú.")
                            continue

                        else:
                            break
                    
                    if opcion_ingresada == 0:
                        break

                    else:

                        materia_elegida = nombres_materias[opcion_ingresada - 1]

                        ya_inscripto = False
                        for id_clase in materias_inscriptas:

                            info_clase = leer_archivo(id_clase, "ids_clases")

                            if info_clase[0] == materia_elegida:  # Comparar nombres de materia
                                ya_inscripto = True
                                break

                        if ya_inscripto:
                            print()
                            print("Error! El alumno ya está inscripto en esta materia. Elija otra.")
                            print()
                            continue
                    
                        clases_dispo = id_segun_nombre_materia(materia_elegida, 1)

                        if len(clases_dispo) == 0:
                            print("Error! Esta materia no tiene clases con cupos disponibles. Intente con otra materia.")
                            continue

                        ids_dispo = mostrar_clases_dispo(clases_dispo, materia_elegida)
                        opciones_dispo = len(ids_dispo)
                        while  True:
                            try:

                                opcion_ingresada = int(input("Ingrese el N° correspondiente a la clase a la cual quiere iscribir al alumno o 0 para volver atras: "))
                                opcion_ingresada = validar_entre(opcion_ingresada, 0, opciones_dispo)

                            except ValueError:
                                print("Error! El dato a ingresar debe ser un numero entero!")

                            except KeyboardInterrupt:
                                print()
                                print(" Usa '0' para salir del menú.")
                                continue

                            else:
                                break

                        if opcion_ingresada == 0:

                            continue

                        id_elegido = ids_dispo[opcion_ingresada - 1]
                        info_clase_elegida = leer_archivo(id_elegido, "ids_clases")

                        if cantidad_inscripto > 0:
                        
                            conflicto_id = validar_conflicto_horario(id_elegido, materias_inscriptas)
                            if conflicto_id:

                                info_clase_conflicto = leer_archivo(conflicto_id, "ids_clases")                               
                                
                                print()
                                print("Error! El alumno ya tiene una clase en ese día y turno.")
                                print(f"Clase inscripta: ID {conflicto_id} - {info_clase_conflicto[0]} - {info_clase_conflicto[1]} - {info_clase_conflicto[2]}")
                                print(f"Clase seleccionada: ID {id_elegido} - {info_clase_elegida[0]} - {info_clase_elegida[1]} - {info_clase_elegida[2]}")
                                print()
                                continue

                        confirmacion = input(f"Esta seguro de querer inscribir al alumno a la clase{id_elegido}? (S/N)").title().strip()
                        confirmacion = validar_string(confirmacion, ["S", "N"])

                        if confirmacion == "S":
                                
                            match info_clase_elegida[1]:
    
                                case "Turno Mañana":
                                    escribir_archivo_log("estudiantes", "MODIFICAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Mañana": id_elegido,
                                    })
                                                                
                                case "Turno Tarde":
                                    escribir_archivo_log("estudiantes", "MODIFICAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Tarde": id_elegido,
                                    })

                                case "Turno Noche":
                                    escribir_archivo_log("estudiantes", "MODIFICAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Noche": id_elegido,
                                    })

                            materias_inscriptas.append(id_elegido)
                            cantidad_inscripto += 1

                            escribir_archivo_log("cupos", "AGREGAR", {
                                legajo: str(id_alumno),
                                "id_clase": id_elegido
                            })

                            cupo_clase_elegida = leer_archivo(id_elegido, "cupos_clases")

                            if len(cupo_clase_elegida) > 1:

                                legajo_referencia = cupo_clase_elegida[0] #Tomar alumno de referencia en la clase
                                diccionario = {} #Diccionario para guardar la clase y las fechas con estado "No cargada"
                                asistencia_referencia = leer_archivo(legajo_referencia, "asistencia_alumnos")
                                fechas_existentes = asistencia_referencia[id_elegido] #Obtener fechas existentes
                                
                                lista_fechas = [] #Lista para guardar las fechas con estado "No cargada"

                                for fecha_estado in fechas_existentes: #Copiar cada fecha

                                    fecha = fecha_estado[0]
                                    lista_fechas.append([fecha, "No cargada"])
                                
                                diccionario[id_elegido] = lista_fechas
                                escribir_archivo_log("asistencia", "AGREGAR", {
                                    "legajo": str(id_alumno),
                                    "asistencias": diccionario
                                })

                                print(f"Se inscribio correctamente al alumno a la clase {id_elegido}")
                            
                            else: 

                                print("Advertencia: No hay fechas cargadas aún para esta clase.")

            else:
                while True:

                    materias_inscriptas = info_estudiante["Clases Mañana"] + info_estudiante["Clases Tarde"] + info_estudiante["Clases Noche"]
                    cantidad_inscripto = len(materias_inscriptas)

                    if cantidad_inscripto == 0:
                        print("El alumno no esta incripto en ninguna materia.")
                        break

                    clases = mostrar_clases_anotadas(id_alumno)
                    while True:
                        try:

                            opcion = int(input("Ingrese el N° corresponddiente a la materia la cual quiere dar de baja al alumno o 0 para salir: "))
                            opcion = validar_entre(opcion, 0, len(clases))

                        except ValueError:
                            print("Error! El dato a ingresar debe ser un numero entero!")

                        except KeyboardInterrupt:
                            print()
                            print(" Usa '0' para salir del menú.")
                            continue
                        
                        else:
                            break
                    
                    if opcion == 0:
                        break

                    else:
                        
                        opcion_elegida = clases[opcion -1]
                        info_clase_elegida = leer_archivo(opcion_elegida, "ids_clases")

                        confirmacion = input(f"¿Esta seguro de querer dar de baja al alumno de la materia {info_clase_elegida[0]} - {info_clase_elegida[1]} - {info_clase_elegida[2]}? (S/N)").title().strip()
                        confirmacion = validar_string(confirmacion, ["S", "N"])

                        if confirmacion == "S":

                            match info_clase_elegida[1]:

                                case "Turno Mañana":
                                    
                                    info_estudiante["Clases Mañana"].remove(opcion_elegida)
                                    escribir_archivo_log("estudiantes", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Mañana": info_estudiante["Clases Mañana"]
                                    })

                                    escribir_archivo_log("asistencia", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "id_clase": opcion_elegida
                                    })
                                
                                    escribir_archivo_log("cupos","BORRAR",{
                                        "legajo":str(id_alumno),
                                        "id_clase" : opcion_elegida
                                    })
                                    
                                case "Turno Tarde":
                                    info_estudiante["Clases Tarde"].remove(opcion_elegida)
                                    escribir_archivo_log("estudiantes", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Tarde": info_estudiante["Clases Tarde"]
                                    })

                                    escribir_archivo_log("asistencia", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "id_clase": opcion_elegida
                                    })
                                
                                    escribir_archivo_log("cupos","BORRAR",{
                                        "legajo":str(id_alumno),
                                        "id_clase" : opcion_elegida
                                    })
                            
                                case "Turno Noche":
                                    info_estudiante["Clases Noche"].remove(opcion_elegida)
                                    escribir_archivo_log("estudiantes", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "Clases Noche": info_estudiante["Clases Noche"]
                                    })

                                    escribir_archivo_log("asistencia", "BORRAR", {
                                        "legajo": str(id_alumno),
                                        "id_clase": opcion_elegida
                                    })
                                
                                    escribir_archivo_log("cupos","BORRAR",{
                                        "legajo":str(id_alumno),
                                        "id_clase" : opcion_elegida
                                    })

                            print("Baja realizada con exito.")
                            
                        else:
                            print("Operacion cancelada, cargando materias disponibles...")

def leer_archivo(parametro_buscar, diccionario, uso=None):
    """
    Carga el archivo correspondiente y devuelve el registro que coincide con el
    parámetro de búsqueda para ese archivo. No verifica contraseña.
    """
    archivo = None  # Inicializamos la variable para el archivo
    try:

        if diccionario == "estudiantes":
        
            registro = []
            archivo = open("estudiantes.csv", "r", encoding="utf-8")

            for linea in archivo: # Dividir la línea en campos

                datos = linea.strip().split(",")
                parametro_buscar = str(parametro_buscar)

                if uso == None:

                    if datos[0] == parametro_buscar:
                        registro = {
                            "Legajo": int(datos[0]),
                            "Nombre": datos[1],
                            "Clases Mañana": datos[2].split(";") if datos[2] else [],
                            "Clases Tarde": datos[3].split(";") if datos[3] else [],
                            "Clases Noche": datos[4].split(";") if datos[4] else [],
                        }
                        break  #Devolver el estudiante encontrado
                else:

                    registro.append(int(datos[0])) #Devolver lista de legajos 
      
        elif diccionario == "administradores":  #JSON

            archivo = open("admin.json", "r", encoding="utf-8")
            dic_administradores = json.load(archivo)
            
            registro = dic_administradores[parametro_buscar]
                
        elif diccionario == "ids_clases":

            registro = False
            archivo = open("ids_clases.json", "r", encoding="utf-8")
            ids_clases = json.load(archivo)
            parametro_buscar = str(parametro_buscar)

            if parametro_buscar.isdigit():
                
                for id in ids_clases:
                    if id == parametro_buscar:
                        registro = ids_clases[id]
                        break
                    else:
                        continue
            
            else:
                ids = list(ids_clases.keys())
                registro = []
                
                for id in ids:

                    if len(registro) == 6:      #cantidad clases max
                        break

                    if ids_clases[id][0] == parametro_buscar:
                        registro.append([id, ids_clases[id][1], ids_clases[id][2]])
                    
                    else:
                        continue    

        elif diccionario == "cupos_clases":

            registro = False
            archivo = open("cupos_clases.csv", "r", encoding="utf-8")

            for linea in archivo: # Dividir la línea en campos

                datos = linea.strip().split(",")
                parametro_buscar = str(parametro_buscar)

                if datos[0] == str(parametro_buscar):
                    registro = datos[1].split(";") #devolver solo los legajos de la clase
                    break
                else:
                    continue


        elif diccionario == "asistencia_alumnos":
            
            registro = False
            archivo = open("asistencia_alumnos.txt", "r", encoding="utf-8")
            
            for linea in archivo:
                datos = json.loads(linea.strip())  # Cada línea es un JSON
                parametro_buscar = str(parametro_buscar)
                
                if parametro_buscar in datos:  # parametro_buscar es el legajo
                    registro = datos[parametro_buscar]
                    archivo.close()
                    break         

                else:
                    continue

        elif diccionario == "profesores":
        
            registro = False
            archivo = open("profesores.csv", "r", encoding="utf-8")

            for linea in archivo: # Dividir la línea en campos

                datos = linea.strip().split(",")
                parametro_buscar = str(parametro_buscar)

                if datos[0] == parametro_buscar:
                    registro = {
                        "Usuario": datos[0],
                        "Nombre": datos[1],
                        "Clases": datos[2].split(";") if datos[2] else [],  #retorna lista vacia
                    }
                    break  # Devolver el estudiante encontrado

                else:
                    continue

        elif diccionario == "legajos_historicos" or diccionario == "legajos_actuales":

            archivo = open("legajos.json", "r", encoding="utf-8")
            datos = json.load(archivo)  # Carga todo el JSON como diccionario
            
            # Retorna la lista completa según el diccionario solicitado
            registro = datos[diccionario]
                        
        else:
            print("Diccionario no reconocido.")
            return None

    except FileNotFoundError:
        print(f"Error: El archivo '{diccionario}' no existe.")
        return None

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    
    else:

        if registro == False:

            print("No hubo resultados en la busqueda.")
        
        else: 
            archivo.close()
            return registro
        
    return None

def escribir_archivo_log(diccionario, tipo_accion, datos):

    if diccionario == "asistencia":
        archivo = open("cambios_asistencia.txt", "a", encoding="utf-8")

    elif diccionario == "cupos":
        archivo= open("cambios_cupos.txt", "a", encoding="utf-8")

    elif diccionario == "estudiantes":
        archivo = open("cambios_estudiantes.txt", "a", encoding="utf-8")

    elif diccionario == "legajos":
        archivo = open("cambios_legajos.txt", "a", encoding="utf-8")

    elif diccionario == "contrasena":
        archivo = open("cambios_contrasena.txt", "a", encoding="utf-8")

    else:
        print("Diccionario no reconocido.")
        return None

    # Crear el registro del cambio
    cambio = {
        "accion": tipo_accion,       #que se hizo
        "datos": datos                 #datos que se  modificaron
    } 
    
    # Escribir en el archivo (JSON Lines, como asistencia_alumnos.txt)
    archivo.write(json.dumps(cambio, ensure_ascii=False) + "\n")  #Permite que tildes se guarden correctamente
    archivo.close()  #Guarda todo y cierra el archivo

def aplicar_cambios_asistencia():
    """Lee el log y aplica cambios al archivo de asistencia procesando línea por línea."""
    
    try:
        archivo_original = open("asistencia_alumnos.txt", "r", encoding="utf-8")  #Original
        archivo_temporal = open("asistencia_temp.txt", "w", encoding="utf-8")       #temporal
        
        # Procesar cada línea del archivo original
        linea_original = archivo_original.readline()
        while linea_original:     #Mientras tenga contenido
            datos_orig = json.loads(linea_original.strip())            # Cargar línea como JSON sacando espacios
            eliminar = False

            # Buscar cambios para esta asistencia
            archivo_log = open("cambios_asistencia.txt", "r", encoding="utf-8")     #Ver cambios pendientes
            linea_log = archivo_log.readline()        #Leer línea por línea de archivo de log buscando cambios que apliquen a ese alumno
            agregados_realizados = []                   #Lista de legajos agregados
            
            while linea_log:  #si queda algo

                cambio = json.loads(linea_log.strip())
                
                if cambio["accion"] == "MODIFICAR":

                    legajo_str = str(cambio["datos"]["legajo"])      #Extrae el legajo de cambio y pasa str
                    
                    if legajo_str in datos_orig:                    #verifica si existe en los datos actuales
                        # Modificar estado de asistencia
                        id_clase = cambio["datos"]["id_clase"]      #busca la clase especifica dentro de las asistencias del alumno
                        
                        # Buscar la fecha específica en la lista de asistencias
                        for fecha_estado in datos_orig[legajo_str][id_clase]:         #busca la fecha especificia en la lista de asistencias de esa clase
                            
                            if fecha_estado[0] == cambio["datos"]["fecha"]:
                                fecha_estado[1] = cambio["datos"]["estado"] # Modificar el estado
                
                elif cambio["accion"] == "AGREGAR": 

                    if cambio["datos"]["legajo"] in datos_orig: # Si el legajo ya existe, solo agregar la nueva clase con sus asistencias
                        
                        legajo_existente = str(cambio["datos"]["legajo"])
                        datos_orig[legajo_existente][cambio["datos"]["id_clase"]] = cambio["datos"]["asistencias"] # Agrega la nueva clase con sus asistencias
                        agregados_realizados.append(legajo_existente)     #Se agrega para no volver a agregarlo despues 
                    
                elif cambio["accion"] == "BORRAR":

                    if not "Clases Mañana" in cambio["datos"] and not "Clases Tarde" in cambio["datos"] and not "Clases Noche" in cambio["datos"]:
                        # Eliminar solo una clase específica
                        legajo_str = str(cambio["datos"]["legajo"])    #Extrae el legajo de cambio y pasa str
                        
                        if legajo_str in datos_orig:                   #verifica si existe en los datos actuales
                            id_clase = cambio["datos"]["id_clase"]     #busca la clase especifica dentro de las asistencias del alumno
                            datos_orig[legajo_str].pop(id_clase)  # Elimina la clase específica
                            
                    else:
                        # Eliminar el legajo completo
                        eliminar = True #Al eliminar por completo no lo escribe en el archivo temporal
                        break
                
                linea_log = archivo_log.readline()
            
            archivo_log.close()

            if not eliminar:  # Si no se eliminó, escribir en archivo temporal
                archivo_temporal.write(json.dumps(datos_orig, ensure_ascii=False) + "\n") #Reconoce acentos y caracteres especiales
            
            linea_original = archivo_original.readline()  # Leer siguiente línea del archivo original
        
        archivo_log = open("cambios_asistencia.txt", "r", encoding="utf-8")   # Procesar agregados que no estaban en el archivo original
        linea_log = archivo_log.readline()  

        while linea_log:    
            cambio = json.loads(linea_log.strip())     

            if cambio["accion"] == "AGREGAR":   #Agregar legajos nuevos

                legajo_nuevo = str(cambio["datos"]["legajo"])

                if legajo_nuevo in agregados_realizados:  #Si el legajo ya fue agregado, saltar
                    linea_log = archivo_log.readline() 
                    continue

                linea_completa = {legajo_nuevo  : cambio["datos"]["asistencias"]}      #Cear nueva linea completa para agregar con legajo y asistencias
                archivo_temporal.write(json.dumps(linea_completa, ensure_ascii=False) + "\n") #Reconoce acentos y caracteres especiales
            linea_log = archivo_log.readline()

        archivo_original.close()
        archivo_temporal.close()

        # Reemplazar el archivo original con el temporal
        os.replace("asistencia_temp.txt", "asistencia_alumnos.txt")    #Eliminar el archivo de cambios Y renombra el temporal como el original
        archivo = open("cambios_asistencia.txt", "w", encoding="utf-8")   #
        archivo.close()
        
        
    except FileNotFoundError:
        print("Error: Archivo no encontrado")
        return

    except json.JSONDecodeError as e:
        print(f"❌ Error en línea: {linea_original[:100]}...")  # Solo mostrar primeros 100 chars
        print(f"Error JSON: {e}")

def aplicar_cambios_cupos():

    try:
        archivo_original = open("cupos_clases.csv", "r", encoding="utf-8")    #Abre archvios orignal y temporal
        archivo_temporal = open("cupos_temp.csv", "w", encoding="utf-8")


        linea_original = archivo_original.readline()      # Procesar cada línea del archivo original
        while linea_original: 
            datos = linea_original.strip().split(",")  # Dividir la línea en campos  dato[0] =id clase dato[1]= legajos
            id_clase = datos[0]
            eliminar = False
            
        
            # Buscar cambios para este cupo
            archivo_log = open("cambios_cupos.txt", "r", encoding="utf-8")   #Ver cambios pendientes
            linea_log = archivo_log.readline()     #Leer línea por línea de archivo de log buscando cambios que apliquen a ese cupo
            
            while linea_log:
                cambio = json.loads(linea_log.strip())   #Convierte linea a un diccionario de python segun agregar o eliminar
                
                if cambio["accion"] == "AGREGAR":
                    
                    if id_clase in cambio["datos"]["clases"]:   
                        datos_cupos = datos[1].split(";") if datos[1] else [] #Hace otro split para trabajar con legajos individuales                               
                                                                                #=["100","101","102"]
                        if str(cambio["datos"]["legajo"]) not in datos_cupos:
                            datos_cupos.append(str(cambio["datos"]["legajo"]))   #Si la clase ya esta(siempre esta) y legajo no, se agrega
                            datos[1] = ";".join(datos_cupos)
                
                elif cambio["accion"] == "BORRAR":

                    if id_clase in cambio["datos"]["clases"]:                       #Si la clase del cupo coincide con la del cambio
                        datos_cupos = datos[1].split(";") if datos[1] else []

                        if str(cambio["datos"]["legajo"]) in datos_cupos:
                            datos_cupos.remove(str(cambio["datos"]["legajo"])) #Marcás la línea para eliminar (eliminar = True) 
                                                                                #y cortás el bucle del log, de modo que esa clase no se escribe en el archivo temporal.
                            datos[1] = ";".join(datos_cupos)                
                            eliminar = True
                            break
                    
                linea_log = archivo_log.readline()
                                        
            archivo_log.close()

            if not eliminar:        
                archivo_temporal.write(",".join(datos) + "\n")
        
            linea_original = archivo_original.readline()      #Si la clase no fue marcada para elimianr se vuelve a escrbir en csv
        
        archivo_original.close()
        archivo_temporal.close()

        # Reemplazar el archivo original con el temporal
        os.replace("cupos_temp.csv", "cupos_clases.csv")
        archivo = open("cambios_cupos.txt", "w", encoding="utf-8")
        archivo.close()
        
    except FileNotFoundError:
        print("Error: Archivo no encontrado")
        return

def aplicar_cambios_legajos():

    try:
        archivo_original = open("legajos.json", "r", encoding="utf-8")
        archivo_temporal = open("legajos_temp.json", "w", encoding="utf-8")    #Abre archvios orignal y temporal

        # Procesar cada línea del archivo original     
        diccionario_legajos = json.load(archivo_original)              #Cargar todo el JSON como diccionario
        legajos_historicos = diccionario_legajos["legajos_historicos"]     
        legajos_actuales = diccionario_legajos["legajos_actuales"]     #Extrae las listas de legajos
 
        archivo_original.close()

        # Buscar cambios para este legajo
        archivo_log = open("cambios_legajos.txt", "r", encoding="utf-8")
        linea_log = archivo_log.readline()
         
        while linea_log:         # Abre el archivo de log y procesa línea por línea
            cambio = json.loads(linea_log.strip())
            
            if cambio["accion"] == "BORRAR":
                if cambio["datos"]["legajo"] in legajos_actuales:
                    legajos_actuales.remove(cambio["datos"]["legajo"])  #Eliminar legajo de actuales
            
            elif cambio["accion"] == "AGREGAR":
                if cambio["datos"]["legajo"] not in legajos_actuales:
                    legajos_actuales.append(int(cambio["datos"]["legajo"])) #Agregar legajo a actuales
                
                if cambio["datos"]["legajo"] not in legajos_historicos:
                    legajos_historicos.append(int(cambio["datos"]["legajo"]))  #Agregar legajo a historicos
            
            linea_log = archivo_log.readline()
    
        archivo_log.close()

        #Crear nuevo diccionario
        nuevo_diccionario = {
            "legajos_historicos": legajos_historicos,
            "legajos_actuales": legajos_actuales
        }
        
        archivo_temporal.write(json.dumps(nuevo_diccionario, ensure_ascii=False) + "\n")     #Rescribe el nuevo diccionario para guardar en temporal
        archivo_temporal.close()

        # Reemplazar el archivo original con el temporal       
        os.replace("legajos_temp.json", "legajos.json")                       #Remplaza y cierra
        archivo = open("cambios_legajos.txt", "w", encoding="utf-8")
        archivo.close()

    except FileNotFoundError:
        print("Error: Archivo no encontrado")
        return

    except Exception as e:
        print(f"Error inesperado al aplicar cambios en legajos: {e}")
        return        

def aplicar_cambios_estudiantes():

    try:
        archivo_original = open("estudiantes.csv", "r", encoding="utf-8")
        archivo_temporal = open("estudiantes_temp.csv", "w", encoding="utf-8")      #Abris archivos orignal y temporal
 
        linea_original = archivo_original.readline()      # Procesar cada línea del archivo original
      
        print(f"DEBUG: Iniciando procesamiento de estudiantes existentes")

        while linea_original:       # Leer cada línea del archivo original
            
            
            datos = linea_original.strip().split(",")       #Saca legajo,nombre y clases
            legajo_actual = datos[0]

            eliminar = False

            archivo_log = open("cambios_estudiantes.txt", "r", encoding="utf-8")
            linea_log = archivo_log.readline()             #Ve si hay cambios pendientes
 
            while linea_log:     #Si hay cambios
                cambio = json.loads(linea_log.strip())

                if cambio["accion"] == "ELIMINAR":
                    if str(cambio["datos"]["legajo"]) == legajo_actual:     #No se escribe en el archivo temporal
                        eliminar = True
                        break

                elif cambio["accion"] == "MODIFICAR":
                    if str(cambio["datos"]["legajo"]) == legajo_actual:
                        # Modificar los datos según lo especificado
                        if "nombre" in cambio["datos"]:
                            datos[1] = cambio["datos"]["nombre"]
                        
                        if "Clases Mañana" in cambio["datos"]:
                            datos[2] = ";".join(cambio["datos"]["Clases Mañana"])
                        
                        if "Clases Tarde" in cambio["datos"]:
                            datos[3] = ";".join(cambio["datos"]["Clases Tarde"])
                        
                        if "Clases Noche" in cambio["datos"]:
                            datos[4] = ";".join(cambio["datos"]["Clases Noche"])
                    
                else: #Si la accion es agregar
                    pass
            
                linea_log = archivo_log.readline()

            archivo_log.close()

            # Escribir línea si no está eliminada
            if not eliminar:    #Alumnos vigentes
                archivo_temporal.write(",".join(datos) + "\n")
            
            linea_original = archivo_original.readline()
        archivo_original.close()

        archivo_log = open("cambios_estudiantes.txt", "r", encoding="utf-8")
        linea_log = archivo_log.readline()

        while linea_log:          #Una vez terminado el procesamiento original,recorre devuelta el log para agregar nuevos alumnos
            cambio = json.loads(linea_log.strip())  #Recorre aca porque los agregados no estaban en el archivo original

            if cambio["accion"] == "AGREGAR":
                datos = cambio["datos"]
                clases_manana = ';'.join(datos['Clases Mañana']) if datos['Clases Mañana'] else ""
                clases_tarde = ';'.join(datos['Clases Tarde']) if datos['Clases Tarde'] else ""
                clases_noche = ';'.join(datos['Clases Noche']) if datos['Clases Noche'] else ","
                linea_nueva = f"{datos['legajo']},{datos['nombre']},{clases_manana},{clases_tarde},{clases_noche}"
                archivo_temporal.write(linea_nueva + "\n")     #Escribe la nueva linea en el archivo temporal

            linea_log = archivo_log.readline()
        
        archivo_log.close()
        archivo_original.close()
        archivo_temporal.close()

        # Reemplazar el archivo original con el temporal
        os.replace("estudiantes_temp.csv", "estudiantes.csv")
        #Borrar cotnenido del log
        archivo = open("cambios_estudiantes.txt", "w", encoding="utf-8")
        archivo.close()
        
    except FileNotFoundError:
        print("Error:Archivo no encontrado")
        return

def aplica_cambios_contrasenas():

    try:
        archivo_original = open("contrasena.json", "r", encoding="utf-8")
        archivo_temporal = open("contrasena_temp.json", "w", encoding="utf-8")  #Abre los archivos original y temporal

        # Procesar cada línea del archivo original
                    
        diccionario_legajos = json.load(archivo_original)        #Convierte a diccionario de python
        archivo_original.close()

        # Buscar cambios para este legajo
        archivo_log = open("cambios_contrasena.txt", "r", encoding="utf-8")      #Abre archivo de log

        linea_log = archivo_log.readline()      #Recorre linea por linea el archivo de log
        while linea_log:

            cambio = json.loads(linea_log.strip())

            if cambio["accion"] == "BORRAR":
                if cambio["datos"]["legajo"] in diccionario_legajos:
                    diccionario_legajos.pop(cambio["datos"]["legajo"])      #Elimina la clave correspondiente del diccionario
                    
            elif cambio["accion"] == "AGREGAR":
                diccionario_legajos[cambio["datos"]["legajo"]] = cambio["datos"]["contrasena"]    #El legajo se agrega(o actualiza)con la nueva contraseña
             
            linea_log = archivo_log.readline() 
        
        archivo_log.close()
        archivo_temporal.write(json.dumps(diccionario_legajos, ensure_ascii=False) + "\n")
        archivo_temporal.close()

        # Reemplazar el archivo original con el temporal
        os.replace("contrasena_temp.json", "contrasena.json")
        #Borrar cotnenido del log
        archivo = open("cambios_contrasena.txt", "w", encoding="utf-8")
        archivo.close()


    except FileNotFoundError:
        print("Error:Archivo no encontrado")
        return

def comparar_archivos():
    
    print()
    print("Aplicando cambios en asistencias...")
    aplicar_cambios_asistencia()
    print("Cambios aplicados con exito.")
    print()
    
    print("Aplicando cambios en cupos de clases...")
    aplicar_cambios_cupos() 
    print("Cambios aplicados con exito.")
    print()

    print("Aplicando cambios en legajos...")
    aplicar_cambios_legajos()  
    print("Cambios aplicados con exito.")
    print()

    print("Aplicando cambios en contraseñas...")
    aplica_cambios_contrasenas()
    print("Cambios aplicados con exito.")
    print()

    print("Aplicando cambios en estudiantes...")
    aplicar_cambios_estudiantes()  
    print("Cambios aplicados con exito.")
    print()

#Listas-------------------------------------------------------------------------------------------------------------

materias_disponibles = ["Matematica Discreta", "Testing de apps",
                        "Sistemas Operativos", "Marketing",
                        "Sistemas de info II", "Programacion II"]

#Anotaciones---------------------------
'''
Cosas 2da entrega:
-Modificar cambiar al alumno de curso Agregar sin modificar las asistencias? O que sea borrarlo y agregarlo a la misma materia pero distinta clase.

1- Modificacion:
    a- Carga
    b- Alta y baja
    c- Pasar lista
2-Agregar leer archivo a legajos historicos y actuales
3- Agregar escritura de archivos
'''
#Main----------------------------------------------------------

while True:
    
    menu_inicial()

    while True:

        try:    
            opcion = int(input("Ingrese una opcion: "))
            opcion = validar_entre(opcion, 1,3)

        except ValueError:
            print("Error! El dato a ingresar debe ser un numero entero!")
        
        except KeyboardInterrupt:
            print()
            print(" Usa '0' para salir del menú.")
            continue

        except Exception as error:
            print(f"Error inesperado: {error}")
            
        else:
            break

    if opcion == 1: #Estudiante
        
        legajo, contrasena = menu_login(0)
        legajo = str(legajo)

        while True:
            try:

                while validacion_log_in(legajo, contrasena) == False and legajo != "0" and contrasena != "0":

                    print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                    legajo, contrasena = menu_login(0)
            
            except ValueError:
                print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                legajo, contrasena = menu_login(0)

            except KeyboardInterrupt:
                print()
                print("Usa '0' para salir del menú.")
            
            except Exception as error:
                print(f"Error inesperado: {error}")

            else:
                break
        
        if legajo == "0" or contrasena == "0":
            continue

        datos_estudiante = leer_archivo(legajo, "estudiantes")

        nombre = datos_estudiante["Nombre"]

        print(f"Inicio de sesion correcto, bienvenido/a {nombre}")

        while validacion_log_in(legajo, contrasena):

            menu_estudiante()
            while True:
                
                try:

                    accion = int(input("Ingrese una opcion o 0 para salir: "))
                    accion = validar_entre(accion, 0,3)

                except ValueError:
                    print("Error! El dato a ingresar debe ser un numero entero!")

                except KeyboardInterrupt:
                    print()
                    print("Usa '0' para salir del menú.")
                    continue
                
                except Exception as error:
                    print(f"Error inesperado: {error}")
                
                else:
                    break
            
            if accion == 0:
                break

            if accion == 1: #Ver asistencia de todas
                print()
                mostrar_asistencia_todas(legajo)           

            else: #Ver asistencia de una materia
                
                print("Materias a las que estas anotado: ")
                clases_anotadas = mostrar_clases_anotadas(datos_estudiante)

                while True:
                
                    try:
        
                        id_clase = int(input("Ingrese el N° correspondiente a clase a la que desee ver asistencia o 0 para volver al de estudiante: "))
                        print()
                        id_clase = validar_entre(id_clase,0, len(clases_anotadas))
                    
                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")
                    
                    except Exception as error:
                        print(f"Error inesperado: {error}")
                        
                    else:

                        break

                if id_clase == 0:
                    continue

                id_clase = clases_anotadas[id_clase - 1] #Toma el id de la clase seleccionada
                mostrar_asistencia_simple(nombre, id_clase, legajo)
    
    if opcion == 2: #Profesor
        
        usuario, contrasena = menu_login(1)

        while True:

            try:

                while validacion_log_in(usuario, contrasena) == False and usuario != "0" and contrasena != "0":
                    print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                    usuario, contrasena = menu_login(1)
            
            except ValueError:
                print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                usuario, contrasena = menu_login(1)
            
            except KeyboardInterrupt:
                print()
                print("Ingrese '0' para salir del  menu.")
                continue

            except Exception as error:
                print(f"Error inesperado: {error}")

            else:
                break

        if usuario == "0" or contrasena == "0":
            continue

        datos_profesor = leer_archivo(usuario, "profesores")
        
        nombre = datos_profesor["Nombre"]

        print(f"Inicio de sesion correcto. Bienvenido {nombre}")

        while validacion_log_in(usuario, contrasena):

            menu_profesor()
            while True:
                
                try:
                        
                    accion = int(input("Ingrese una opcion o 0 para salir: "))
                    accion = validar_entre(accion,0,6)
                
                except ValueError:
                    print("Error! El dato a ingresar debe ser un numero entero!")
                
                except KeyboardInterrupt:
                    print()
                    print(" Usa '0' para salir del menú.")
                    continue
                
                except Exception as error:
                    print(f"Error inesperado: {error}")
                
                else:
                    break

            if accion == 0:
                break

            elif accion == 1: #Pasar lista

                clases_asignadas = datos_profesor["Clases"]

                mostrar_clases_asignadas(clases_asignadas)

                while True:

                    try:

                        clase_id= int(input("Ingrese el N° correspondiente a clase a la que desea pasar lista o 0 para volver al menú de profesor: "))           
                        clase_id = validar_entre(clase_id, 0, len(clases_asignadas))
                    
                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")
                    
                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue
                    
                    except Exception as error:
                        print(f"Error inesperado: {error}")
                
                    else:

                        break

                if clase_id == 0:
                    continue
                    
                clase_id = clases_asignadas[clase_id - 1] #Toma el id de la clase seleccionada
                print()
                pasar_lista(clase_id) 
                
            elif accion ==2 : #Ver asistencia de una clase
                
                clases_asignadas = datos_profesor["Clases"]

                mostrar_clases_asignadas(clases_asignadas)

                while True:
                    try:


                        clase_id= int(input("Ingrese el N° correspondiente a clase a la que desea pasar lista o 0 para volver al menú de profesor: "))           
                        clase_id = validar_entre(clase_id, 0, len(clases_asignadas))

                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")
                    
                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue
                    
                    except Exception as error:
                        print(f"Error inesperado: {error}")

                    else:
                        break

                if clase_id == 0:
                    continue
                    
                clase_id = clases_asignadas[clase_id - 1] #Toma el id de la clase seleccionada
                print()

                mostrar_asistencia_clase(clase_id)

            elif accion == 3: #Ver asistencia de un alumno

                clases_asignadas = datos_profesor["Clases"]

                mostrar_clases_asignadas(clases_asignadas)

                while True:

                    try:

                        clase_id= int(input("Ingrese el N° correspondiente a clase del alumno que quiere ver su asistencia o 0 para volver al menú de profesor: "))           
                        clase_id = validar_entre(clase_id, 0, len(clases_asignadas))
                    
                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")
                    
                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue
                        
                    except Exception as error:
                        print(f"Error inesperado: {error}")
                
                    else:

                        break

                if clase_id == 0:
                    continue
                    
                clase_id = clases_asignadas[clase_id - 1] 
                print()
                estudiantes_inscriptos = mostrar_alumnos_clase(clase_id)

                if len(estudiantes_inscriptos) == 0:

                    print("No hay estudiantes anotados a esta clase. Volviendo al menu...")
                    continue

                while True:
                
                    opcion = input("Ingrese el N° correspondiente, el legajo o nombre del alumno a buscar o 0 para salir: ").strip()
                    cupos_clase = leer_archivo(clase_id, "cupos_clases")
                
                    if opcion == "0":
                        break
                    
                    elif opcion.isdigit():

                        if int(opcion) > 0 and int(opcion) <= len(estudiantes_inscriptos):
                            legajo_mostrar = estudiantes_inscriptos[int(opcion) - 1]

                        elif int(opcion) > 100:

                            
                            legajo_mostrar = busqueda_alumno(cupos_clase, opcion)

                            if legajo_mostrar == 0:
                                break #Vuelve al menu de profesor

                        else:
                            legajo_mostrar = False
                    
                    else:

                        try:

                            opcion = int(opcion)
                            legajo_mostrar = False

                        except ValueError: #Validar que no sea un numero negativo

                            opcion = opcion.title()

                            legajo_mostrar = busqueda_alumno(cupos_clase, opcion)

                            if legajo_mostrar == 0:
                                break #Vuelve al menu de profesor
                    
                    if legajo_mostrar == False:
                        print("Error! Intente nuevamente.")
                        continue
                        
                    elif legajo_mostrar == 0 or opcion == "0":
                        break

                    datos_estudiante = leer_archivo(legajo_mostrar, "estudiantes")
                    nombre = datos_estudiante["Nombre"]

                    print()
                    mostrar_asistencia_simple(nombre, clase_id, legajo_mostrar)
                    break
                
            elif accion == 4: #Modificar asistencia

                clases_asignadas = datos_profesor["Clases"]
                mostrar_clases_asignadas(clases_asignadas) 
                
                while  True:
                    try:

                        clase_id= int(input("Ingrese el N° correspondiente a clase del alumno que quiere modificar su asistencia o 0 para volver al menú de profesor: "))           
                        clase_id = validar_entre(clase_id, 0, len(clases_asignadas))

                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")
                    
                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue

                    except Exception as error:
                        print(f"Error inesperado: {error}")

                    else:
                        break

                if clase_id == 0:
                    continue
                    
                clase_id = clases_asignadas[clase_id - 1] 
                print()
                estudiantes_inscriptos = mostrar_alumnos_clase(clase_id)

                if len(estudiantes_inscriptos) == 0:

                    print("No hay estudiantes anotados a esta clase. Volviendo al menu...")
                    continue

                while True:

                    opcion = input("Ingrese el N° correspondiente, el legajo o nombre del alumno a buscar o 0 para salir: ").strip()
                    cupos_clase = leer_archivo(clase_id, "cupos_clases")

                    if opcion == "0":
                        break
                    
                    elif opcion.isdigit():

                        if int(opcion) > 0 and int(opcion) <= len(estudiantes_inscriptos): #Opcion esta entre 1 y la cantidad de estudiantes inscriptos
                            legajo_mostrar = estudiantes_inscriptos[int(opcion) - 1]

                        elif int(opcion) > 100:

                            legajo_mostrar = busqueda_alumno(cupos_clase, opcion)

                            if legajo_mostrar == 0:
                                break #Vuelve al menu de profesor

                        else:
                            legajo_mostrar = False

                    else:

                        try:

                            opcion = int(opcion)
                            legajo_mostrar = False

                        except ValueError: #Validar que no sea un numero negativo

                            opcion = opcion.title()

                            legajo_mostrar = busqueda_alumno(cupos_clase, opcion)

                            if legajo_mostrar == 0:
                                break #Vuelve al menu de profesor
                    
                    if legajo_mostrar == False:
                        print("Error! Intente nuevamente.")
                        continue
                        
                    elif legajo_mostrar == 0 or opcion == "0":
                        break

                    print()
                    modificar_asistencia(legajo_mostrar, clase_id)
                    break

            else: #Ver clases asignadas

                clases_asignadas = datos_profesor["Clases"]
                mostrar_clases_asignadas(clases_asignadas)
                print()
            
    if opcion == 3: #Administrador

        usuario, contrasena = menu_login(1)

        while True:

            try:
                
                while validacion_log_in(usuario, contrasena) == False and usuario != "0" and contrasena != "0":
                    print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                    usuario, contrasena = menu_login(1)
            
            except ValueError:
                print("Usuario y/o contraseña incorrectos. Intente nuevamente")
                usuario, contrasena = menu_login(1)
            
            except KeyboardInterrupt:
                print()
                print("Ingrese '0' para salir del  menu.")
                continue

            except Exception as error:
                print(f"Error inesperado: {error}")

            else:
                break
        
        if usuario == "0" or contrasena == "0":
            continue
        
        datos_administrador = leer_archivo(usuario, "administradores") 

        nombre = datos_administrador

        print(f"Inicio de sesion correcto. Bienvenido {nombre}")
        
        while validacion_log_in(usuario, contrasena):

            menu_administrador()

            while True:
                try:

                    accion = int(input("Ingrese una opcion o 0 para salir: "))
                    accion = validar_entre(accion,0,5)
                except ValueError:
                    print("Error! El dato a ingresar debe ser un numero entero!")
                    
                except KeyboardInterrupt:
                    print()
                    print(" Usa '0' para salir del menú.")
                    continue

                except Exception as error:
                    print(f"Error inesperado: {error}")

                else:
                    break

            if accion == 0:
                break

            elif accion == 1: #Alta alumno
                
                nuevo_nombre = input("Ingrese el nombre del nuevo estudiante: ").title().strip()

                while validar_nuevo_nombre(nuevo_nombre) == False and nuevo_nombre != "0":
                    print("El nombre no puede contener numeros.")
                    nuevo_nombre = input("Intentelo nuevamente o 0 para salir: ")

                if nuevo_nombre == "0":
                    continue

                nuevo_apellido = input("Ingrese el apellido del nuevo estudiante: ").title().strip()

                while validar_nuevo_nombre(nuevo_apellido) == False and nuevo_apellido != "0":
                    print("El nombre no puede contener numeros.")
                    nuevo_apellido = input("Intentelo nuevamente o 0 para salir: ")

                if nuevo_apellido == "0":
                    continue

                nuevo_nombre_completo =nuevo_nombre + " " + nuevo_apellido
                alta_alumno(nuevo_nombre, materias_disponibles)
                
            elif accion == 2: #Baja alumno

                baja_de_alumno()

            elif accion == 3: #Modificar alumno 
            
                alumno = input("Ingrese el nombre o el legajo del alumno a modificar o 0 para salir: ").title().strip()

                if alumno == "0":
                    continue

                lista_legajos = leer_archivo(0, "estudiantes", 1)
                id = busqueda_alumno(lista_legajos, alumno)

                if id == 0:
                    continue
                
                while id == False:
                    print()
                    print("Alumno o Legajo no encontrado...")
                    alumno = input("Intente nuevamente o 0 para salir: ").title().strip()
                    id = busqueda_alumno(lista_legajos, alumno)

                info_estudiante = leer_archivo(id, "estudiantes")
                nombre = info_estudiante["Nombre"]

                print()
                print(f"Ingresando a la modificacion del alumno {nombre}")
                modificacion_alumno(id, nombre,info_estudiante)

            elif accion == 4: #Ver asistencia por curso

                nombres_materias = mostrar_nombres_materias(materias_disponibles)
                while True:
                    try:
                        opcion = int(input("Ingrese el N° correspondiente a la materia a la cual quiere acceder o 0 para volver al menú de administrador: "))
                        opcion = validar_entre(opcion, 0, len(nombres_materias))

                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")

                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue

                    except Exception as error:
                        print(f"Error inesperado: {error}")

                    else:
                        break

                if opcion == 0:
                    print("Volviendo al menú...")
                    continue

                materia_elegida = nombres_materias[opcion - 1]
                clases_mostrar = id_segun_nombre_materia( materia_elegida, 0)

                ids_mostrar = mostrar_clases_dispo(clases_mostrar, materia_elegida)
                opciones_dispo = len(ids_mostrar)
                while True:
                    try:
                        opcion = int(input("Ingrese el N° correspondiente a la clase a la cual quiere iscribir al alumno o 0 para volver al menú de administrador: "))
                        opcion = validar_entre(opcion, 0, opciones_dispo)

                    except ValueError:
                        print("Error! El dato a ingresar debe ser un numero entero!")

                    except KeyboardInterrupt:
                        print()
                        print(" Usa '0' para salir del menú.")
                        continue

                    except Exception as error:
                        print(f"Error inesperado: {error}")

                    else:
                        break
                if opcion == 0:

                    print("Volviendo al menú...")
                    continue

                id_elegido = ids_mostrar[opcion - 1]
                mostrar_asistencia_clase(id_elegido)
            
            else: #REINICIAR 

                print("Reiniciando el sistema y aplicando cambios...")
                comparar_archivos()

                print("Apagando sistema...")
                print()
                print()
                print("Iniciando sistema...")
                print()
                print("Cargando datos...")
                print("Datos cargados con exito.")
                print("Sistema listo para usarse.")
                break





    
