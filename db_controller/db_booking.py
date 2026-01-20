from db_controller.db_pool import get_db_connect

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
	conn.close()
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
	conn.close()
	return result
a = render_booking()
