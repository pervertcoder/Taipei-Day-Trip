from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import mysql.connector
from pydantic import BaseModel
from typing import List
import jwt
from datetime import datetime, timedelta, timezone
import time
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
load_dotenv('.env_jwt')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

def create_jwt(data:dict):
	payload = data.copy()
	expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
	payload["exp"] = int((expire_time).timestamp())
	token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
	return token


def split_maker(string:str) -> list:
	target_lis = string.split('https')
	target_lis[0] = ':jpg'
	new_target_lis = []
	for i in target_lis:
		x = i.replace(':', 'https:')
		new_target_lis.append(x)
	length_new = len(new_target_lis)
	for m in range(length_new):
		if new_target_lis[m][-3:].lower() == 'jpg' or new_target_lis[m][-3:].lower() == 'png':
			new_target_lis[m] == new_target_lis[m]
		else:
			new_target_lis[m] = '無'
	return new_target_lis

def get_db_connect():
	mydb = mysql.connector.connect(
		host = os.getenv('DB_HOST'),
		user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
	return mydb

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

# print(check_member('test@test.com'))

def check_rigisted_mem(m:str) -> list:
	pass

def get_mrt_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select MRT_data, count(*) as 次數 from attraction_info group by MRT_data order by 次數 desc'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result

def get_data_name() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select name_data from attraction_info'

	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result


def get_cate_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select cate_data from attraction_info group by cate_data'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result

def get_attraction_data(data_id:int) -> tuple:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from attraction_info where id = %s'
	mycursor.execute(sql, (data_id,))
	result = [x for x in mycursor]
	return result[0]

def page_date(page:int, category:str | None = None, keyword:str | None = None) -> tuple:
	offset = page * 8
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from attraction_info'
	# mrt = get_mrt_data()
	# name = get_data_name()
	sql_filter = []
	param = []
	if category:
		sql_filter.append('cate_data = %s')
		param.append(category)
	if keyword:
		mrt = get_mrt_data()
		name = get_data_name()
		if keyword in mrt:
			sql_filter.append('MRT_data = %s')
			param.append(keyword)
			# and name_data LIKE %s
		else:
			sql_filter.append('name_data LIKE %s')
			param.append(f'%{keyword}%')
	if sql_filter:
		sql += ' where' + ' ' + ' and '.join(sql_filter)
	sql += ' limit %s, 8'
	param.append(offset)
	
	mycursor.execute(sql, tuple(param))
	result = mycursor.fetchall()
	return result

def diff_page(page:int, category:str | None = None, keyword:str | None = None) -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')

	sql = 'select count(*) as total_count, ceil(count(*) / 8) as total_page from attraction_info'
	mrt = get_mrt_data()
	name = get_data_name()
	sql_filter = []
	param = []
	if category:
		sql_filter.append('cate_data = %s')
		param.append(category)
	if keyword:
		if keyword in mrt:
			sql_filter.append('MRT_data = %s')
			param.append(keyword)
		for i in name:
			if keyword in i:
				sql_filter.append('name_data like %s')
				keyword_name = f'%{keyword}%'
				param.append(keyword_name)
				break
	if sql_filter:
		sql += ' where' + ' ' + ' and '.join(sql_filter)
	
	mycursor.execute(sql, tuple(param))
	result = [x for x in mycursor]
	final_result = []
	final_result.append(result[0][0])
	final_result.append(int(result[0][1]))
	return final_result

# booking資料寫入
def insert_booking_data(user_id:int, attraction_id:int, date:str, time:str, price:int):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'insert into booking_data (user_id, attraction_id, date, time, price)value(%s, %s, %s, %s, %s)'
	mycursor.execute(sql, (user_id, attraction_id, date, time, price))

	conn.commit()
	conn.close()
	print('data inserted successfully')
# 檢查booking資料
def check_booking_data()->list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	mycursor.execute('select * from booking_data')
	result = [x for x in mycursor]
	return result

# 刪除資料表
def delete_booking_data():
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	mycursor.execute('truncate table booking_data')

	conn.commit()
	conn.close()

# 拿booking資料
def render_booking():
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	mycursor.execute('''select
		booking_data.id,
		booking_data.attraction_id,
		booking_data.user_id,
		booking_data.date,
		booking_data.time,
		booking_data.price,
		attraction_info.name_data,
		attraction_info.address_data,
		attraction_info.file_data
		from booking_data
		join attraction_info
		on booking_data.attraction_id = attraction_info.id
	''')
	result = [x for x in mycursor]
	return result
a = render_booking()
# print(a[0])
# 捷運/分類資料回傳格式
class DataResponse(BaseModel):
	data: List[str]

class ErrorResponse(BaseModel):
    error: bool
    message: str

class AttractionResponse(BaseModel):
	data: dict

class AttractionDataResponse(BaseModel):
	nextPage: int | None
	data: list

# 成功狀態格式
class stateResponse(BaseModel):
	ok : bool

# 註冊request格式
class registDataRequest(BaseModel):
	name : str
	email : str
	password : str

# 登入request格式
class loginDataRequest(BaseModel):
	email :str
	password : str

#登入路由回傳格式
class loginDataResponse(BaseModel):
	token : str

# 登入狀態驗證資料格式
class userData(BaseModel):
	id : int
	name : str
	email : str

# 登入狀態驗證
class loginDataCheck(BaseModel):
	data : userData

# 訂單資料details
class bookingData(BaseModel):
	id : int
	name : str
	address : str
	image : str
	

# 訂單資料
class booking(BaseModel):
	attraction : bookingData
	date : str
	time : str
	price : int

# 訂單
class bookingResponse(BaseModel):
	data : booking

# 建立新的訂單
class createBooking(BaseModel):
	attractionId : int
	date : str
	time : str
	price: int
	

app=FastAPI()

security = HTTPBearer()

@app.post('/api/user', tags=['Users'], response_model=stateResponse, responses={200 : {'description' : '註冊成功'}, 400:{'model' : ErrorResponse, 'description' : '註冊失敗，重複的 Email 或其他原因'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
async def register (request:registDataRequest):
	try:
		name = request.name
		email = request.email
		password = request.password
		state = True
		# 檢查有無重複
		check_email = check_member(email)
		print(check_email)
		# 存入資料庫
		if check_email != []:
			state = False
			# raise HTTPException(status_code=400, detail='Email已存在')
		if state:
			insert_register_data(name, email, password)
			return {
				'ok' : True
			}
		else:
			return JSONResponse(status_code=400, content={
				'error' : True,
				'message' : 'Email已存在'
			})
		
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})

@app.put('/api/user/auth', tags=['Users'], response_model=loginDataResponse, responses={400:{'model' : ErrorResponse, 'description' : 'Email或密碼不正確'}})
async def member_data (request:loginDataRequest):
	try:
		email = request.email
		password = request.password
		check = check_member(email)
		# print(check[0][0], check[0][2])
		if check != [] and password == check[0][3]:
			token = create_jwt({'id' : check[0][0], 'email' : check[0][2]})
			return {
				'token' : token
			}
		else:
			return JSONResponse(status_code=400, content={
				'error' : True,
				'message' : 'Email或密碼不正確'
			})
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : '帳號或密碼發生錯誤'
		})
	
