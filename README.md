# OCR_WebCam
El código es una aplicación de Python construida utilizando la biblioteca Tkinter para la interfaz gráfica y diversas bibliotecas adicionales para manipular imágenes y realizar OCR (Reconocimiento Óptico de Caracteres) a través de la API de Google Cloud Vision. A continuación, se describe cada sección del código:

### Importaciones

- Se importan bibliotecas necesarias para el funcionamiento de la aplicación, incluyendo `tkinter` para la GUI, `cv2` para la manipulación de imágenes, `requests` para realizar peticiones HTTP, entre otras.

### Lectura de Configuraciones

- Se lee un archivo `settings.json` para obtener configuraciones predefinidas como las coordenadas `x, y` y las dimensiones `w, h` para recortar la imagen y el índice de la cámara a utilizar.

### Funciones

- **crop_image**: Función que recibe una imagen y coordenadas/dimensiones para recortar la imagen.
- **run_ocr**: Función que captura una imagen desde la webcam, la procesa aplicando varios filtros y técnicas de procesamiento de imágenes para luego enviarla a la API de Google Cloud Vision para realizar OCR. El texto resultante se copia al portapapeles y se muestra una notificación al usuario.
- **run_fast_ocr**: Similar a `run_ocr` pero con diferencias en la configuración de la cámara y sin la notificación final de éxito. 
- **show_image**: Función que simplemente captura una imagen desde la webcam, aplica algún procesamiento básico y muestra la imagen al usuario.

  
  ![Captura de pantalla 2023-09-18 232622](https://github.com/HonroAvisp/OCR_WebCam/assets/73007200/76521f10-95ae-49a2-9ed4-40c85414d76a)

### Creación de la Interfaz Gráfica (GUI)

- Se crea una ventana principal usando `tk.Tk()`.
- Se configuran y colocan tres botones en la ventana, cada uno asociado con una de las funciones descritas anteriormente.
- Se configuran "hotkeys" (atajos de teclado) para cada función, permitiendo activarlas con combinaciones de teclas.
- Se inicia el bucle principal de Tkinter con `root.mainloop()` para iniciar la aplicación.

### Consideraciones adicionales

- La aplicación guarda automáticamente cada imagen procesada en una carpeta llamada `img_sources`, creando un historial de todas las imágenes procesadas con un nombre de archivo que contiene la fecha y hora exacta de cuando fue tomada la imagen.
- La aplicación verifica si las coordenadas y dimensiones para recortar la imagen son diferentes a 'default' antes de decidir si recortar la imagen o no.
- La API de Google Cloud Vision se utiliza mediante peticiones HTTP POST con la imagen codificada en base64 en el cuerpo de la petición. El código de API se incluye directamente en la URL.
- Se ha comentado el código para una posible funcionalidad de enviar una solicitud RESET a un dispositivo a través de una dirección IP específica.

## Ejemplo de uso
### Entrada
![image](https://github.com/HonroAvisp/OCR_WebCam/assets/73007200/2ce096bf-578c-4461-b7c1-e0c2aa271813)
### Salida
PSelnt - Ejecutando proceso DIASAMESESYSE...
Ingrese el número total de días:
$$
>4859
$$
El total de días equivale a:
Años: 13
Meses: 3
Semanas: 3
Días: 3
*** Ejecución Finalizada.

