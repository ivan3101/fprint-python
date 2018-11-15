import urllib
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
import pyfprint
import base64

url = 'http://192.168.0.100:8080/shot.jpg'  # Cambia esto por la ip de la camara


def decode(frame):
    # Find barcodes and QR codes
    decoded_objects = pyzbar.decode(frame)

    if decoded_objects:
        obj_type = decoded_objects[0].type
        obj_data = None

        # Comprobar si es un QR
        if obj_type == 'QRCODE':
            # Obtener informacion del QR
            obj_data = decoded_objects[0].data

        return obj_data

    else:
        return None


def scan_qr():
    cedula = None

    while not cedula:
        # Iniciar conexion a la Camara
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)

        bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Transformar imagen a Blanco y Negro
        qr_data = decode(bw)

        # Mostrar imagenes de la camara
        cv2.namedWindow('QR', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('QR', 1280, 720)
        cv2.imshow('QR', frame)

        if qr_data:
            imgResp.close()
            cv2.destroyAllWindows()
            qr_data_decoded = qr_data.decode('utf-8')
            cedula = qr_data_decoded.split(' ')[2]

        # Leer keyboard input para cerrar la conexion
        if ord('q') == cv2.waitKey(10):
            exit(0)
    return cedula


def get_huella(cedula):
    r = requests.post('http://localhost:3000/login', json={'cedula': cedula})
    if 'data' in r.json():
        huella_decoded = r.json()['data']['huella']
        huella_b64 = huella_decoded.encode('utf-8')
        return base64.decodebytes(huella_b64)

    else:
        return None


def verify_identity(huella):
    pyfprint.init()
    fp_reader = pyfprint.discover_devices()[0]
    finger = pyfprint.Fprint(huella)
    print('Deslice su dedo por el lector para verificar su identidad')
    fp_reader.open()
    is_verified = fp_reader.verify_finger(finger)[0]
    fp_reader.close()
    pyfprint.exit()
    return is_verified


cedula = scan_qr()
huella = get_huella(cedula)
if huella:
    if verify_identity(huella):
        print('Sesion iniciada')
    else:
        print('Su huella no es la almacenada en la BD')
else:
    print('Su informacion no coincide con ninguno de los usuarios en la BD')
