from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

#Hecho por Ronny
#Opciones de navegacion
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
driver_path = 'Drivers/chromedriver.exe'

driver = webdriver.Chrome(driver_path,options=options)

#Inicializamos el navegador
driver.get("https://www.paginas-amarillas.com.ec/guayaquil/servicios/exportadores-e-importadores")


WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div[2]/div/div[2]')))\


#Contenedor con nuemro de pagina
contenedor2 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div')


#Listas de resultado de scrapping
titles = list()
urls = list()
direction = list()
pagefinal = [0,1]

for page in pagefinal:
    if (page + 1) >= 1:
        driver.get('https://www.paginas-amarillas.com.ec/guayaquil/servicios/exportadores-e-importadores?page=' + str(page + 1))
        WebDriverWait(driver, 5) \
            .until(EC.element_to_be_clickable((By.XPATH,
                                               '/html/body/div[1]/div[2]/div')))

        contenedor = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]')
        catalogWebList = contenedor.find_elements_by_class_name('col-sm-10')
        for element in catalogWebList:
            # Titulo
            componenteTitulo = element.find_element_by_class_name('companyName')
            titulos = componenteTitulo.text
            titles.append(titulos)
            # URL
            componenteURL = element.find_element_by_class_name('titleFig')
            p_url = componenteURL.find_element_by_tag_name('a').get_attribute('href')
            urls.append(p_url)
            # Direccion
            componenteDescripcion = element.find_element_by_class_name('directionFig')
            direc = componenteDescripcion.text
            direction.append(direc)


df = pd.DataFrame({'Compañia': titles,
                       'Direccion': direction,
                       'URL': urls})
df.to_csv('Paginas-Amarillas.csv', index=False)
driver.quit()