@app.get('/api/user/auth', tags=['Users'], response_model=loginDataCheck)
async def check_mem (credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		print(payload)
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=401, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })

		user = check_DB[0]
		return {
			'data' : {
				'id' : user[0],
				'name' : user[1],
				'email' : user[2]
			}
		}
	except jwt.ExpiredSignatureError:
		return JSONResponse(status_code=401, content={
			'error': True,
			'message': 'Token 已過期，請重新登入'
		})
	except jwt.InvalidTokenError:
		return JSONResponse(status_code=401, content={
			'error': True,
			'message': 'Token 無效，請重新登入'
		})

@app.get('/api/mrts', tags=['MRT Station'], response_model=DataResponse, responses={200 : {'description' : '正常運作'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_mrts() -> DataResponse | ErrorResponse:
	try:
		mrt_data = get_mrt_data()
		return {
			'data' : mrt_data
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})

@app.get('/api/categories', tags=['Attraction Category'], response_model=DataResponse, responses={200 : {'description' : '正常運作'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_cate() -> DataResponse | ErrorResponse:
	try:
		cate_data = get_cate_data()
		return {
			'data' : cate_data
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
	
# 範例{400: {'model' : ErrorResponse, 'description' : '景點編號不正確'}}
@app.get('/api/attraction/{attraction_id}', tags=['Attraction'], response_model=AttractionResponse, responses={200 : {'description' : '景點資料'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}, 400 : {'model' : ErrorResponse, 'description' : '景點編號不正確'}})
def get_attraction(attraction_id:int) -> AttractionResponse | ErrorResponse:
	if attraction_id > 58:
		return JSONResponse(status_code=400, content={'error' : True, 'message' : '查無資料'})
	try:
		att_data = get_attraction_data(attraction_id)
		file_data = split_maker(att_data[15])
		file_data.pop(0)
		file_data = [i for i in file_data if i != '無']
		return {
			'data' : {
				'id' : att_data[0],
				'name' : att_data[3],
				'category' : att_data[12],
				'description' : att_data[18],
				'address' : att_data[-1],
				'transport' : att_data[2],
				'mrt' : att_data[9],
				'lat' : att_data[-5],
				'lng' : att_data[5],
				'image' : file_data
			}
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
	

@app.get('/api/attractions', tags=['Attraction'], response_model=AttractionDataResponse, responses={500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_specific_data(page:int, category:str | None = None, keyword:str | None = None) -> AttractionDataResponse | ErrorResponse:
	try:
		result = page_date(page, category, keyword)
		total_page = diff_page(page, category, keyword)[1]
		used_page = None
		if page == total_page - 1:
			final_page = used_page
		else:
			final_page = page + 1
		data_list = []
		for rows in result:
			new_file = split_maker(rows[15])
			new_file.pop(0)
			new_file = [i for i in new_file if i != '無']
			data_list.append({
				'id' : rows[0],
				'name' : rows[3],
				'category' : rows[12],
				'description' : rows[18],
				'address' : rows[-1],
				'transport' : rows[2],
				'mrt' : rows[9],
				'lat' : rows[-5],
				'lng' : rows[5],
				'image' : new_file
			}
		)
		
		return {
			'nextPage' : final_page,
			'data' : data_list
		}
	
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
		
@app.get('/api/booking', tags=['Booking'], response_model=bookingResponse, responses={403:{'model' : ErrorResponse, 'description' : '未登入系統，拒絕存取'}})
def booking_fun(credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		print(payload)
		id = payload['id']
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=401, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })

		booking = render_booking()
		booking_data = list(booking)[0]
		file_data = split_maker(booking_data[8])
		file_data.pop(0)
		file_data = [i for i in file_data if i != '無']
		print(file_data)
		return {
			'data' : {
				'attraction' : {
					'id' : booking_data[1],
					'name': booking_data[6],
					'address' : booking_data[7],
					'image' : file_data[0]
				},
				'date' : booking_data[3],
				'time' : booking_data[4],
				'price' : booking_data[5]
			}
		}
	except jwt.ExpiredSignatureError:
		return JSONResponse(status_code=401, content={
			'error': True,
			'message': 'Token 已過期，請重新登入'
		})
	except jwt.InvalidTokenError:
		return JSONResponse(status_code=401, content={
			'error': True,
			'message': 'Token 無效，請重新登入'
		})

@app.post('/api/booking', tags=['Booking'], response_model=stateResponse, responses={400:{'model' : ErrorResponse, 'description' : '建立失敗，輸入不正確或其他原因'}, 403:{'model' : ErrorResponse, 'description' : '未登入系統，拒絕存取'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def create_booking(request:createBooking, credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		print(payload)
		id = payload['id']
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=403, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })

		user_id = id
		attraction_id = int(request.attractionId)
		date = request.date
		time = request.time
		price = int(request.price)
		check_booking = check_booking_data()
		if not check_booking:
			insert_booking_data(user_id, attraction_id, date, time, price)
		else:
			delete_booking_data()
			insert_booking_data(user_id, attraction_id, date, time, price)

		return {
			'ok' : True
		}

	except jwt.ExpiredSignatureError:
		return JSONResponse(status_code=403, content={
			'error': True,
			'message': 'Token 已過期，請重新登入'
		})
	except jwt.InvalidTokenError:
		return JSONResponse(status_code=403, content={
			'error': True,
			'message': 'Token 無效，請重新登入'
		})
	except Exception as e:
		return JSONResponse(status_code=400, content={
			'error' : True,
			'message' : str(e)
		})
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
	
@app.delete('/api/booking', tags=['Booking'], response_model=stateResponse, responses={400:{'model' : ErrorResponse, 'description' : '建立失敗，輸入不正確或其他原因'}, 403:{'model' : ErrorResponse, 'description' : '未登入系統，拒絕存取'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def delete_booking(credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		print(payload)
		id = payload['id']
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=403, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })

		# check_booking = check_booking_data()
		delete_booking_data()

		return {
			'ok' : True
		}

	except jwt.ExpiredSignatureError:
		return JSONResponse(status_code=403, content={
			'error': True,
			'message': 'Token 已過期，請重新登入'
		})
	except jwt.InvalidTokenError:
		return JSONResponse(status_code=403, content={
			'error': True,
			'message': 'Token 無效，請重新登入'
		})
	except Exception as e:
		return JSONResponse(status_code=400, content={
			'error' : True,
			'message' : str(e)
		})
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
	
app.mount('/static', StaticFiles(directory='static'), name='static')
# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")