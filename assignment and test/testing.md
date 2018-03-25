# Testing

Las pruebas al servidor están desarrolladas utilizando Behavior-Driven Development (BDD). Más específicamente se está usando el framework [`behave`](https://pythonhosted.org/behave/), disponible para el lenguaje Python. En particular se está testeando lo siguiente:

* Dado que el servidor está corriendo en la dirección localhost:9100
* Cuando el servidor recibe un request con método M, path P, y headers H
* Entonces, dependiendo del contenido de `documentRoot` el servidor responde con status 200 o 404
* Y además, la respuesta contiene el header `X-RequestEcho`
* Y además, el contenido de `X-RequestEcho` es el correcto, según los parámetros del request

## Cómo ejecutar los tests

Para ejecutar los tests es necesario tener instalado Python, y los siguientes paquetes:

* behave
* requests
* json
* nose

Esto puede instalarse ejecutando `pip install behave requests nose` en la línea de comandos.

Para ejecutar los tests, se debe estar dentro de la carpeta que contiene los directors `features` y `steps`, y ejecutar el comando `behave`, que debiera estar disponible una vez instalado el paquete correspondiente. 

La ejecución de los tests asume un entorno Linux, y además asume que el archivo `iniciarServidor.sh` también está en la carpeta mencionada. 

Usted en su tarea debería sólo modificar el archivo `iniciarServidor.sh` con los comandos necesarios para ejecutar su servidor. Además, debe agregar todos los archivos fuente para la compilación o ejecución de programa.

