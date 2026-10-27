docker compose -p iot exec superset superset db upgrade
docker compose -p iot exec superset superset init
docker compose -p iot restart superset
docker compose -p iot exec superset superset fab create-admin --username admin --firstname admin --lastname admin --password admin

