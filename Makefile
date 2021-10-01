# Makefile
## 🌶 flask and hot-reload

flaskdebug:
	docker-compose -f docker-compose-dev.yml run --rm -e DEBUGGER=True -e FLASK_APP=app.py -e FLASK_ENV=development -e SECRET_KEY=B0849467FE81F850D634DDD1CE985EECFB6666E07BC4129FBB641ECBA54AE7CE -e SLACK_API_TOKEN -e MYSQL_DATABASE_USER=root -e MYSQL_DATABASE_PASSWORD=root -e MYSQL_DATABASE_HOST=db -e MYSQL_PORT=3306 -e MYSQL_DATABASE_DB=wallet_sentinel_db_test --service-ports flask flask run --host 0.0.0.0