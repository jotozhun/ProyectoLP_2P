#ANALISIS DE DATOS PAGINAS AMARILLAS 
#HECHO POR RONNY RAUL ANDRADE MORA

library(dplyr) 
library(tidyr)
library(readxl)

pA = read.csv("Paginas-Amarillas.csv",header = TRUE,sep = ",",na.strings = "" ) #CARGA EL ARCHIVO .csv
pA_sinURL = pA[ , -c(3)] #SE ELIMINA LA COLUMNA URL,NO SIRVE PARA EL ANALISIS
pA_sinNA <- pA_sinURL[complete.cases(pA_sinURL),] # SE SELECCIONA LAS FILAS COMPLETAS (sin NA)
pA_Nombres = pA_sinNA
names(pA_Nombres)[1] = "Empresas"
names(pA_Nombres)[3] = "Ventas 1S"
names(pA_Nombres)[4] = "Ventas 2S"
names(pA_Nombres)[7] = "GananciaTotal"
View(pA_Nombres)
sapply(pA_Nombres, class)


#PREGUNTA 1: MODIFIQUE LAS COLUMNAS DE VENTAS 1S Y VENTAS 2S EN DONDE SI TIENE 
#UNA GANANCIA MAYOR A $10.000 SE COBRE UN IMPUESTOS DEL 10%, Y CREE UN DATAFRAME
#EN DONDE SE PONGA LAS EMPRESAS PAGAN IMPUESTOS DEL 10% EN LOS 2 SEMESTRES.

em = pA_Nombres["Empresas"]
impuesto1S = replace(pA_Nombres$`Ventas 1S`,pA_Nombres$`Ventas 1S` > 10000, "Impuestos 10%")
datos1 =data.frame(Empresas = em,Declaracion1S= impuesto1S)

impuesto2S = replace(pA_Nombres$`Ventas 2S`,pA_Nombres$`Ventas 2S` >10000,"Impuestos 10%")
datos2 =data.frame(Empresas = em, Declaracion2S =impuesto2S)

inter = merge(datos1,datos2)
View(inter)

filtrado=filter(inter, Declaracion1S =="Impuestos 10%" & Declaracion2S == "Impuestos 10%")
View(filtrado)
write.csv(filtrado,"Impuestos a pagar.csv")




#PREGUNTA 2: MUESRTRE UNA GRAFICA EN LA QUE MUESTRE LA CANTIDAD DE EMPRESAS
#QUE TIENEN UNA GANANCIA NETA MAYOR A $20K.

bG = pA_Nombres["GananciaTotal"]
Ndato = data.frame(Empresas = em,GananciaTotal = bG)
View(Ndato)
filtadro2 = filter(Ndato,GananciaTotal >20000)
histograma = hist(x = filtadro2$GananciaTotal, main = "EMPRESAS CON MAS DE $20K DE GANACIA NETA", 
                 xlab = "GANANCIA EN DOLARES", ylab = "CANTIDAD DE EMPRESAS",
                 col = "red")


#PREGUNTA 3: LOS INVERSIONSTA TIENEN UN FONDO PARA COMPRAR EMPRESAS QUE TENGAN UNA GANANCIA NETA 
#MENOR AL $5000, EN DONDE SI LA SUMA DE SUS GANANCIA NETA ES MAYOR A SUS FONDOS NO ES UNA BUENA INVERSION
#SI LA SUMA DE SUS GANANCIA NETA ES MEJOR ES UNA BUENA INVERSION.

fondoInversionistas = 15000
Mdatos = data.frame(Empresas = em,GananciaTotal =bG)
filtrado3 = filter(Mdatos,GananciaTotal < 5000)
View(filtrado3)
vec1 = filtrado3[,2]
sumaMenoresEmpresas = sum(vec1)
if(sumaMenoresEmpresas > fondoInversionistas){
  "Es una inversion arriesgada"
}else{
  "Es una buena inversion"
}




