import tkinter as tk
import tkinter.ttk as ttk
import cv2
import requests
import base64
import json
import os
import numpy as np
import pyperclip
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime

with open("settings.json", "r") as f:
    settings = json.load(f)

x = settings["x"]
y = settings["y"]
h = settings["h"]
w = settings["w"]
camera_index = settings["camera_index"]


def crop_image(image, x, y, w, h):
    return image[y:y+h, x:x+w]

def run_ocr():
     # Envía la solicitud HTTP de RESET
    #requests.get("http://192.168.0.200/RESET")

    # Inicializa la cámara
    cap = cv2.VideoCapture(camera_index)

    # Obtiene una imagen de la cámara
    ret, image = cap.read()

    # Redimensiona la imagen a un tamaño más grande
    #image = cv2.resize(image, (1920, 1080))

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica un filtro Gaussiano para suavizar la imagen
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplica un filtro de threshold para resaltar los bordes
    threshold = cv2.Canny(blurred, 75, 200)

    # Aplica un filtro de dilatación para llenar los huecos entre las letras
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    # Verifica si x, y, w y h son diferentes a 'default'
    if x != 'default' and y != 'default' and w != 'default' and h != 'default':
        # Realiza el cropping de la imagen
        cropped_image = crop_image(image, x, y, w, h)
    else:
        # Conserva la imagen original
        cropped_image = image

    # Convierte la imagen a formato base64
    _, img_encoded = cv2.imencode('.jpg', cropped_image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Crea la carpeta img_sources si no existe
    if not os.path.exists('img_sources'):
        os.makedirs('img_sources')

    # Obtiene la fecha y hora actual
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Guarda la imagen en la carpeta img_sources con un nombre único
    cv2.imwrite('img_sources/image_{}.jpg'.format(now), cropped_image)

    # Especifica la URL de la API de Google Cloud Vision
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIz...'

    # Especifica los parámetros de la petición
    data = {
      "requests": [
        {
          "image": {
            "content": img_base64
          },
          "features": [
            {
              "type": "TEXT_DETECTION"
            }
          ]
        }
      ]
    }

    # Realiza la petición a la API
    response = requests.post(url, data=json.dumps(data))

    # Verifica si la respuesta incluye la clave 'responses'
    if 'responses' in response.json():
        text = response.json()['responses'][0]['textAnnotations'][0]['description']
    else:
        text = ''
        messagebox.showerror("Error", "No se ha encontrado ningún texto en la imagen.")

    # Copia el texto al portapapeles
    pyperclip.copy(text)

        # Muestra el texto detectado
    messagebox.showinfo("Escaneado con éxito", "El texto ha sido copiado al portapapeles.")
        # Muestra la imagen
    image = Image.open('img_sources/image_{}.jpg'.format(now))
    image.show()

    # Libera la cámara
    cap.release()

def run_fast_ocr():
     # Envía la solicitud HTTP de RESET
    #requests.get("http://192.168.0.200/RESET")

    # Inicializa la cámara
    cap = cv2.VideoCapture(camera_index)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Obtiene una imagen de la cámara
    ret, image = cap.read()

    # Redimensiona la imagen a un tamaño más grande
    #image = cv2.resize(image, (1920, 1080))

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica un filtro Gaussiano para suavizar la imagen
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplica un filtro de threshold para resaltar los bordes
    threshold = cv2.Canny(blurred, 75, 200)

    # Aplica un filtro de dilatación para llenar los huecos entre las letras
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    # Verifica si x, y, w y h son diferentes a 'default'
    if x != 'default' and y != 'default' and w != 'default' and h != 'default':
        # Realiza el cropping de la imagen
        cropped_image = crop_image(image, x, y, w, h)
    else:
        # Conserva la imagen original
        cropped_image = image

    # Convierte la imagen a formato base64
    _, img_encoded = cv2.imencode('.jpg', cropped_image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Crea la carpeta img_sources si no existe
    if not os.path.exists('img_sources'):
        os.makedirs('img_sources')

    # Obtiene la fecha y hora actual
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Guarda la imagen en la carpeta img_sources con un nombre único
    cv2.imwrite('img_sources/image_{}.jpg'.format(now), cropped_image)

    # Especifica la URL de la API de Google Cloud Vision
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AI...'

    # Especifica los parámetros de la petición
    data = {
      "requests": [
        {
          "image": {
            "content": img_base64
          },
          "features": [
            {
              "type": "TEXT_DETECTION"
            }
          ]
        }
      ]
    }

    # Realiza la petición a la API
    response = requests.post(url, data=json.dumps(data))

    # Verifica si la respuesta incluye la clave 'responses'
    if 'responses' in response.json():
        text = response.json()['responses'][0]['textAnnotations'][0]['description']
    else:
        text = ''
        messagebox.showerror("Error", "No se ha encontrado ningún texto en la imagen.")

    # Copia el texto al portapapeles
    pyperclip.copy(text)

    # Libera la cámara
    cap.release()

    # Muestra el mensaje de éxito
    # messagebox.showinfo("Escaneado con éxito", "El texto ha sido copiado al portapapeles.")

def show_image():
    # Inicializa la cámara
    cap = cv2.VideoCapture(camera_index)

    # Obtiene una imagen de la cámara
    ret, image = cap.read()

    # Redimensiona la imagen a un tamaño más grande
    #image = cv2.resize(image, (1920, 1080))

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica un filtro Gaussiano para suavizar la imagen
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplica un filtro de threshold para resaltar los bordes
    threshold = cv2.Canny(blurred, 75, 200)

    # Aplica un filtro de dilatación para llenar los huecos entre las letras
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    # Verifica si x, y, w y h son diferentes a 'default'
    if x != 'default' and y != 'default' and w != 'default' and h != 'default':
        # Realiza el cropping de la imagen
        cropped_image = crop_image(image, x, y, w, h)
    else:
        # Conserva la imagen original
        cropped_image = image

    # Obtiene la fecha y hora actual
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Guarda la imagen en la carpeta img_sources con un nombre único
    cv2.imwrite('img_sources/image_{}.jpg'.format(now), cropped_image)

    # Muestra la imagen
    image = Image.open('img_sources/image_{}.jpg'.format(now))
    image.show()

    # Libera la cámara
    cap.release()

# Crea la ventana principal
root = tk.Tk()
root.title("OCR WebCam")
root.geometry("435x120")

# Crea los botones
scan_button = tk.Button(root, text="SCAN(ctrl+L)", command=run_ocr, font=("Helvetica", 16), padx=30, pady=10, bg='blue', fg='white')
fast_button = tk.Button(root, text="FAST(ctrl+K)", command=run_fast_ocr, font=("Helvetica", 16), padx=30, pady=10, bg='green', fg='white')
image_button = tk.Button(root, text="IMAGEN(ctrl+I)", command=show_image, font=("Helvetica", 12), padx=10, pady=5, bg='yellow', fg='black')

scan_button.config(relief=tk.GROOVE)
fast_button.config(relief=tk.GROOVE)
image_button.config(relief=tk.GROOVE)
# Agrega relieve a los botones
scan_button.config(relief=tk.GROOVE)
fast_button.config(relief=tk.GROOVE)
image_button.config(relief=tk.GROOVE)

# Redondea las esquinas de los botones
scan_button.config(highlightbackground='blue')
fast_button.config(highlightbackground='green')
image_button.config(highlightbackground='yellow')

# Empaqueta los botones en dos columnas
scan_button.grid(row=0, column=0, padx=10)
fast_button.grid(row=0, column=1, padx=10)
image_button.grid(row=1, column=0, columnspan=2, pady=10)

# Agrega hotkeys a los botones
root.bind('<Control-l>', lambda event: run_ocr())
root.bind('<Control-k>', lambda event: run_fast_ocr())
root.bind('<Control-i>', lambda event: show_image())

# Inicia la aplicación
root.mainloop()
