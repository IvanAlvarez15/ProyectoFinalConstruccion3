from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    #path("api/docs", views.docs, name="docs"),
    path("api/users.json", views.apis, name="apis"),
    path("api/private/", views.post_or_get, name="post_or_get"),
    #path('signup/', views.SignUp.as_view(), name='signup'),
    #Url de dashboard
    path("api/dashboard.json/", views.apiss, name="apis"),
    #Dashboard Personal
    path('Dashboard_Personal/', views.Dashboard_Personal, name="Dashboard_Personal"),
    path('Dashboard_Personal/<int:id>', views.Dashboard_Personal,
    name="Dashboard_Personal"),
    #Urls de web
    path('',views.index, name="index"),
    path('index/', views.index, name="index"),
    path('Cambiar_contraseña/', views.Cambiarcontra, name="Cambiar"),
    path('Cambiar_contraseña/<int:id>', views.Cambiarcontra, name="Cambiar"),
    path('Editar_perfil/', views.editarperfil, name="Editar_perfil"),
    path('Editar_perfil/<int:id>', views.editarperfil, name="Editar_perfil"),
    path('Como_jugar/', views.Comojugar, name="Como_jugar"),
    path('Sobre_juego/', views.Sobrejuego, name="Sobre_juego"),
    path('Registrarse/', views.registrarse, name="Registrarse"),
    path('Nuestro_equipo/', views.ourteam, name="Nuestro_equipo"),
    path('Ingresar/', views.ingresar, name="Ingresar"),
    path('Estadisticas_globales/', views.estadisticasglobales, name="Estadisticas_globales"),
    path('Estadisticas_personales/', views.estadisticaspersonales, name="Estadisticas_personales"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('Borrar/', views.Borrar, name="Borrar"),
    path('Borrar/<int:id>', views.Borrar, name="Borrar"),
    #Para Unity
    path('Puntajes/', views.Puntajes, name="Puntajes"),
    path('LoginUnity/', views.LoginUnity, name="LoginUnity"),
    path('BorrarUnity/', views.BorrarUnity, name="BorrarUnity"),
    path('NivelAlto/', views.NivelAlto, name="NivelAlto"),
    #Para la documentación de la API
    path('API/', views.APIDoc, name="APIDOC")
]
