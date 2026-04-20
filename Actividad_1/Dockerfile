#Imgen base oficial de nginx
FROM nginx:alpine

#Elimina configuracion por defecto  
RUN rm -rf /usr/share/nginx/html/*

#Copia tu sitio html al contenedor 
COPY . /usr/share/nginx/html

#expone el puerto 
EXPOSE 80

#EJecuta nginx en primer plano
CMD ["nginx","-g","daemon off;"]