BASE_URL = 'https://api.warframe.market/v1/'
JTW_URL = 'https://warframe.market/'
AUTH_SIGNIN = BASE_URL + '/auth/signin'
AUTH_REGISTRATION = BASE_URL + '/auth/registration'
AUTH_RESTORE = BASE_URL + '/auth/restore'
ITEMS_ALL = BASE_URL + 'items'
ITEMS_BASE = ITEMS_ALL + '/'


def get_item_info_url(url_name: str) -> str:
	return ITEMS_BASE + url_name


def get_item_orders_url(url_name: str) -> str:
	return ITEMS_BASE + url_name + '/orders'


def get_item_dropsources_url(url_name: str) -> str:
	return ITEMS_BASE + url_name + '/dropsources'
