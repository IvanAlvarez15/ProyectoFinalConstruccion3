from contextvars import Context
from itertools import count
import json
from multiprocessing import context
import string
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Historial, User
from random import randrange
#Librerias para web
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import sqlite3
from .models import Historial
#from .forms import CambiarPassword
from django.contrib.auth.views import LogoutView 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Count, Max, Min, Avg
import hashlib as hb
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt #excepcion POST
import ast #para diccionario
import json
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from datetime import datetime
import random
# from django.contrib.auth.hashers import check_password, is_password_usable
#Condigo de Unity
def create_endpoint(user):
    username = user.username
    status = user.status
    api_create = {"username" : username, "status" : status}
    final = json.dumps(api_create)
    return final
def extractRequest(credentials):
    credentials = credentials.split('&')
    print(credentials)
    user = credentials[0].replace("username=","")
    hshpass = credentials[1].replace("hshpass=","")
    return user, hshpass

#Vistas de la página web
# def index(response):
#     return HttpResponse("<h1>Hello</h1>")
def Comojugar(request):#Ya quedo
    return render(request, 'users/how-to-play.html', {})

def index(request):#Ya quedo
    return render(request, 'users/index.html', {})

def registrarse(request): # Ya quedo y tiene mensajes de errores para cada situación posible
    if request.user.is_authenticated:
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        maxi = Historial.objects.filter(Nombre_usuario="LoboSalvaje").order_by('-Puntos_por_partida') [0:1] #Ya se muestran los primeros 5 datos
        #timer= Historial.objects.all().aggregate('Tiempo_jugado')
        # data = Historial.objects.all()
        total_sum = 0
        # for item in data:
        #     total_sum += item.Tiempo_jugado
        tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
        tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))
        context = {
            'data': data, #Si sirve y funciona bien
            'maxi': maxi,
            'timer':total_sum,
            'timer_min': tmer_min['Tiempo_jugado__min'], 
            'timer_max':tmer_max['Tiempo_jugado__max']
        }
        return render(request, 'users/stadistics-personal.html',context)
    elif request.method == 'POST':
        usuario = request.POST['usuario']
        Contra = request.POST['Contraseña']
        try:
            user_check = User.objects.get(username=usuario)
            user_check.is_superuser = True
            user_check.is_active = True
            user_check.is_staff = True
            user_check.save()
            Confirmacion = authenticate(request, username = usuario, password = Contra)
            if Confirmacion is not None:
                login(request, Confirmacion)
                user_check.is_superuser = False
                #user_check.is_active = False
                user_check.is_staff = False
                user_check.save()
                return redirect('index')
            else:
                messages.error(request, ("La contraseña o el usuario podrían estar incorrectos, ingreselos nuevamente"))
                return redirect('Registrarse')
        except User.DoesNotExist:
            messages.error(request, ("El usuario no existe, pruebe creando uno"))
            return redirect('Registrarse')
    else:
        return render(request, 'users/log-in.html', {})

def ourteam(request): #Esta lista
    return render(request, 'users/our-team.html', {})

def ingresar(request): # Ya quedo
    if request.user.is_authenticated:
        #return render(request, 'users/log-in.html', {})
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        maxi = Historial.objects.filter(Nombre_usuario="LoboSalvaje").order_by('-Puntos_por_partida') [0:1] #Ya se muestran los primeros 5 datos
        #timer= Historial.objects.all().aggregate('Tiempo_jugado')
        # data = Historial.objects.all()
        total_sum = 0
        # for item in data:
        #     total_sum += item.Tiempo_jugado
        tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
        tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))

        context = {
            'data': data, #Si sirve y funciona bien
            'maxi': maxi,
            'timer':total_sum,
            'timer_min': tmer_min['Tiempo_jugado__min'], 
            'timer_max':tmer_max['Tiempo_jugado__max']
        }

        return render(request, 'users/stadistics-personal.html',context)
    elif request.method == 'POST': #CREATE
        usuario = request.POST['Usuario'] #LoboSalvaje
        nombre = request.POST['nombre'] #Nombre real de la persona
        Fecha = request.POST['Fecha'] #Fecha de nacimiento
        Contra = request.POST['Contra'] #Contraseña
        mail = request.POST['mail'] #Email
        Apellido1 = request.POST['Apellido'] #Apellido paterno
        Gender = request.POST['Gender'] #Genero de la persona
        Pais = request.POST['Pais'] #Pais de origen o de estancia
        numero = request.POST['Numero'] #Numero de cel
        User.objects.create_user(username = usuario,email= mail,password=Contra, first_name=nombre, last_name=Apellido1, country=Pais, birthday=Fecha, gender=Gender, phone=numero) #Crea el usuario en la BD de user en django
        return redirect('Estadisticas_personales') #Redirige a la página de estadisticas personales
    else:
        return render(request, 'users/sign-in.html', {})

