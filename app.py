from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timezone
import requests

# 資料庫操作函式
from db_controller.db_MRT.db_MRT_category import get_mrt_data, get_cate_data
from env_settings.settings import SECRET_KEY, PARTNER_KEY, ALGORITHM
from db_controller.db_attraction import split_maker, get_attraction_data, page_date, diff_page
from db_controller.db_user import insert_register_data, check_member, create_jwt, check_format
from db_controller.db_booking import insert_booking_data, check_booking_data, delete_booking_data, render_booking, check_time
from db_controller.db_order import write_order_data, get_auto_increment, write_payment, update_status, get_order_complete
from db_controller.api_class import DataResponse, ErrorResponse, AttractionResponse, AttractionDataResponse, stateResponse, registDataRequest, loginDataRequest, loginDataResponse, loginDataCheck, bookingResponse, createBooking, createOrder, orderResponse, getOrderResponse


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
		# 檢查格式
		check_email_format = check_format(email)
		# 存入資料庫
		if check_email != [] or check_email_format != True:
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
		# print(payload)
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
		id = payload['id']
		# print(id)
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=401, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })

		booking = render_booking()
		if booking == []:
			return {
				'data' : None
			}
		booking_data = list(booking)[0]
		file_data = split_maker(booking_data[8])
		file_data.pop(0)
		file_data = [i for i in file_data if i != '無']
		# print(file_data[0])
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
		# print(payload)
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
		checking_time = check_time()
		if int(date[5:7]) < int(checking_time['month']):
			print('無效日期')
			return
		if int(date[8:10]) <= int(checking_time['date']):
			print('無效日期')
			return
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
		# print(payload)
		# id = payload['id']
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

@app.post('/api/orders', tags=['order'], response_model=orderResponse, responses={400:{'model' : ErrorResponse, 'description' : '建立失敗，輸入不正確或其他原因'}, 403:{'model' : ErrorResponse, 'description' : '未登入系統，拒絕存取'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def create_order(request:createOrder, credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id = payload['id']
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=403, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })
		prime = request.prime
		order_data = request.order
		price = order_data.price
		attraction_data = request.order.trip.attraction
		attraction_id = attraction_data.id
		attraction_name = attraction_data.name
		attraction_address = attraction_data.address
		attraction_image = attraction_data.image
		date = order_data.trip.date
		time = order_data.trip.time
		user_data = request.order.contact
		user_id = id
		user_name = user_data.name
		user_email = user_data.email
		user_phone = user_data.phone

		status = 'unpaid'
		order_num = None

		
		# 確認日期格式
		time = datetime.now(timezone.utc)
		edit_time = str(time)
		current_date = edit_time[0:10]
		# print(current_date)
		order_num_son = get_auto_increment()
		
		if order_num_son == None:
			order_num = current_date + '0' + '1'
		else:
			order_num = current_date + '0' + str(order_num_son + 1)

		# 寫入資料庫
		write_order_data(
			order_num, 
			user_id, 
			user_name, 
			user_phone,
			user_email,
			attraction_id, 
			attraction_name, 
			attraction_address, 
			attraction_image,
			date,
			time,
			price,
			status
			)
		credit_load = {
  			"prime": prime,
  			"partner_key": PARTNER_KEY,
  			"merchant_id": "pertvertcasher_CTBC",
  			"amount": price,
			'order_number' : order_num,
  			"details":"TapPay Test",
  			"cardholder": {
      			"phone_number": user_phone,
      			"name": user_name,
      			"email": user_email,
  				},
  			"remember": False
		}
		url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
		headers = {
			'Content-Type': 'application/json',
			'x-api-key' : PARTNER_KEY
			}

		response = requests.post(url, json=credit_load, headers=headers)

		# 寫入已付款資料
		if response.status_code != 200:
			return {
				'error' : True,
				'message' : 'taypay HTTP error'
			}
		taypay_result = response.json()
		print(taypay_result)
		booking_id = order_num[-2] + order_num[-1];
		if taypay_result['status'] == 0:
			update_status(booking_id)
			payment_id = taypay_result['order_number'][-2] + taypay_result['order_number'][-1]
			write_payment(payment_id, taypay_result['amount'])
			delete_booking_data()
			return {
				'data' : {
					'number' : taypay_result['order_number'],
					'payment' : {
						'status' : taypay_result['status'],
						'message' : '付款成功'
					}
				}
			}
		else:
			return {
				'data' : {
					'number' : order_num,
					'error' : True,
					'message' : '付款失敗'
				}
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


@app.get('/api/orders/{number}', tags=['order'], response_model=getOrderResponse, responses={403:{'model' : ErrorResponse, 'description' : '未登入系統，拒絕存取'}})
def get_order(number:str, credentials: HTTPAuthorizationCredentials = Depends(security)):
	token = credentials.credentials.replace('Bearer ', '')
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id = payload['id']
		# print(id)
		check_DB = check_member(payload['email'])

		if not check_DB:
			return JSONResponse(status_code=403, content={
                'error': True,
                'message': '使用者不存在或已被刪除'
            })
		
		render_data = get_order_complete(number, id)
		if render_data == []:
			return {
				'data' : None
			}
		else:
			render_data_arr = []
			for i in render_data[0]:
				render_data_arr.append(i)

			if render_data_arr[13] != 'paid':
				render_data_arr[13] = 2
			else:
				render_data_arr[13] = 1
			
			return {
				"data": {
					"number": render_data_arr[1],
					"price": render_data_arr[12],
					"trip": {
						"attraction": {
							"id": render_data_arr[6],
							"name": render_data_arr[7],
							"address": render_data_arr[8],
							"image": render_data_arr[9]
							},
						"date": render_data_arr[10],
						"time": render_data_arr[11]
					},
					"contact": {
					"name": render_data_arr[3],
					"email": str(render_data_arr[2]),
					"phone": render_data_arr[4]
					},
					"status": render_data_arr[13]
				}
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