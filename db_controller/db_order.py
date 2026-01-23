from db_controller.db_pool import get_db_connect

# 寫入order資料
def write_order_data(
		order_num:int,
		user_id:int,
		user_name:str,
		user_phone:str,
		user_email:str,
		attraction_id:int,
		attraction_name:str,
		attraction_address:str,
		attraction_image:str,
		date:str,
		time:str,
		price:int,
		status:str
):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = '''insert into order_data(
	order_num,
	user_id,
	user_name,
	user_phone,
	user_email,
	attraction_id,
	attraction_name, 
	attraction_address,
	image,
	date,
	time,
	price,
	status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
	'''
	mycursor.execute(sql, (order_num,
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
		status))
	conn.commit()
	conn.close()
	print('data insert successfully')

# 拿auto_increment
def get_auto_increment() -> int:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	mycursor.execute('select max(id) from order_data')

	result = [x for x in mycursor]
	final_result = result[0]
	conn.close()
	return final_result[0]
# print(get_auto_increment())

# 寫入已付款資料
def write_payment(booking_id, amount):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')

	sql = 'insert into payment_data(booking_id, amount)values(%s, %s)'
	mycursor.execute(sql, (booking_id, amount))

	conn.commit()
	conn.close()
	print('data insert successfully')

# 更新訂單狀態
def update_status(id:int):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')

	mycursor.execute("update order_data set status='paid' where id = %s", (id,))

	conn.commit()
	conn.close()
	print('update successfully')

# 拿取付款完成訂單資料
def get_order_complete(orderN:str, user_id:int) -> tuple:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')

	sql = "select * from order_data where order_num = %s and user_id = %s"
	mycursor.execute(sql, (orderN, user_id))

	result = [x for x in mycursor]
	conn.close()
	return result

# c = get_order_complete('2026-01-1905', 6)

# 檢查結帳資料
def check_format_phone(str_param:str) -> bool:
	search_dash = str_param.index('-')
	if search_dash == -1:
		return False
	else:
		return True