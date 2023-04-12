from pydrive2.auth import GoogleAuth
#import funciones as fun
def iniciar_autenticacion():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    #fun.Entrar_Pagina(str(url))
iniciar_autenticacion()
