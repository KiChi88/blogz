    Для корректной работы необходимо:
1. Установить зависимости из requarements.txt
2. Внести данные для postgresql
3. Внести данные аккаунта gmail для отправки почты
4. Проверить наличие и в случае отсутствия установить Redis (также для отправки почты)

  Далее:
  
  - Для windows -
  
  1. Запускаем Redis: redis-server.exe, redis-cli.exe (остальным в отдельной консоли redis-server)
  2. Запускаем Celery из директории проекта в отдельной консоли:
      celery -A main worker --pool=solo -l info (остальным celery worker -A main --loglevel=debug --concurrency=4)
