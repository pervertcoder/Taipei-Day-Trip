from db_controller.db_pool import get_db_connect
import jwt
from env_settings.settings import ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta, timezone

def insert_register_data(n:str, m:str, p:str):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'insert into web_attraction_memberinfo (name, email, password) values (%s, %s, %s)'
	mycursor.execute(sql, (n, m, p))

	conn.commit()
	conn.close()
	print('data inserted successfully')

def check_member(m:str) -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from web_attraction_memberinfo where email = %s'
	mycursor.execute(sql, (m,))
	result = [x for x in mycursor]
	conn.close()
	return result

def create_jwt(data:dict):
	payload = data.copy()
	expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
	payload["exp"] = int((expire_time).timestamp())
	token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
	return token