# Selecciona la imagen base de Python que necesitas
FROM python:3.9-slim-buster

# Instala los paquetes necesarios para Apache y tu proyecto Python
RUN apt-get update \
    && apt-get install -y apache2 apache2-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install uwsgi

# Copia los archivos necesarios a la imagen
COPY . /app
WORKDIR /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Instala y configura Apache y mod_wsgi
RUN apt-get install -y libapache2-mod-wsgi-py3 \
    && a2enmod rewrite \
    && a2enmod headers \
    && a2enmod proxy \
    && a2enmod proxy_http \
    && a2enmod ssl \
    && a2enmod wsgi \
    && rm /etc/apache2/sites-enabled/000-default.conf \
    && COPY docker/apache/myapp.conf /etc/apache2/sites-available/myapp.conf \
    && ln -s /etc/apache2/sites-available/myapp.conf /etc/apache2/sites-enabled/myapp.conf \
    && sed -i 's/LogLevel warn/LogLevel info/g' /etc/apache2/apache2.conf \
    && sed -i 's/ServerTokens OS/ServerTokens Prod/g' /etc/apache2/conf-available/security.conf \
    && sed -i 's/ServerSignature On/ServerSignature Off/g' /etc/apache2/conf-available/security.conf \
    && sed -i 's/IncludeOptional sites-enabled\/\*.conf/IncludeOptional sites-enabled\/\*.conf\n\n<Directory \/app>\n    Options FollowSymLinks\n    AllowOverride All\n    Require all granted\n<\/Directory>/g' /etc/apache2/apache2.conf \
    && sed -i 's/^Listen 80/Listen 8080/g' /etc/apache2/ports.conf \
    && chown -R www-data:www-data /app \
    && chmod -R 755 /app

# Define el puerto y el comando que se ejecutará al iniciar el contenedor
EXPOSE 8080
CMD ["apache2ctl", "-D", "FOREGROUND"]
