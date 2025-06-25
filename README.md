from server directory run 

FLASK_APP=server.app  
FLASK_DEBUG=True
FLASK_RUN_HOST=localhost   
FLASK_RUN_PORT=5555        

flask db init
flask db migrate 
flask db upgrade 
python -m server/seed.py or python -m server.seed

flask run 
