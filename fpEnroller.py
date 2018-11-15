import pyfprint
import requests
import base64


def add_user():
    print("Se procedera a agregar un nuevo usuario al sistema. Por favor, siga las instrucciones\n")
    user = get_user_info()
    user['huella'] = base64.encodebytes(get_finger()[0].data()[:]).decode('utf-8')
    r = requests.post('http://localhost:3000/register', json=user)
    print(r.json())


def get_user_info():
    user = {
        "nombre": input("Ingrese su nombre completo: "),
        "cedula": input("Ingrese su cedula: "),
        "correo": input("Ingrese su correo: "),
        "username": input("Ingrese su nombre de usuario de UJAP en linea: ")
    }

    return user


def get_finger():
    fp_reader = pyfprint.discover_devices()[0]

    fp_reader.open()

    print("Se procedera a escanear su dedo. Debera deslizar su dedo por el escaner hasta que se le indique")
    finger = fp_reader.enroll_finger()

    fp_reader.close()

    return finger


add_user()
