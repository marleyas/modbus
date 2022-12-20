public static int calculateCRC(byte[] bytes) {
  int crc = 0xFFFF;
  for (byte b : bytes) {
    crc = ((crc >>> 8) | (crc << 8)) & 0xffff;
    crc ^= (b & 0xff);
    crc ^= ((crc & 0xff) >> 4);
    crc ^= (crc << 12) & 0xffff;
    crc ^= ((crc & 0xFF) << 5) & 0xffff;
  }
  crc &= 0xffff;
  return crc;
}

# example:
byte[] bytes = { 0x01, 0x04, 0x00, 0x10, 0x00, 0x02 };
int crc = calculateCRC(bytes);
System.out.println(String.format("%04X", crc));
