#!/usr/bin/env bash
# start a database within a docker container

[ -z "${COMPOSE_PROJECT_NAME:-}" ] && \
  COMPOSE_PROJECT_NAME="$(basename "$(pwd)" | sed -e s/-//g)"

if [ -z "$1" ]; then
  docker-compose up -d db
else
  docker-compose stop db
  docker-compose rm -f db
  docker volume rm "${COMPOSE_PROJECT_NAME}_pgvolume"
  docker-compose build db
  docker-compose up -d db

  DB="${DB:-}"
  DB_USER="${DB_USER:-}"
  MAX_RETRIES=60
  RETRIES_REMAINING="${MAX_RETRIES:-}"

  until "${WINPTY}" docker-compose exec db \
    psql -d "${DB}" -c "select count(*) from ${DB_USER}.testtable"
  do
      sleep 1
      echo "retrying db connection..."
      RETRIES_REMAINING=$((RETRIES_REMAINING - 1))
      if [ "${RETRIES_REMAINING}" -lt 1 ]; then
          cat <<EOF
******* GIVING UP ON DATABASE CONNECTION AFTER ${MAX_RETRIES} RETRIES *********
EOF
          break;
      fi
  done

  sleep 5

  docker cp "$1" "${COMPOSE_PROJECT_NAME}_db_1:/tmp/latest.backup"

  docker-compose exec db \
    pg_restore -d "${DB}" --clean --if-exists //tmp/latest.backup
  docker-compose exec --user root db rm -f //tmp/latest.backup
fi
