import win32con

key_dict = {
	"A": "65", "B": "66", "C": "67", "D": "68", "E": "69", "F": "70", "G": "71", "H": "72", "I": "73", "J": "74",
	"K": "75", "L": "76", "M": "77", "N": "78", "O": "79", "P": "80", "Q": "81", "R": "82", "S": "83", "T": "84",
	"U": "85", "V": "86", "W": "87", "X": "88", "Y": "89", "Z": "90", "0": "48", "1": "49", "2": "50", "3": "51",
	"4": "52", "5": "53", "6": "54", "7": "55", "8": "56", "9": "57", "F1": "112", "F2": "113", "F3": "114",
	"F4": "115", "F5": "116", "F6": "117", "F7": "118", "F8": "119", "F9": "120", "F10": "121", "F11": "122",
	"F12": "123", "TAB": "9", "ALT": "18"
}


class PicAPI(object):
	def __init__(self):
		self.ImgPath = 'ocr/RapidOCR-json/screenshot/screen.jpg'
		self.HandleName = 'Warframe'
		self.PrtKey = 'F8'
		self.handle = None

	def listener_keyboard(self):
		pass
