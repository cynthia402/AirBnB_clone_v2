#!/usr/bin/env bash
#config nginx and the neccessary directory and files

[[ ! -x nginx ]]  && apt update && apt install nginx -y

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
touch /data/web_static/releases/test/index.html
echo "<html>
   <head>
     </head>
     <body>
        Holberton School
    </body>
 </html>" > /data/web_static/releases/test/index.html
[[ -L /data/web_static/current ]] && rm -rf /data/web_static/current
 
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data
chmod -R 755 /data
sed -i '48 i \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
 
service nginx restart
