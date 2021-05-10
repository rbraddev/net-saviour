FROM edgedb/edgedb:latest

# COPY ./backend/dbschema /dbschema

COPY ./compose/local/backend/db/migrate.sh /migrate.sh
RUN sed -i 's/\r$//g' /migrate.sh
RUN chmod +x /migrate.sh