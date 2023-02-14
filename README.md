# MinIO tutorial

### Шаг 1.
Развернули Server + MinIO. Доступ по портам.
```shell
docker-compose up -d --build
```

### Шаг 2.
Добавляем Nginx в `docker-compose.yml`, убираем проброс порта у сервера.  
Меняем ссылку на загрузку файла на клиенте.
