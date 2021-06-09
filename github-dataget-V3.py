###############################################################################################
##########  Herramienta elaborada para obtener datos de repositorios en Github  ###############
##########  con fines didacticos, para el curso de paradigmas de programación   ###############
##########                                                                      ###############
##########                Autor: Sebastián Orellana Verdejo                     ###############
##########                            Version 3.0                               ###############
###############################################################################################
# 
# 
# Librerías utilizadas                 
from github import Github # para conectarse a la API de  Github
import datetime
import pandas as pd       # para trabajar con documentos excel


# Función que obtiene las fechas de commits de una lista de commits #
def obtenerFechasCommits(listaCommits, largo):
    #for ci in listaCommits:
        #print(ci.commit.author.date)
    fechaInicio = 0
    fechaTermino = 0
    i = 0
    for c in listaCommits:
        if(i == 0):
            if(c.commit.author.date.hour == 0):
                fecha1 = c.commit.author.date - datetime.timedelta(days=1)
            else:
                fecha1 = c.commit.author.date
            fechaTermino = str(fecha1.day)+"/"+ str(fecha1.month) +"/"+ str(fecha1.year)

        if(i == largo-1):
            if(c.commit.author.date.hour == 0):
                fecha2 = c.commit.author.date - datetime.timedelta(days=1)
            else:
                fecha2 = c.commit.author.date
            fechaInicio = str(fecha2.day)+"/"+ str(fecha2.month) +"/"+ str(fecha2.year)
                
        i += 1
    
    return fechaInicio, fechaTermino


# Función que obtiene el n° maximo de commits diarios de una lista de commits #
def obtenerMaxCommitsDiarios(listaCommits):
    fechaActual = datetime.date(2020,1,1)
    maxCount = 1
    count = 0
    for c in listaCommits:
        if(c.commit.author.date.hour == 0):
            fechaRecalculada = c.commit.author.date - datetime.timedelta(days=1)
        else:
            fechaRecalculada = c.commit.author.date
        y = fechaRecalculada.year
        m = fechaRecalculada.month
        d = fechaRecalculada.day
        fecha = datetime.date(y, m, d)
        if(fechaActual == fecha):
            count += 1
        else:
            fechaActual = fecha
            if(count > maxCount):
                maxCount = count
            count = 1
    return maxCount


# Función que obtiene todos los datos requeridos de los repositorios (llama a otra funciones) #
def obtenerEstadisticas(repo):
    datos = []
    estudiante = repo.owner
    nombreRepo = repo.name

    try:
        listaCommits = repo.get_commits()
        maxCommits = listaCommits.totalCount
        fechaInicio, fechaTermino = obtenerFechasCommits(listaCommits, maxCommits)
        maxCommitsDiarios = obtenerMaxCommitsDiarios(listaCommits)
        datos.append(repo.owner.login)
        datos.append(repo.name)
        datos.append(fechaInicio)
        datos.append(fechaTermino)
        datos.append(maxCommits)
        datos.append(maxCommitsDiarios)
        return datos

    except:
        print("No se pudo acceder a un repositorio")
        return ["repo_malo"]


# main #
usuario = "paradigmasdiinf"
contrasena = 'paradigmasbot2019'
g = Github(login_or_token="0e485cfd5ce54f231c16b4953ec008fd24475e94")

estudiantes = []
repos = []
finicio = []
ffin = []
maxCommits = []
maxCommitsDiarios = []

fecha = input("¿Hasta que FECHA se desean recuperar los repositorios?\nFormato fecha: 2021/03/29\n")
año = int(fecha[0:4])
mes = int(fecha[5:7])
dia = int(fecha[8:])
### Establecer fecha limite para recuperar repos
fechaLimite = datetime.datetime(año, mes, dia)

# Aceptar invitaciones pendientes
while(g.get_user().get_invitations().totalCount > 0):       #Mientras hayan invitaciones 
    lista_paginada = g.get_user().get_invitations()         #Se obtiene la lista de invitaciones
    print("Aceptanci invitaciones pendientes...")                
    for invitacion in lista_paginada:
        g.get_user().accept_invitation(invitacion.id)                      

# Recuperar repositorios
repositorios = g.get_user().get_repos(sort="created", direction="desc")

# Recuperar datos
for repo in repositorios:
    if repo.created_at >= fechaLimite:
        print("fecha de creación del repo: "+str(repo.created_at))
        data = obtenerEstadisticas(repo)   #Se obtienen los datos del repo
        print(data)
        if data[0] != "repo_malo":
            estudiantes.append(data[0])
            repos.append(data[1])
            finicio.append(data[2])
            ffin.append(data[3])
            maxCommits.append(data[4])
            maxCommitsDiarios.append(data[5])
    else:
        break

"""
while(g.get_user().get_invitations().totalCount > 0):       #Mientras hayan invitaciones 
    lista_paginada = g.get_user().get_invitations()         #Se obtiene la lista de invitaciones
    print("Obteniendo invitaciones...")
    print("Obteniendo datos...")                 
    for invitacion in lista_paginada:                       #Para cada invitacion 
        data = obtenerEstadisticas(invitacion.repository)   #Se obtienen los datos del repo
        print(data)
        if data[0] != "repo_malo":
            estudiantes.append(data[0])
            repos.append(data[1])
            finicio.append(data[2])
            ffin.append(data[3])
            maxCommits.append(data[4])
            maxCommitsDiarios.append(data[5])
        g.get_user().accept_invitation(invitacion.id)       #Se acepta la invitacion del repo
"""

# Se crea un diccionario con los datos #
dataExcel = {
    'Estudiante': estudiantes,
    'Repositorio': repos,
    'fecha inicio': finicio,
    'fecha fin': ffin,
    'Max Commits': maxCommits,
    'Max Commits Diarios': maxCommitsDiarios
}

# Se crea el excel con los datos obtenidos
excel = pd.DataFrame(dataExcel, columns = ['Estudiante', 'Repositorio', 'fecha inicio', 'fecha fin', 'Max Commits', 'Max Commits Diarios'])
excel.to_excel('github_data_paradigmas.xlsx', sheet_name='github_data')
print("¡Terminado Satisfactoriamente!")

####################################################################################################################################