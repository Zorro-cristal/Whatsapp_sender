import tkinter
from tkinter import font
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox

#Funciones
def convertir(numer):
    if (numer[:1] == '+'):
        numer= numer[1:]
    if (numer[:1] == '0'):
        numer= '595' + numer[1:]
    if (numer[:3] != '595'):
        print(numer)
        numero= input("Ingrese el numero corregido o enter para continuar")
        if numero != '':
            numer= numero
    return numer

# Recibe el mensaje
def recep_mensaje():
    global mensaje
    mensaje= str(my_text.get("1.0", "end-1c"))
    for pos in range(len(mensaje)):
        if mensaje[pos] == " ":
            mensaje= mensaje[:pos] + "%20" + mensaje[pos+1:]
            continue
        elif mensaje[pos] == '\n':
            mensaje= mensaje[:pos] + "%0A" + mensaje[pos+1:]
            continue
    print(mensaje)
    ventana.destroy()

def prueba_num():
    #Numero de prueba personales
    global numeros
    numeros= ["0983510916", "+595975901657", "+595993258537"]
    ventana2.destroy()

def recep_num():
    global numeros
    nums= str(my_text2.get("1.0", "end-1c"))
    print(nums)
    numeros= list(nums.split('\n'))
    print(numeros)
    ventana2.destroy()

# Lee el mensaje a enviar
ventana= Tk()
ventana.title("Mensaje a enviar")
Label(text= "Ingrese el mensaje a enviar", font= ("Arial", 14)).grid(row=0, column=0)
my_text= Text(ventana, width=50, height=30)
my_text.grid(row=1, column=0)
my_botton= Button(ventana, text="Aceptar", command=recep_mensaje)
my_botton.grid(row=2, column=0)
ventana.mainloop()
#mensaje= "Porqué%20en%20RAS%20queremos%20que%20sigas%20aprendiendo%20y%20creciendo%20🤩%20te%20traemos%20HOY%20un%20Webinar%20que%20indispensable%20en%20tu%20formación%20profesional%20😎%20y%20tiene%20como%20tema%20%0AIntroducción%20a%20Data%20Science%20y%20Machine%20Learning%20%0A📆%20Fecha:%20Martes%2003%20%0A⏳%20Hora:%2019:00%20H%20%0A📌%20Transmisión:%20Vía%20Google%20Meet%0A🔗%20Link%20del%20Webinar:%20https://meet.google.com/jpq-qnbg-upt%0AACCESO%20LIBRE%20Y%20GRATUITO%0ATe%20esperamos!!!"

# En caso de haber errores permite volver a ingresar los numeros si el usuario asi lo desea
cont= True
while cont:
    # Lee los numeros que se usaran
    fallidos= []
    numeros= []
    ventana2= Tk()
    ventana2.title("Numeros de destino")
    Label(text= "Ingrese los numeros de telefono con codigo de pais", font= ("Arial", 14)).grid(row=0, column=0)
    my_text2= Text(ventana2, width=50, height=30)
    my_text2.grid(row=1, column=0)
    my_botton= Button(ventana2, text="Aceptar", command=recep_num)
    my_botton.grid(row=2, column=0)
    my_botton2= Button(ventana2, text="Prueba", command=prueba_num)
    my_botton2.grid(row=3, column=0)
    ventana2.mainloop()

    #Inicia el navegador
    driver= webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://web.whatsapp.com')

    # Espera a que se halla iniciado sesion para continuar
    x= input("Presione una tecla cuando haya iniciado sesion")

    url= 'https://web.whatsapp.com/send?phone='
    #url= 'https://wa.me/'
    # Recorre los numeros de la lista
    for num in numeros:
        try:
            print("Enviando a " + str(num) + " posicion: " + str(numeros.index(num)))
            num= convertir(num)
            page= url + str(num) + "&text=" + mensaje
            driver.get(page)
            time.sleep(5) # Espera 5 segundos
            #driver.find_element_by_link_text('Escribe un mensaje aquí').send_keys(Keys.ENTER)
            time.sleep(5) # Espera 5 segundos
            driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button').click()
            time.sleep(10) # Espera 10 segundos
        except OSError as err:
            print(err)
            print("Error al enviar al " + num)
            print("Posicion: " + str(numeros.index(num)))
            fallidos.append(num)

    # Cierra el navegador y muestra los numeros fallidos
    root= Tk()
    driver.close()        
    print("Numeros Fallidos: ")
    messagebox.showinfo(message=fallidos, title="Numeros fallidos")
    print(fallidos)

    # Pregunta si se desea continuar o no
    cont= messagebox.askyesno(title="Continuar", message="Desea continuar enviando los mensajes?")
    root.destroy()
