import re
import sqlite3
import sys
import time

import requests

from func.wmAPI.url import ITEMS_ALL, get_item_info_url


def create_db() -> bool:
	# 检测
	cconn = sqlite3.connect('../../db/wmOCR.db')
	try:
		# 战甲
		cconn.execute('''
		create table if not exists warframe(
		id integer primary key autoincrement,
		name text
		);
		''')
		# 武器
		cconn.execute('''
		create table if not exists weapon(
		id integer primary key autoincrement,
		name text,
		url_name text,
		wm_id text,
		price int,
		component int,
		number_owned int
		) 
		''')
		# mod
		cconn.execute('''
		create table if not exists mod(
		id integer primary key autoincrement,
		name text,
		url_name text,
		wm_id text,
		price int,
		number_owned int
		) 
		''')
		# 具体部件

		cconn.commit()
		cconn.close()
		return True
	except Exception as e:
		print('Create db failed, Exception: ', e)
		return False

	"""
	获取所有可交易物品，格式为
	{'payload':{'items':[{'item_name':物品的中文名称, 'url_name': api中物品的url, 'thumb': 物品的图片, 'id': 物品的id}, {...}]},}

	返回的dict格式为
	{'code': (失败->100,成功->200),'content': 获取到的交易物品中的items列表,删除列表中items_name所带的所有空格 }
	"""


def get_all_items(url: str) -> dict:
	return_dict = {'code': 100, 'content': None}
	print('正在从Warframe Market获取所有可交易物品')
	responses = requests.get(url=url, headers={'Language': 'zh-hans'})
	num = 1
	while responses.status_code != 200:
		print('获取失败， 重新尝试获取，当前尝试次数: ', num)
		responses = requests.get(url=url, headers={'Language': 'zh-hans'})
		num += 1
		time.sleep(1)
	del num
	if responses.status_code != 200:
		return return_dict
	print('获取成功')
	responses = responses.json()['payload']['items']
	for d in responses:
		d['item_name'] = d['item_name'].replace(' ', '')
	return_dict['content'] = responses
	return_dict['code'] = 200
	return return_dict


# 获取特定物品的info
def get_item_info(url_name: str) -> dict:
	url = get_item_info_url(url_name)
	return_dict = {'code': 100, 'content': None}
	responses = requests.get(url=url, headers={'Platform': 'pc'})
	num = 1
	while responses.status_code != 200:
		print('获取物品信息失败, url: ', url_name, '当前尝试次数：', num)
		responses = requests.get(url=url, headers={'Platform': 'pc'})
		num += 1
		time.sleep(1)
	del num
	if responses.status_code != 200:
		return return_dict
	responses = responses.json()['payload']['item']['items_in_set'][0]
	return_dict['code'] = 200
	return_dict['content'] = responses
	time.sleep(0.4)

	return return_dict


# 获取特定物品的tags
def get_item_tags(url_name: str) -> dict:
	print('get tags from ', url_name)
	return_dict = {'code': 100, 'content': None}
	info_dict = get_item_info(url_name)
	if info_dict['code'] != 200:
		print('获取物品信息失败')
		return return_dict
	else:
		return_dict['content'] = info_dict['content']['tags']
		return_dict['code'] = 200
		return return_dict


if __name__ == '__main__':
	create_db()
	conn = sqlite3.connect('../../db/wmOCR.db')
	cur = conn.cursor()
	items_dict = get_all_items(ITEMS_ALL)
	if items_dict['code'] == 100:
		print('获取所有可交易物品信息失败,停止当前脚本')
		time.sleep(3)
		sys.exit(0)

	for item in items_dict['content']:
		info_list = get_item_tags(item['url_name'])['content']
		for info in info_list:
			name = item['item_name']
			match info:
				case 'warframe':
					if 'mod' in info_list:
						break
					name = re.findall('.+Prime', name)[0]
					sql = 'select name from warframe where name = ?'
					cur.execute(sql, (name,))
					is_insert = cur.fetchone()
					if is_insert is None:
						sql = 'insert into warframe (name) values (:name)'
						cur.execute(sql, (name,))
						print('insert ', name, ' to table warframe')
						conn.commit()
				case 'weapon':
					if 'component' not in info_list:
						# 不需要制作的可交易武器
						sql = 'select name from weapon where name = ?'
						cur.execute(sql, (name,))
						is_insert = cur.fetchone()
						if is_insert is None:
							sql = 'insert into weapon(name,url_name,wm_id,component) values (:name,:url_name,:wm_id,0)'
							cur.execute(sql, (name, item['url_name'], item['id']))
							print('insert ', name, 'to table weapon')
							conn.commit()
					elif 'prime' not in info_list:
						# 非P版需要制造的可交易武器
						name = get_item_info(item['url_name'])['zh-hans']['item_name'].rsplit(' ', 1)[0]
						sql = 'select name from weapon where name = ?'
						cur.execute(sql, (name,))
						is_insert = cur.fetchone()
						if is_insert is None:
							sql = 'insert into weapon(name,component) values (:name,1)'
							cur.execute(sql, (name,))
							print('insert ', name, ' to table weapon')
							conn.commit()
					else:
						# 需要制作的P版武器
						name = re.findall('.+Prime', name)[0]
						sql = 'select name from weapon where name = ?'
						cur.execute(sql, (name,))
						is_insert = cur.fetchone()
						if is_insert is None:
							sql = 'insert into weapon(name,component) values (:name,1)'
							cur.execute(sql, (name,))
							print('insert ', name, ' to weapon')
							conn.commit()

				case 'mod':
					sql = 'select name from mod where  name = ?'
					cur.execute(sql, (name,))
					is_insert = cur.fetchone()
					if is_insert is None:
						sql = 'insert into mod(name, url_name, wm_id) values (:name,:url_name,:wm_id)'
						cur.execute(sql, (name, item['url_name'], item['id']))
						print('insert ', name, ' to table mod')
						conn.commit()
