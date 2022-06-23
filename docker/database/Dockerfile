FROM mariadb
ENV MYSQL_ROOT_PASSWORD=mypass
ENV MYSQL_DATABASE=lexsearch
RUN apt update -y
RUN apt upgrade -y
ADD database-schema.sql /docker-entrypoint-initdb.d/database-schema.sql
