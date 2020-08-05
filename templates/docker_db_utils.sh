#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# useful functions for dealing with logic surrounding docker and posgres

# wait for a database to spin up in a docker (compose) project # {{{1 ---------
wait_for_db() {
  if [ -z "$3" ]; then
    MAX_RETRIES="$3"
  else
    MAX_RETRIES=60
  fi
  RETRIES_REMAINING="$MAX_RETRIES"
  until docker-compose exec -T "$1" psql -d "$2" -c 'select now()'; do
    echo -e "\e[32m. . .\e[33m retrying \e[34m$2\e[33m connection . . .\e[39m"
    sleep 5
    if [ "$RETRIES_REMAINING" -lt 1 ]; then
      echo -e "\e[35m! ! \e[36m UNABLE TO CONNECT TO DATABASE\e[35m ! !\e[39m"
      echo -e "\e[32m. . \e[31mRETRY COUNT: \e[37m$MAX_RETRIES\e[39m"
      break;
    fi

  done
} # 1}}} ----------------------------------------------------------------------

# backup a database from a postgres docker image {{{1 -------------------------
backup_db() {
  # probably should be its own script
  NOW="$(date +%F)"
  # assign default values from env vars
  PROJECT_NAME=${PROJECT_NAME:-$(basename "$(pwd)")}
  DATABASE=${DATABASE:-postgres}
  CONTAINER=${DB_CONTAINER:-db}
  DB_USER=${DB_USER:-postgres}
  DB_HOST=${DB_HOST:-\tmp}  # default sock for crunchy postgres
  DB_BACKUP=${DB_BACKUP:-$NOW.backup}
  echo -e "\e[32m Backuping at \e[33m$NOW\e[39m"
  while [[ ${1} ]]; do
    case "${1}" in
      -p|--project) PROJECT_NAME="$2"; shift 2;;
      -d|--database) DATABASE="$2"; shift 2;;
      -c|--container) CONTAINER="$2"; shift 2;;
      -u|--user) DB_USER="$2"; shift 2;;
      -h|--host) DB_HOST="$2"; shift 2;;
      -b|--backup-file) DB_BACKUP="$2.backup"; shift 2;;
      *) echo "incorrect flag"; exit 1
    esac
  done
  echo "Creating backup file: $DB_BACKUP"
  docker exec -it "${PROJECT_NAME}_${CONTAINER}_1" \
    pg_dump -U "$DB_USER" -h /tmp -d "$DATABASE" \
      --format=custom -f "/tmp/$DB_BACKUP"
  echo "Copying backup file: $DB_BACKUP"
  docker cp "${PROJECT_NAME}_${CONTAINER}_1" \
    "/tmp/$DB_BACKUP" .
  docker exec -it "${PROJECT_NAME}_${CONTAINER}_1" \
    rm -rf "/tmp/$DB_BACKUP"
  echo "Backup file placed: $DB_BACKUP"
} # 1}}} ----------------------------------------------------------------------

# run a sql file into a database container {{{1 -------------------------------
run_sql() {
  # look for env to set vars first
  DATABASE=${DATABASE:=postgres}
  CONTAINER=${DB_CONTAINER:-db}
  DB_USER=${DB_USER:-postgres}
  DB_HOST=${DB_HOST:-\tmp}  # default sock for crunchy postgres
  LOCAL_SCRIPT="$1"; shift  # first argument should always be the script
  DOCKER_SCRIPT=$(basename "$LOCAL_SCRIPT") # set to basename of script file
  while [[ ${1} ]]; do
    case "${1}" in 
      -c|--container) CONTAINER="$2"; shift 2;;
    esac
  done
  echo "Copying $LOCAL_SCRIPT to $CONTAINER as $DOCKER_SCRIPT."
  sleep 3
  docker cp "$LOCAL_FILE" "${CONTAINER}":"${DOCKER_SCRIPT}"
  echo "Copied $LOCAL_FILE to $CONTAINER as $DOCKER_SCRIPT, running."
  docker-compose exec "${CONTAINER}" \
    psql -d "$DATABASE" -f "${DOCKER_SCRIPT}"
  echo "Finished running SQL script"
} # 1 }}} ---------------------------------------------------------------------

# restore a database from a backup {{{1 ---------------------------------------
restore_db() {
  BACKUP_FILE="$1" # backup file should be first argument
  PROJECT_NAME=${PROJECT_NAME:-$(basename "$(pwd)")}
  DATABASE=${DATABASE:-postgres}
  CONTAINER=${DB_CONTAINER:-db}
  DB_USER=${DB_USER:-postgres}
  DB_HOST=${DB_HOST:-\tmp}  # default sock for crunchy postgres
  while [[ ${1} ]]; do
    case "${1}" in
      -p|--project) PROJECT_NAME="$2"; shift 2;;
      -d|--database) DATABASE="$2"; shift 2;;
      -c|--container) CONTAINER="$2"; shift 2;;
      -u|--user) DB_USER="$2"; shift 2;;
      -h|--host) DB_HOST="$2"; shift 2;;
      -b|--backup-file) BACKUP_FILE="$2.backup"; shift 2;;
      *) echo "incorrect flag"; exit 1
    esac
  done
  echo "Copying backup file $BACKUP_FILE"
  docker cp "$BACKUP_FILE" "${PROJECT_NAME}_${CONTAINER}_1:/tmp/$BACKUP_FILE"
  wait_for_db "$CONTAINER" "$DATABASE"
  docker-compose exec "$CONTAINER" pg_restore -d "$DATABASE" --clean \
    --if-exists "/tmp/$BACKUP_FILE"
  echo "Database restored. Removing restore file."
  docker-compose exec --user root "$CONTAINER" rm -f "/tmp/$BACKUP_FILE"
}

