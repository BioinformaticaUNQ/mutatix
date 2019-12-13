Mutatix
===============

Mutatix es un software de experimentación simple y visualización de mutaciones sobre sequencias de adn. 

Utiliza:

* Pymol para el dibujado de las imagenes.
* Nginx para servir las imagenes a un browser.
* Docker para encapsulado de instalación y dependencias.
* Internacionalización!
 
## Installation

Desde la carpeta principal ejecutar : `docker build -t mutatix -f docker/Dockerfile .`


## Usage

`docker run -v$(pwd)/fasta:/usr/src/fasta -v$(pwd):/usr/src  -it -p8080:80 -eMUTATIX_LOCALE=es mutatix`

Aclaraciones: 

* `-v$(pwd)/fasta:/usr/src/fasta` indica la carpeta donde compartir los archivos fasta (host, contenedor)
* Opcional : si se dispone del código fuente, para reflejar cambios o mantener el historial del cliente.
* El puerto 8080 puede ser cualquiera que no esté en uso en la máquina host.
* La variable de entorno MUTATIX_LOCALE indica el idioma a utilizar: [es, en]

### Examples
```
load_fasta  ./fasta/example_1.fasta -s687 -e3158

mutate -m JukesCantor -s 150

mutate -m manual

image export cealign

image view
```


## License
Mutatix is being developed and maintained as Open-Source software. Licensed under [GNU GENERAL PUBLIC LICENSE version 3](https://www.gnu.org/licenses/gpl-3.0.html)