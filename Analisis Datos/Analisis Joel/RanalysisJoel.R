install.packages("dplyr")
install.packages("ggplot2")
install.packages("zoo")
install.packages("kableExtra")
install.packages("tidyverse")
install.packages("devtools")


library("dplyr")
library("ggplot2")
library("zoo")
library("kableExtra")
library("tidyverse")
library(devtools)
library("forcats")

celulares = read.csv(file = "Files/celulares.csv", header = TRUE, sep = ",")
tecnologia = read.csv(file = "Files/tecnologia.csv", header = TRUE, sep = ",")
videojuegos = read.csv(file = "Files/videojuegos.csv", header = TRUE, sep = ",")


#Ventas mensuales de proveedores que vendan celulares marca Xiaomi o Apple que tengan un rating mayor o igual a 4

#Primero se filtra las marcas
celu_filtro1 = dplyr::filter(celulares, grepl('Xiaomi|Apple', celulares$Products_brands))
#Luego se filtra el rating
celu_filtro2 = filter(celu_filtro1, celu_filtro1$Rating >= 4)

celu_filtro2 %>%
  mutate(name = fct_reorder(Title, Monthly_sells)) %>%
  ggplot( aes(x=Title, y=Monthly_sells)) +
  geom_bar(stat="identity", fill="#f68060", alpha=.6, width=.4) +
  coord_flip() +
  xlab("") +
  theme_bw()

#Ventas mensuales de proovedores que vendan laptops de marcas Asus, Lenovo y Dell; y que importen hasta latinoamérica
tecno_filtro1 = dplyr::filter(tecnologia, grepl('Laptops', tecnologia$Products))
tecno_filtro2 = dplyr::filter(tecno_filtro1, grepl('Asus|Lenovo|Dell', tecno_filtro1$Products_brands))
tecno_filtro3 = filter(tecno_filtro2, tecno_filtro2$Imports_to_LA == 'True')

#Dibujo del pie chart

ggplot(tecno_filtro3, aes(x="", y=Monthly_sells, fill=Title)) +
  geom_bar(stat="identity", width=1, color="white") +
  coord_polar("y", start=0) +
  
  theme_void()
