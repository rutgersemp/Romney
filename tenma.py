import serial
from time import sleep

class TENMA:
	safeDelay = 0.1

	def __init__(self, com):
		self.com = com
		self.ser = serial.Serial(self.com)

		self.ser.baudrate = 9600
		self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
		self.ser.parity = serial.PARITY_NONE #set parity check: no parity
		self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
		self.ser.timeout = 1            #non-block read

		try:
			self.ser.open()
		except serial.serialutil.SerialException:
			pass

	def writeBytes(self, cmd):
		self.ser.write(bytes(cmd, encoding='utf8'))
		sleep(TENMA.safeDelay)

	def readN(self, N):
		return self.ser.read(N)

	def readAll(self):
		bufsize = self.ser.in_waiting
		res =  self.ser.read(bufsize)

		return res

	# set maximum output voltage for channel
	def setV(self, channel, voltage):
		cmd = f"VSET{channel}:{voltage}"
		self.writeBytes(cmd)

	# return current max voltage setting
	def getVset(self, channel):
		self.ser.reset_input_buffer()

		cmd = f"VSET{channel}?"
		self.writeBytes(cmd)
		res = self.readAll()

		return self.toFloat(res)

	# return actual voltage output
	def getVout(self, channel):
		self.ser.reset_input_buffer()

		cmd = f"VOUT{channel}?"
		self.writeBytes(cmd)
		res = self.readAll()

		return self.toFloat(res)

	# set maximum output current for channel
	def setI(self, channel, current):
		cmd = f"ISET{channel}:{current}"
		self.writeBytes(cmd)

	# return current max current setting
	def getIset(self, channel):
		self.ser.reset_input_buffer()

		cmd = f"ISET{channel}?"
		self.writeBytes(cmd)
		res = self.readAll()

		return self.toFloat(res)

	# return actual current output
	def getIout(self, channel):
		self.ser.reset_input_buffer()

		cmd = f"IOUT{channel}?"
		self.writeBytes(cmd)
		res = self.readAll()

		return self.toFloat(res)

	def OverCurrentEnable(self, enabled):
		if enabled is 1 or enabled is 0:
			self.writeBytes(f"OCP{enabled}")
		else:
			raise ValueError("enabled flag non-boolean")

	def OverVoltageEnable(self, enabled):
		raise NotImplementedError
	"""
		if enabled is 1 or enabled is 0:
			self.writeBytes(f"OVP{enabled}")
		else:
			raise ValueError("enabled flag non-boolean")
	"""


	def outputEnable(self, enabled):
		if enabled is 1 or enabled is 0:
			self.writeBytes(f"OUT{enabled}")
		else:
			raise ValueError("enabled flag non-boolean")

	# return status byte
	def getStat(self):
		self.writeBytes("STATUS?")
		res = self.ser.readall()[0] # sends a single non-ascii value representing an 8 bit status register
		
		return res

	def getIDN(self):
		self.writeBytes('*IDN?')
		#return self.readN(17)
		return self.readAll() 

	def toFloat(self, b):
		try:
			return float(b)
		except:
			print(f"Weird output! : ({b}) of type {type(b)}")
			return float('nan')

if __name__ == '__main__':
	psu = TENMA('COM9')

	print(f"ID number: {psu.getIDN()}")
	sleep(1)
	while 1:
		print("Channel 1")
		print(f"Set point:\t\t{psu.getVset(1)}V\t|\t{psu.getIset(1)}A")
		print(f"Outputs:\t\t{psu.getVout(1)}V\t|\t{psu.getIout(1)}A")
		print()
		print("Channel 2")
		print(f"Set point:\t\t{psu.getVset(2)}V\t|\t{psu.getIset(2)}A")
		print(f"Outputs:\t\t{psu.getVout(2)}V\t|\t{psu.getIout(2)}A")
		print("----------------------------------------------")

		sleep(1)