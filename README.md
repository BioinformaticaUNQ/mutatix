Mutatix
===============

## Description 

Mutatix es un software de experimentación simple y visualización de mutaciones sobre sequencias de adn. En simples pasos permite :

* Cargar un archivo fasta con encabezado y secuencia ADN.
* Hacer una mutación sobre la información cargada.
* Visualizarla.

La aplicación permite al usuario hacer dos tipos de mutaciones:

### A nivel secuencia.

Este tipo de mutación se realiza de dos formas. Una al azar utilizando el algoritmo Jukes - Cantor o una manual, dada por input del usuario. Luego se realiza automáticamente una alineación a nivel secuencia utilizando la librería de bio python pairwise2.

### A nivel PDB.

Si se dispone de un genbank id válido al momento de cargar un fasta. Se intenta buscar un código pdb utilizando un servicio de uniprot. Una vez obtenido el pdb la aplicación permite una mutación de residuos utilizando una librería de [Modeller](https://salilab.org/modeller/wiki/Mutate%20model). Este paso se puede realizar n veces hasta alcanzar una estructura deseada. 

Se pueden visualizar ambas estructuras utilizando el navegador y una aplicación montada en el contenedor de docker.

Mutatix is a simple visualization and experimentation tool on mutations over dna sequences. It allowes:

* Load a fasta file with a header and DNA sequences.
* Work mutating that loaded information.
* Visualize it .

The kind of mutations are divided in two modes.

#### At sequence level

This mutation can be achieved via two ways. One by running Jukes-Cantor algorithm, the other by manually modifying the sequence. Then an alignment is provided using biopython library pairwise2.

#### AT PDB level

If a genebank id is provided at loading fasta time of execution (in the fasta header), the application will ask uniprot for associated pdb ids. With this information, the user can modify the structure residues using a [Modeller](https://salilab.org/modeller/wiki/Mutate%20model) library. 

This can be visualized via web browser and a webapp mounted on the docker container.

## Uses:

* request de id uniprot a través de : https://www.uniprot.org/uniprot/?query={pdb_id}&format=tab&columns=database%28PDB%29
* ngl modificado para visualización en html [NGL at github](https://github.com/arose/ngl)
* Pymol para el dibujado de las imagenes + fetch de pdbs.
* [Modeller](https://salilab.org/modeller/) (requiere licencia)
* Nginx como servidor web.
* Docker para encapsulado de instalación y dependencias.
* Internacionalización!
* Se requiere un navegador actualizado para visualizar pdbs
 
## Installation

Desde la carpeta principal ejecutar : `docker build -t mutatix -f docker/Dockerfile . --build-arg modeller_license={LICENCIA_MODELLER_AQUI}`

## Usage

`docker run -v$(pwd)/fasta:/usr/src/fasta -v$(pwd)/pdb:/usr/src/pdb -v$(pwd)/images:/usr/src/images -it -p8080:80 -eMUTATIX_LOCALE=es mutatix`

`docker run -v$(pwd):/usr/src  -it -p8080:80 -eMUTATIX_LOCALE=es mutatix`

Aclaraciones: 

* `-v$(pwd)/fasta:/usr/src/fasta ... pdb ... images` indica la carpeta donde compartir los archivos fasta, pdbs, e imagenes (host, contenedor).
* Opcional : o puede directamente si se dispone del código fuente, para compartir con el contenedor las 3 carpetas antes mencionadas,, reflejar cambios o mantener el historial del cliente de consola.
* La variable de entorno MUTATIX_LOCALE indica el idioma a utilizar: [es, en]

### Examples
```
load_fasta  ./fasta/example_1.fasta -s687 -e3158

mutate terminal -m JukesCantor -s 150

mutate terminal -m manual

image export cealign

image view
```


```
load_fasta  ./fasta/example_1.fasta -s33 -e1856 -f " "

mutate modeller check 

mutate modeller execute 3 GLN -cA

image html
```


## License
Mutatix is being developed and maintained as Open-Source software. Licensed under [GNU GENERAL PUBLIC LICENSE version 3](https://www.gnu.org/licenses/gpl-3.0.html)
