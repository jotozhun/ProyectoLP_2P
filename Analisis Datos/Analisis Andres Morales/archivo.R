#Hecho por Andres Morales G.
#Analisis de importadoras

install.packages("ggplot2")
install.packages("dplyr")


library(dplyr)
library(ggplot2)

clientes<-sample(10:80, size = 30, replace = TRUE)

 doc = read.csv(file = "importadoras.csv", header = TRUE, sep = ",")
 
 #Pregunta 1. Muestre un grafico de barras donde aparezcan las importadoras, cuya descripcion se distribuidora 
 #ademas que la cantidad de clientes sea mayor o igual a 60
 
 
 doc<-cbind(doc,clientes)
 distribuidores=dplyr::filter(doc,grepl('distribuidora|distribuidores|DISTRIBUIDORES|distribuidor',doc$Description))
 View(distribuidores)
 distribuidoresFiltrados=data.frame(distribuidores$Name,distribuidores$Description,distribuidores$clientes)
 View(distribuidoresFiltrados)
 names(distribuidoresFiltrados)[1]="Nombre"
 names(distribuidoresFiltrados)[2]="Descripcion"
 names(distribuidoresFiltrados)[3]="Clientes (miles)"
  View(distribuidoresFiltrados)
 filtro=filter(distribuidoresFiltrados,distribuidoresFiltrados$`Clientes (miles)`>=60)
 View(filtro)
 ggplot(data=filtro,aes(x=Nombre,y=`Clientes (miles)`)) + geom_bar(stat="identity", position="stack") + coord_flip()+ ggtitle("Gráfico de Distribuidores con mas de 60k clientes")

 
 #Pregunta 2. Muestre un histograma para conocer la cantidad de importadoras que tienen mas $10 millones 
 beneficios<-sample(1:20, size = 30, replace = TRUE)
  doc<-cbind(doc,beneficios)
  doc=filter(doc,doc$beneficios>10)
  histograma = hist(x = doc$beneficios, main = "Importadoras que sus beneficios son mas de 10 millones", xlab = "Ganancias en millones de dolares", ylab = "Numero de importadoras",  col = "gray")

  