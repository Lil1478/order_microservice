# order_microservice
## Create the database
Firstly should be created a database
```bash
python create_db.py
```

## Run API
```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
```

### Branch database_queue - using database and rabbitMQ
### Branch master - no database connection and no rabbitMQ
