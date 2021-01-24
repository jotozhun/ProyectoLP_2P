from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

# Hecho por Joel Torres - Scrapping página principal para el proyecto
def filter_description(raw_description):
    prov_description = ''
    prov_products = ''
    prov_brands = ''
    if ('Marca:' in raw_description):
        raw_description.replace('Marca:', 'Marcas:')
    if ('Productos' in raw_description) and ('Marcas' in raw_description):
        description_list1 = raw_description.split('Productos:')

        description_list2 = []
        if ('Marcas:' in description_list1[0]):
            description_list2 = description_list1[0].split('Marcas:')
            prov_description = description_list2[0]
            prov_brands = description_list2[1]
            prov_products = description_list1[1]
        else:
            description_list2 = description_list1[1].split('Marcas:')
            prov_description = description_list1[0]
            prov_products = description_list2[0]
            prov_brands = description_list2[1]
    else:
        prov_description = raw_description
    return prov_description, prov_products, prov_brands


# Opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = 'Drivers/chromedriver.exe'

driver = webdriver.Chrome(driver_path, options=options)

catalog_list = ['celulares', 'tecnologia', 'videojuegos']
page_code = '?PAGEN_1='
# Inicializar en el navegador
for catalog in catalog_list:
    driver.get('https://compredesdemiami.com/catalog/' + catalog + '/' + page_code + '1')

    # Scrapping del csv de celulares
    WebDriverWait(driver, 5) \
        .until(EC.element_to_be_clickable((By.XPATH,
                                           '/html/body/div/div[2]/div[3]/div[2]/div')))

    catalogListElement = driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div')
    catalogWebList = catalogListElement.find_elements_by_class_name('catalog-item-text')
    pages_num = int(catalogListElement.find_element_by_class_name('modern-page-navigation').text.split(' ')[-3])

    # Los campos que van a llenarse
    titles = list()
    urls = list()
    descriptions = list()
    products = list()
    brands = list()
    for page in range(pages_num):
        if (page + 1) > 1:
            driver.get('https://compredesdemiami.com/catalog/' + catalog + '/' + page_code + str(page + 1))
            WebDriverWait(driver, 5) \
                .until(EC.element_to_be_clickable((By.XPATH,
                                                   '/html/body/div/div[2]/div[3]/div[2]/div')))

            catalogListElement = driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div')
            catalogWebList = catalogListElement.find_elements_by_class_name('catalog-item-text')
        for providerWebElement in catalogWebList:
            prov_title_web_element = providerWebElement.find_element_by_class_name('catalog-item-title')
            prov_title = prov_title_web_element.text
            prov_url = prov_title_web_element.find_element_by_tag_name('a').get_attribute('href')

            titles.append(prov_title)
            urls.append(prov_url)
            # Descripcion necesita su propio filtrado de texto

            prov_description_unfiltered = providerWebElement.find_element_by_class_name('catalog-item-desc').text

            prov_description, prov_products, prov_brands = filter_description(prov_description_unfiltered)
            descriptions.append(prov_description)
            products.append(prov_products)
            brands.append(prov_brands)
            # print('descripcion: %s\nproductos: %s\nmarcas: %s\n' %(prov_description, prov_products, prov_brands))
    df = pd.DataFrame({'Title': titles,
                       'Description': descriptions,
                       'Products': products,
                       'Products_brands': brands,
                       'Contact_url': urls})
    df.to_csv(catalog + '.csv', index=False)
driver.quit()