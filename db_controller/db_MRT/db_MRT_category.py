from db_controller.db_pool import get_db_connect

def get_mrt_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select MRT_data, count(*) as 次數 from attraction_info group by MRT_data order by 次數 desc'
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