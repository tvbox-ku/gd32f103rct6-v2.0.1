#ifndef __MODBUS_RTU_H__
#define __MODBUS_RTU_H__

#include <Arduino.h>

#define MODBUS_REG_COUNT 18

class ModbusRTU {
public:
  void begin(uint8_t addr, HardwareSerial &port, uint8_t deRePin);
  void poll();
  uint16_t holdingRegs[MODBUS_REG_COUNT];

private:
  uint8_t slaveAddr;
  HardwareSerial *port;
  uint8_t deRePin;
  uint8_t rxBuf[256];
  uint8_t rxLen;
  uint32_t lastRxMicros;
  uint16_t calcCrc(uint8_t *data, uint8_t len);
  void sendResponse(uint8_t *data, uint8_t len);
  void sendException(uint8_t func, uint8_t code);
  void processFrame();
};

extern ModbusRTU modbus;

#endif
