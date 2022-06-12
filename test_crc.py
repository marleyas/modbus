
def calc_crc(data):
    '''
    Calcula o CRC para comunicação ModBus
    Retorna uma string com os 2 bytes do CRC
    '''
    crc = 0xFFFF
    for pos in data:
        crc ^= pos 
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    crc = str("%04X"%(crc))
    return crc[2:] + crc[:2]
    
    	
if __name__ == '__main__':
	data = bytearray.fromhex("010300010001")
	crc = calc_crc(data)
	print(crc)
