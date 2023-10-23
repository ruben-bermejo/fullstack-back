# Práctica desarrollo Cloud Native
### Un ejercicio práctico de uso y orquestación de contenedores Docker.  

## Entorno de trabajo  

Este ejercicio se ha llevado a cabo sobre una distribución Ubuntu en una Raspberry Pi 4, pero debe ser compatible con cualquier otra distribución de Linux. 

Se ha utilizado Podman como solución de contenedores, por la ventaja que supone prescindir de un daemon centralizado y de los derechos de root para su funcionamiento, y por su casi total compatibilidad con Docker.

La solución consiste en:
- Un contenedor para una base de datos relacional (mariadb)
- Un contenedor para una base de datos documental (mongodb)
- Un contenedor para el backend (tomcat + aplicación java/spring)

## Instalación:
Copiar los archivos incluidos en la entrega en la ruta deseada de una máquina Linux y llevar a cabo los pasos siguientes desde dicha ruta  

### Instalar los paquetes necesarios:
`sudo apt-get install podman`  
`sudo apt-get install podman-compose`

### Construir la imagen personalizada de Tomcat que contiene el backend
`podman build -t repositorios-app -f Dockerfile`

### Arrancar los contenedores a partir del fichero docker-compose.yml proporcionado
`podman-compose up -d`
