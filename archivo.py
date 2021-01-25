# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
#hecho por Andres Morales
def filtradoCampos(variable):
    name=""
    description=""
    address=""
    phone=""
    city=""

    camposList=variable.split("\n")
    name=camposList[0]
    description=camposList[1]
    for campo in camposList[2:]:
        if not("Guayaquil" in campo) and not("593" in campo):
            address=campo
        elif ("593" in campo):
            phone=campo
        else:
            city=campo
    return name,description,address,phone,city


# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = 'C:\\Users\\moral\\Downloads\\chromedriver.exe'

driver = webdriver.Chrome(driver_path, chrome_options=options)

# Iniciarla en la pantalla 2
driver.set_window_position(2000, 0)
driver.maximize_window()
time.sleep(1)

# Inicializamos el navegador
driver.get('https://www.ecuador-directorio.com/tag/311-importadoras/guayaquil')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div/div/div[1]')))

contenedorIzquierdo = driver.find_element_by_xpath('/html/body/div/div/div[1]')
pages= [0, 1,2,3]
contenedores = contenedorIzquierdo.find_elements_by_class_name('itemPublic')

#for contenedor in contenedores:
 #   print(contenedor.text)

  #  print("\n")

nombre = list()
descripcion = list()
direccion = list()
telefono = list()
ciudad = list()


for page in pages:
    driver.get('https://www.ecuador-directorio.com/tag/311-importadoras/guayaquil?pagina='+ str(page + 1))
    WebDriverWait(driver, 5) \
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div/div/div[1]')))
    listaImportadoraWeb=driver.find_element_by_xpath('/html/body/div/div/div[1]')
    listaImportadoras = listaImportadoraWeb.find_elements_by_class_name('itemPublicInfo')

    for importadora in listaImportadoras:
        raw=importadora.text
        name,description,address,phone,city=filtradoCampos(raw)
        print("nombre"+ name+"\ndescripcion "+description+ "\nphone "+phone+"\ncity"+city)
        nombre.append(name)
        descripcion.append(description)
        direccion.append(address)
        telefono.append(phone)
        ciudad.append(city)

df = pd.DataFrame({'Name': nombre,
                       'Description': descripcion,
                       'Address': direccion,
                       'Phone': telefono,
                       'City': ciudad})
df.to_csv("importadoras.csv" , index=False)
driver.quit()





