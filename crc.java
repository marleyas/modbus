#include <cstdint>

uint16_t calculateCRC(uint8_t* data, size_t length) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < length; i++) {
    crc = ((crc >> 8) | (crc << 8)) & 0xFFFF;
    crc ^= data[i];
    crc ^= (crc & 0xFF) >> 4;
    crc ^= (crc << 12) & 0xFFFF;
    crc ^= ((crc & 0xFF) << 5) & 0xFFFF;
  }
  crc &= 0xFFFF;
  return crc;
}


# example:
uint8_t data[] = { 0x01, 0x04, 0x00, 0x10, 0x00, 0x02 };
size_t length = sizeof(data) / sizeof(data[0]);
uint16_t crc = calculateCRC(data, length);
printf("%04X\n", crc);
