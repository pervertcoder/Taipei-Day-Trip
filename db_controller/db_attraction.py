from db_controller.db_pool import get_db_connect
from db_controller.db_MRT.db_MRT_category import get_mrt_data

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

def get_data_name() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select name_data from attraction_info'

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
	sql_filter = []
	param = []
	if category:
		sql_filter.append('cate_data = %s')
		param.append(category)
	if keyword:
		mrt = get_mrt_data()
		if keyword in mrt:
			sql_filter.append('MRT_data = %s')
			param.append(keyword)
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