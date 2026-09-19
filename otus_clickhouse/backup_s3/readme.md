1. Развернул образ s3 в контейнере
version: "3.8"

services:
  minio:
    image: pgsty/minio:latest
    container_name: minio
    command: server /data --console-address ":9001"
    ports:
      - "9005:9000"   # S3 API endpoint
      - "9001:9001"   # MinIO Console UI
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio
    volumes:
      - minio_data:/var/lib/minio
    healthcheck:
      test: ["CMD", "curl", "-f", "http://minio:9001/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    restart: unless-stopped

volumes:
  minio_data:

  И создал bucket clickhouse-backups
  [1.png]

2. Развернул контейнер с clickhouse-server c clickhouse-backup
version: "3.8"

services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse
    restart: unless-stopped
    #environment:
    #  - CLICKHOUSE_PASSWORD=password123
    volumes:
      # Опционально: кастомные конфиги
      - ./config/users.xml:/etc/clickhouse-server/users.d/users.xml
      - ./config/config.xml:/etc/clickhouse-server/config.d/config.xml
      - clickhouse_data:/var/lib/clickhouse
    ports:
      - "8123:8123"   # HTTP
      - "9000:9000"   # Native TCP
      - "9009:9009"   # Interserver
    networks:
      - ch-net

  clickhouse-backup:
    image: altinity/clickhouse-backup:latest
    container_name: clickhouse-backup
    restart: unless-stopped
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    user: "root:root"
    depends_on:
      - clickhouse
    environment:
      CLICKHOUSE_HOST: clickhouse
      CLICKHOUSE_PORT: 9000
      CLICKHOUSE_USERNAME: default
      CLICKHOUSE_PASSWORD: semashko_876543219
      REMOTE_STORAGE: s3

      # S3-настройка
      S3_ENABLED: "true"
      S3_ENDPOINT: http://host.docker.internal:9005          # Для MinIO укажите адрес вашего контейнера; для AWS — s3.amazonaws.com
      S3_ACCESS_KEY: V9Lky1dEKxDDJ4iclMPZ              # Ваш access key
      S3_SECRET_KEY: 1kMcxF1oeOQsCV9ilu2Pc5WxRjWTmJTKIB8yzwUb                # Ваш secret key
      S3_BUCKET: clickhouse-backups           # Имя бакета, он должен быть создан заранее
      S3_REGION: us-east-1                    # Для MinIO можно оставить любое значение, например us-east-1
      S3_FORCE_PATH_STYLE: "true"            # Обязательно true для MinIO и некоторых S3-совместимых хранилищ
      S3_USE_SSL: "false"                     # true для HTTPS, false для HTTP (MinIO локально)

      # Дополнительные опции (опционально)
      # COMPRESSION_LEVEL: 6                  # Уровень сжатия (1–9)
      # UPLOAD_CONCURRENCY: 4                 # Параллельная загрузка частей
    networks:
      - ch-net
    command: ["server"]
    # entrypoint и command не нужны: при S3_ENABLED=true clickhouse-backup сразу готов к create/restore

volumes:
  clickhouse_data:

networks:
  ch-net:
    driver: bridge

3.  Создаю тестовую таблицу и заполняю данными
[2.png]

4. создаем бэкап инстанса clickhouse и проверяем его upload на s3
[3.png]

5. уничтожаем данные в тестовой таблице путем truncate table
[4.png], [5.png]

6. выполним restore c созданного бэкапа командой
docker exec clickhouse-backup clickhouse-backup restore \
  backup_test_2026-09-19_11-23 \ 
  test_backup \
  --config=/etc/clickhouse-backup/config.yml

Проверим что данные восстановились
[6.png]

7.  Скофинурируем storage_policy и создадим таблицу с хранением в s3

Проверяем присоединенный диск s3: [7.png]

create table "test_bacup"."test_s3" 
(id UInt8)
engine=MergeTree
order by tuple()
SETTINGS storage_policy = 's3_policy';

[8.png],[9.png]