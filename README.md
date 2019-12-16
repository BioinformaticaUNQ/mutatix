Mutatix
===============

Mutatix es un software de experimentación simple y visualización de mutaciones sobre sequencias de adn. 

Utiliza:

* ngl modificado para visualización en html [NGL at github](https://github.com/arose/ngl)
* Pymol para el dibujado de las imagenes + fetch de pdbs.
* Nginx como servidor web.
* Docker para encapsulado de instalación y dependencias.
* Internacionalización!
* Se requiere un navegador actualizado para visualizar pdbs
 
## Installation

Desde la carpeta principal ejecutar : `docker build -t mutatix -f docker/Dockerfile . --build-arg modeller_license={LICENCIA AQUI}`

## Usage

`docker run -v$(pwd)/fasta:/usr/src/fasta -v$(pwd)/pdb:/usr/src/pdb -v$(pwd)/images:/usr/src/images -it -p8080:80 -eMUTATIX_LOCALE=es mutatix`
`docker run -v$(pwd):/usr/src  -it -p8080:80 -eMUTATIX_LOCALE=es mutatix`

Aclaraciones: 

* `-v$(pwd)/fasta:/usr/src/fasta ... pdb ... images` indica la carpeta donde compartir los archivos fasta (host, contenedor) , pdbs, e imagenes.
* Opcional : si se dispone del código fuente, para reflejar cambios o mantener el historial del cliente.
* La variable de entorno MUTATIX_LOCALE indica el idioma a utilizar: [es, en]

### Examples
```
load_fasta  ./fasta/example_1.fasta -s687 -e3158

mutate -m JukesCantor -s 150

mutate -m manual

image export cealign

image view
```


```
load_fasta  ./fasta/example_1.fasta -s33 -e1856 -f " "

mutate modeller 3 GLN -cA

image html
```


## License
Mutatix is being developed and maintained as Open-Source software. Licensed under [GNU GENERAL PUBLIC LICENSE version 3](https://www.gnu.org/licenses/gpl-3.0.html)