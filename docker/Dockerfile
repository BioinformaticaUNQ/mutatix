# FROM nginx:alpine


# RUN apk add python3
# RUN apk add python2


# WORKDIR /usr/src


from ubuntu
run apt update
run apt install python3 python3-pip -y 
run DEBIAN_FRONTEND=noninteractive apt install pymol -y
run apt install nginx -y
run apt install vim -y
run apt install wget -y

run pip3 install cmd2 biopython
run pip3 install python-i18n[YAML]
run pip3 install requests

run wget https://salilab.org/modeller/9.23/modeller_9.23-1_amd64.deb
run dpkg -i modeller_9.23-1_amd64.deb
run rm modeller_9.23-1_amd64.deb

arg modeller_license 
run sed -i "s/xxx/$modeller_license/g" /usr/lib/modeller9.23/modlib/modeller/config.py

workdir /usr/src
run mkdir images
run mkdir pdb
run mkdir html

copy docker/nginx.conf /etc/nginx/sites-enabled/default

run rm -rf /var/www/html 

copy . . 

run ln -s /usr/src/images/ /var/www
run ln -s /usr/src/pdb/ /var/www
run ln -s /usr/src/html/ /var/www

# entrypoint service nginx start
cmd python3 mutatix.py


