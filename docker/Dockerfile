# FROM nginx:alpine


# RUN apk add python3
# RUN apk add python2


# WORKDIR /usr/src


from ubuntu
run apt update
run apt install python3 python3-pip -y 
run DEBIAN_FRONTEND=noninteractive apt install pymol -y
run apt install nginx -y

run pip3 install cmd2 biopython
run pip3 install python-i18n[YAML]

copy docker/nginx.conf /etc/nginx/sites-enabled/default


workdir /usr/src

copy . . 

run ln -s /usr/src/images/ /var/www

# entrypoint service nginx start
cmd service nginx start ; python3 mutatix.py


