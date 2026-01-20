from dotenv import load_dotenv
import os
from mysql.connector import pooling

# 建立連線池 connection pool
pool = pooling.MySQLConnectionPool(
	pool_name='mypool',
	pool_size=10,
	pool_reset_session=True,
	host = os.getenv('DB_HOST'),
	user = os.getenv('DB_USER'),
	password = os.getenv('DB_PASSWORD')
)


def get_db_connect():
	return pool.get_connection()

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

def get_mrt_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select MRT_data, count(*) as 次數 from attraction_info group by MRT_data order by 次數 desc'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	conn.close()
	return result

def get_data_name() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select name_data from attraction_info'

	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	conn.close()
	return result


def get_cate_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select cate_data from attraction_info group by cate_data'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	conn.close()
	return result

def get_attraction_data(data_id:int) -> tuple:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from attraction_info where id = %s'
	mycursor.execute(sql, (data_id,))
	result = [x for x in mycursor]
	conn.close()
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
	conn.close()
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
	conn.close()
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
# print(a[0])

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

c = get_order_complete('2026-01-1905', 6)
# print(c)