def estadisticasglobales(request):
    data = Historial.objects.order_by('-Puntos_por_partida')[:5] #Ya se muestran los primeros 5 datos
    maxi = Historial.objects.order_by('-Puntos_por_partida')[0:1] #Ya se muestran los primeros 5 datos
    #timer= Historial.objects.all().aggregate('Tiempo_jugado')
    s = Historial.objects.all()
    total_sum = 0
    for item in s:
        total_sum += item.Tiempo_jugado
    total_sum = total_sum/60
    total_sum = round(total_sum)
    tmer_min = Historial.objects.all().aggregate(Min('Tiempo_jugado'))
    tmer_max = Historial.objects.all().aggregate(Max('Tiempo_jugado'))
    
    #print(len(data))
    #print(tmer_min['Tiempo_jugado__max']) #Muestar el dato correcto
    context = {
        'data': data,
        'maxi': maxi,
        'timer':total_sum,
        'timer_min': round(tmer_min['Tiempo_jugado__min']/60), 
        'timer_max':round(tmer_max['Tiempo_jugado__max']/60)
    }
    #Dashboard
    h_var = 'Points per game'
    v_var = 'Time played in minutes'
    data = [[h_var,v_var]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json = dumps(h_var)
    v_var_json = dumps(v_var)
    # datos_json = dumps(data)

    mydb = sqlite3.connect("db.sqlite3")
    cur = mydb.cursor()
    stringSQL = '''SELECT Puntos_por_partida, Tiempo_jugado FROM users_Historial ORDER BY Puntos_por_partida DESC'''
    rows = cur.execute(stringSQL)
    listasalida = []
    for i in rows:
        d = {}
        d['puntos'] = i[0]
        d['tiempo'] = i[1]
        data.append([i[0],i[1]/60]) #Necesita dos numeros
    datos_json = dumps(data)
    #Grafica 2
    h_var2 = 'Country'
    v_var2 = 'Popularity'
    data2 = [[h_var2,v_var2]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json2 = dumps(h_var2)
    v_var_json2 = dumps(v_var2)
    # datos_json = dumps(data)
    mydb2 = sqlite3.connect("db.sqlite3")
    cur2 = mydb2.cursor()
    stringSQL2 = ''' SELECT DISTINCT country FROM users_user'''
    rows2 = cur2.execute(stringSQL2)
    
    
    for i in rows2:
        r = {}
        r['paises'] = i[0]

        mydb22 = sqlite3.connect("db.sqlite3")
        cur22 = mydb22.cursor()
        cur22.execute ("SELECT COUNT(country) FROM users_user WHERE country = ?" , [i[0]])
        rows22 = cur22.fetchall()
        print(rows22[0])#Imprime bien

        #r['repeticiones'] = i[1]
        data2.append([i[0],rows22[0][0]]) #Necesita dos numeros
    datos_json2 = dumps(data2)
    print(datos_json2)

    #Grafica 3
    h_var3 = 'ID of the level'
    v_var3 = 'Time of play in minutes'
    data3 = [[h_var3,v_var3]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json3 = dumps(h_var3)
    v_var_json3 = dumps(v_var3)
    # datos_json = dumps(data)
    mydb3 = sqlite3.connect("db.sqlite3")
    cur3 = mydb3.cursor()
    stringSQL3 = ''' SELECT Tiempo_jugado, ID_Canciones  FROM users_Historial'''
    rows3 = cur3.execute(stringSQL3)
    for i in rows3:
        rr = {}
        rr['tiempo'] = i[0]
        rr['id'] = i[1]
        data3.append([i[1],i[0]/60]) #Necesita tres numeros

    datos_json3 = dumps(data3)


    #Grafica 4
    h_var4 = 'Points per game'
    v_var4 = 'User name'
    data4 = [[h_var4,v_var4]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json4 = dumps(h_var4)
    v_var_json4 = dumps(v_var4)
    # datos_json = dumps(data)

    mydb4 = sqlite3.connect("db.sqlite3")
    cur4 = mydb4.cursor()
    stringSQL4 = '''SELECT Puntos_por_partida ,Nombre_usuario FROM users_Historial ORDER BY Puntos_por_partida DESC LIMIT 5'''
    rows4 = cur4.execute(stringSQL4)
    listasalida4 = []
    
    for i in rows4:
        #print(i)
        d = {}
        d['puntos'] = i[0]
        d['user'] = i[1]
        data4.append([i[1],i[0]]) #Necesita dos numeros
    #print(data4)
    datos_json4 = dumps(data4)
    #datos_json4 = data4
    #print(datos_json4)

    #Grafica 5
    h_var5 = 'Levels reached'
    v_var5 = 'ID user'
    data5 = [[h_var5,v_var5]]
    # for i in range(0,11):
    #     data.append([randrange(101),randrange(101)])
    h_var_json5 = dumps(h_var5)
    v_var_json5 = dumps(v_var5)
    # datos_json = dumps(data)

    mydb5 = sqlite3.connect("db.sqlite3")
    cur5 = mydb5.cursor()
    stringSQL5 = '''SELECT ID_Canciones ,ID_usuario FROM users_Historial ORDER BY Tiempo_jugado DESC'''
    rows5 = cur5.execute(stringSQL5)
    listasalida5 = []
    for i in rows5:
        d = {}
        d['puntos'] = i[0]
        d['tiempo'] = i[1]
        data5.append([i[0],i[1]]) #Necesita dos numeros
    datos_json5 = dumps(data5)
    print(datos_json5)



    return render(request, 'users/stadistics-global.html', {'values':datos_json,'h_title':h_var_json,'v_title':v_var_json
                                                 ,'values2':datos_json2,'h_title2':h_var_json2,'v_title2':v_var_json2,
                                                 'values3':datos_json3,'h_title3':h_var_json3,'v_title3':v_var_json3 , 'contexto': context
                                                 ,'values4':datos_json4,'h_title4':h_var_json4,'v_title4':v_var_json4
                                                 ,'values5':datos_json5,'h_title5':h_var_json5,'v_title5':v_var_json5 })

def estadisticaspersonales(request): 
    if request.user.is_authenticated:
        
        data = Historial.objects.order_by('-Puntos_por_partida') #Ya se muestran los primeros 5 datos
        context = {
            'data': data, #Si sirve y funciona bien
        }
        return render(request, 'users/stadistics-personal.html',context)
    else:
        return render(request, 'users/index.html', {})

def logout_user(request):#Ya quedo
    logout(request)
    #messages.success(request, ('Logged out'))
    return redirect('index')

def Borrar(request, id):#Ya quedo
    if request.user.is_authenticated and request.method == 'POST':
        #temp_user = User.objects.get(Numero_usuario = id)
        #temp_user.delete()
        #success_url = reverse_lazy('index')
        temp_user2 = User.objects.get(id = id)
        temp_user2.delete()
        return render(request, 'users/index.html',{})
    elif request.user.is_authenticated:
        temp_user = User.objects.get(id = id)
        return render(request, 'users/Borrar.html', {"user":temp_user})
    else:
        return render(request, 'users/index.html', {})

def Sobrejuego(request):
    return render(request, 'users/about-game.html', {})

def Cambiarcontra(request, id): #Ya quedo y ya se preparó para toda posible situación
    if request.user.is_authenticated and request.method == 'POST':
        Intento1 = request.POST['Contraseña']
        Intento2 = request.POST['Confirmacion']
        if Intento1 == Intento2:
            u = User.objects.get(id = id)
            u.set_password(Intento1)
            u.save()
            messages.error(request, ("Se cambió la contraseña correctamente, favor de iniciar sesión nuevamente"))
            return render(request, 'users/index.html', {"user":u})
        else:
            temp_user = User.objects.get(id=id)
            messages.error(request, ("Las contraseñas no coinciden"))
            return render(request, 'users/change-pass.html', {"user":temp_user})
        #return render(request, 'PAS/index.html', {})
    elif request.user.is_authenticated:
        temp_user = User.objects.get(id = id)
        #temp_user = User.objects.get(id = id)
        return render(request, 'users/change-pass.html', {"user":temp_user})
    else:
        return render(request, 'index',{})

def editarperfil(request, id):
    if request.user.is_authenticated and request.method != "POST":
        temp_user = User.objects.get(id = id)
        #print(temp_user.Nombre_usuario) #Si selecciona el perfil correcto
        return render(request, 'users/edit-profile.html', {"user":temp_user}) # paso id -> "id": 
    elif request.user.is_authenticated and request.method == 'POST':
        Num=request.POST['uid'] #Recibe 4 en lugar del numero real (5) en este caso, pasa lo mismo en los demás casos de cambio
        usuario_nuevo = request.POST['nombre']
        Fecha_nueva = request.POST['Fecha']
        Apellido_nuevo = request.POST['Apellido']
        Pais_nuevo = request.POST['Pais']
        genero_nuevo = request.POST['Gender']
        tel_nuevo = request.POST['Numero']
        #nuevo_email = request.POST['Apellido2']
        print(Pais_nuevo) #Si lo imprime en la terminal
        user_temp= User.objects.get(id = id) #UPDATE #No siempre selecciona algo # El error esta en esta linea
        print(user_temp)
        user_temp.country = Pais_nuevo
        user_temp.birthday = Fecha_nueva
        user_temp.first_name = usuario_nuevo
        user_temp.last_name = Apellido_nuevo
        user_temp.gender = genero_nuevo.upper()
        user_temp.phone = tel_nuevo
        #user_temp.email = nuevo_email #Checar esto
        #user_temp.Apellido_materno = Apellido_nuevo_2
        user_temp.save()
        return render(request, 'users/index.html', {})
        #us.update(nombre_principal = usuario_nuevo)
        # cur.execute("SELECT * FROM tasks") #Aqui la querry
        # Model.objects.filter(id = 223).update(field1 = 2)
    else:
        return render(request, 'users/index.html', {})

def Dashboard_Personal(request,id):
    if request.user.is_authenticated and request.method != "POST":
        #Dashboard
        h_var = 'Points per game'
        v_var = 'Time played in minutes'
        data = [[h_var,v_var]]
        # for i in range(0,11):
        #     data.append([randrange(101),randrange(101)])
        h_var_json = dumps(h_var)
        v_var_json = dumps(v_var)
        # datos_json = dumps(data)

        mydb = sqlite3.connect("db.sqlite3")
        cur = mydb.cursor()
        cur.execute ("SELECT Puntos_por_partida, Tiempo_jugado FROM users_Historial WHERE ID_Usuario = ? ORDER BY Puntos_por_partida DESC",[id])
        rows = cur.fetchall()
        listasalida = []
        for i in rows:
            d = {}
            d['puntos'] = i[0]
            d['tiempo'] = i[1]
            data.append([i[0],i[1]/60]) #Necesita dos numeros
        datos_json = dumps(data)

        #Grafica 2
        h_var22 = 'Username'
        v_var23 = 'Points per game'
        v_var24 = 'Date'
        v_var25 = 'Time played'
        v_var26 = 'Level Reached'
        data2 = [[h_var22,v_var23,v_var24,v_var25,v_var26]]
        # for i in range(0,11):
        #     data.append([randrange(101),randrange(101)])
        # h_var_json2 = dumps(h_var2)
        # v_var_json2 = dumps(v_var2)
        # datos_json = dumps(data)
        mydb2 = sqlite3.connect("db.sqlite3")
        cur2 = mydb2.cursor()
        cur2.execute("SELECT Nombre_usuario, Puntos_por_partida, Fecha_del_juego, Tiempo_jugado, ID_Canciones FROM users_Historial WHERE ID_Usuario = ?",[id])
        rows2 = cur2.fetchall()
        for i in rows2:
            print(i)
            r = {}
            r['nombre_usuario'] = i[0]
            r['puntos_partida'] = i[1]
            r['Fecha_de_juego'] = i[2]
            r['Tiempo_jugado'] = i[3]
            r['ID_Canciones'] = i[4]
            # r['Fecha'] = i[2]
            # r['Tiempo'] = i[3]
            # r['ID_Canciones'] = i[4]
            # data2.append([i[0],i[1],i[2],i[3],i[4]]) #Necesita dos numeros
            data2.append([i[0], i[1], i[2], i[3]/60, i[4]])
        datos_json2 = dumps(data2)
        print(datos_json2)

        #Grafica 3
        h_var3 = 'ID of the level'
        v_var3 = 'Time of play in minutes'
        data3 = [[h_var3,v_var3]]
        # for i in range(0,11):
        #     data.append([randrange(101),randrange(101)])
        h_var_json3 = dumps(h_var3)
        v_var_json3 = dumps(v_var3)
        # datos_json = dumps(data)
        mydb3 = sqlite3.connect("db.sqlite3")
        cur3 = mydb3.cursor()
        cur3.execute( "SELECT Tiempo_jugado, ID_Canciones  FROM users_Historial WHERE ID_Usuario = ?" , [id])
        rows3 = cur3.fetchall()
        for i in rows3:
            rr = {}
            rr['tiempo'] = i[0]
            rr['id'] = i[1]
            data3.append([i[1],i[0]/60]) #Necesita tres numeros
        datos_json3 = dumps(data3)

        #Grafica 4
        h_var4 = 'Points per game'
        v_var4 = 'Date'
        data4 = [[h_var4,v_var4]]
        # for i in range(0,11):
        #     data.append([randrange(101),randrange(101)])
        h_var_json4 = dumps(h_var4)
        v_var_json4 = dumps(v_var4)
        # datos_json = dumps(data)

        mydb4 = sqlite3.connect("db.sqlite3")
        cur4 = mydb4.cursor()
        #stringSQL4 = '''SELECT Puntos_por_partida ,Nombre_usuario FROM users_Historial ORDER BY Puntos_por_partida DESC LIMIT 1'''
        cur4.execute( "SELECT Puntos_por_partida, Fecha_del_juego FROM users_Historial WHERE ID_Usuario = ? ", [id])
        rows4 = cur4.fetchall()
        listasalida4 = []
        
        for i in rows4:
            #print(i)
            d = {}
            d['puntos'] = i[0]
            d['user'] = i[1]
            data4.append([i[1],i[0]]) #Necesita dos numeros
        #print(data4)
        datos_json4 = dumps(data4)
        #datos_json4 = data4
        #print(datos_json4)

        #Grafica 5
        h_var5 = 'Levels reached'
        v_var5 = 'ID user'
        data5 = [[h_var5,v_var5]]
        # for i in range(0,11):
        #     data.append([randrange(101),randrange(101)])
        h_var_json5 = dumps(h_var5)
        v_var_json5 = dumps(v_var5)
        # datos_json = dumps(data)

        mydb5 = sqlite3.connect("db.sqlite3")
        cur5 = mydb5.cursor()
        cur5.execute("SELECT ID_Canciones ,ID_usuario FROM users_Historial WHERE ID_Usuario = ?", [id])
        rows5 = cur5.fetchall()
        listasalida5 = []
        for i in rows5:
            d = {}
            d['puntos'] = i[0]
            d['tiempo'] = i[1]
            data5.append([i[0],i[1]]) #Necesita dos numeros
        datos_json5 = dumps(data5)

        return render(request, 'users/Dashboard_Personal.html', {'values':datos_json,'h_title':h_var_json,'v_title':v_var_json
                                                        ,'values2':datos_json2,
                                                        'values3':datos_json3,'h_title3':h_var_json3,'v_title3':v_var_json3 , 'contexto': context,'values4':datos_json4,'h_title4':h_var_json4,'v_title4':v_var_json4
                                                 ,'values5':datos_json5,'h_title5':h_var_json5,'v_title5':v_var_json5})
            #return render(request, 'users/Dashboard_Personal.html',{})
    else:
        return render(request, 'users/index.html', {})

#Codigo de Unity
@csrf_exempt
def post_or_get(request):
    print("GETING HERE FIRST")
    if request.method == 'POST':
        # Compare the sent data with the database data
        print("\n--------------------------------------------------")
        print("Request.body that arrived: ")
        print(type(request.body))
        print(request.body)

        print("\n--------------------------------------------------")
        print("Request decoded: ")
        request = request.body.decode('utf8').replace("'", '"')

        user, hshpass = extractRequest(request) # split request and get user and password to check in db
        USER_OBJ = User.objects.filter(username=user)

        if USER_OBJ.exists():
            for user in USER_OBJ:
                DB_HASHED_PASSWORD = user.check_unity # Instead of contrasena, hashed contrasena
                print("\nData in db: ")
                print(DB_HASHED_PASSWORD)

            if hshpass == DB_HASHED_PASSWORD:
                print("They match. Sending 200 status.\n")
                final = create_endpoint(user)
                return HttpResponse(final, status=200)
            else:
                return HttpResponse(status=406)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=502)
def apis(response):
    list_of_dicts = list()
    dict_with_list = dict()
    user_list = User.objects.all().values('username', 'country') # Python dict

    print(user_list)

    for object in user_list:
        list_of_dicts.append(object)

    dict_with_list["Users"] = list_of_dicts
    final = json.dumps(dict_with_list)
    return HttpResponse(final, content_type="text/users.json")
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

#Prueba para dashboard
def apiss(response):
    list_of_dicts = list()
    dict_with_list = dict()
    user_list = Historial.objects.all().values('Nombre_usuario', 'Puntos_por_partida','Fecha_del_juego','Tiempo_jugado','ID_Canciones', 'ID_Usuario' ) # Python dict

    print(user_list)
    
    for object in user_list:
        list_of_dicts.append(object)

    dict_with_list["Users"] = list_of_dicts
    final = json.dumps(dict_with_list)
    return HttpResponse(final, content_type="text/users.json")

#Documentación de la API
def APIDoc(request):
    return render(request,'users/documentation.html',{})
#Pruebas de conexion a videojuego
@csrf_exempt#Este código sirve para comunicarse entre Django y UNITY
def Puntajes(request):#Se registran los puntos del usuario
    if request.method == 'POST':
        var = request.body #viene de Unity
        #dicc = (request.body).decode()
        dicc = json.loads(var.decode('utf-8'))
        print(dicc["username"])
        print(dicc)
        print(dicc["nivel"])
        #r1 = random.randrange(10, 1001) # Cambiarlo por datos que vengan de UNITY
        u = User.objects.get(username = dicc["username"])
        p = Historial(Nombre_usuario = dicc["username"], Puntos_por_partida = dicc["puntos"], Fecha_del_juego = datetime.today().strftime('%Y-%m-%d'), Tiempo_jugado = "%.1f" % dicc["time"], ID_Canciones = dicc["nivel"], ID_Usuario = u.id)
        p.save()
        #jsonnuevo = (request.body).decode()
        #jsonnuevo = json.loads(jsonnuevo)
        return HttpResponse("Please use get")
    else:
        return HttpResponse("Please use post")

@csrf_exempt
def LoginUnity(request):#Este es el lugar donde se verifica que exista el usuario #Ya sirve bien
    if request.method == 'POST':
        var = request.body #viene de Unity
        #dicc = (request.body).decode()
        dicc = json.loads(var.decode('utf-8'))
        print(dicc["username"])
        try:
            user_check = User.objects.get(username=dicc["username"]) #Ve que el usuario en verdad exista
            if user_check.check_unity == dicc["pwd"]:
                return HttpResponse("Se encontro el usuario")
            else:
                #jsonnuevo = (request.body).decode()
                #jsonnuevo = json.loads(jsonnuevo)
                return HttpResponse("No se encuentra")
        except User.DoesNotExist:
            return HttpResponse("No se encuentra") #No se encontró nada
    else:
        return HttpResponse("Please use post")


@csrf_exempt
def BorrarUnity(request):#Este es el lugar donde se verifica que exista el usuario #Ya sirve bien
    if request.method == 'POST':
        var = request.body #viene de Unity
        #dicc = (request.body).decode()
        dicc = json.loads(var.decode('utf-8'))
        print(dicc["username"])
        p = Historial.objects.filter(Nombre_usuario = dicc["username"]).delete()
        p.save()
        return HttpResponse("Datos Borados")
    else:
        return HttpResponse("Solo se accede por POST")

@csrf_exempt
def NivelAlto(request):#Ya redirige a la escena maxima que alcanzó el usuario
    if request.method == 'GET':
        return HttpResponse("Please use POST")
    else:
        var = request.body #viene de Unity
        #dicc = (request.body).decode()
        dicc = json.loads(var.decode('utf-8'))
        campo=str(dicc["username"]) #Se saca el nombre de usuario

        mydb3 = sqlite3.connect("db.sqlite3")
        cur3 = mydb3.cursor()
        print((str(dicc["username"]))) #Se imprime bien

        cur3.execute(" SELECT MAX(ID_Canciones)  FROM users_Historial WHERE Nombre_usuario = ?" ,[campo])
        print("Aqui si esta llegando")
        #cur3.fetchall()
        #rows3 = cur3.execute(stringSQL3) #Error en esta linea
        rows = cur3.fetchall()
        print(rows)
        if len(rows) == 0 or rows == None:
            return HttpResponse("No se encuentra")
        else:
            print(rows[0])
            return JsonResponse(rows[0], safe=False)