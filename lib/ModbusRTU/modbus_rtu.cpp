#include "modbus_rtu.h"

ModbusRTU modbus;

void ModbusRTU::begin(uint8_t addr, HardwareSerial &port, uint8_t deRePin) {
  slaveAddr = addr;
  this->port = &port;
  this->deRePin = deRePin;
  rxLen = 0;
  lastRxMicros = 0;
  memset(holdingRegs, 0, sizeof(holdingRegs));
  pinMode(deRePin, OUTPUT);
  digitalWrite(deRePin, LOW);
}

uint16_t ModbusRTU::calcCrc(uint8_t *data, uint8_t len) {
  uint16_t crc = 0xFFFF;
  for (uint8_t i = 0; i < len; i++) {
    crc ^= data[i];
    for (uint8_t j = 0; j < 8; j++) {
      if (crc & 0x0001) crc = (crc >> 1) ^ 0xA001;
      else crc >>= 1;
    }
  }
  return crc;
}

void ModbusRTU::sendResponse(uint8_t *data, uint8_t len) {
  uint16_t crc = calcCrc(data, len);
  digitalWrite(deRePin, HIGH);
  port->write(data, len);
  port->write((uint8_t)(crc & 0xFF));
  port->write((uint8_t)(crc >> 8));
  port->flush();
  digitalWrite(deRePin, LOW);
}

void ModbusRTU::sendException(uint8_t func, uint8_t code) {
  uint8_t buf[3];
  buf[0] = slaveAddr;
  buf[1] = func | 0x80;
  buf[2] = code;
  sendResponse(buf, 3);
}

void ModbusRTU::processFrame() {
  if (rxLen < 4) { rxLen = 0; return; }

  uint16_t crc = calcCrc(rxBuf, rxLen - 2);
  uint16_t rxCrc = rxBuf[rxLen - 2] | (rxBuf[rxLen - 1] << 8);
  if (crc != rxCrc) { rxLen = 0; return; }

  if (rxBuf[0] != slaveAddr) { rxLen = 0; return; }

  uint8_t func = rxBuf[1];

  if (func == 0x03) {
    if (rxLen != 8) { rxLen = 0; return; }
    uint16_t startAddr = (rxBuf[2] << 8) | rxBuf[3];
    uint16_t regCount = (rxBuf[4] << 8) | rxBuf[5];
    if (regCount == 0 || startAddr + regCount > MODBUS_REG_COUNT) {
      sendException(func, 0x02); rxLen = 0; return;
    }
    uint8_t resp[256];
    resp[0] = slaveAddr;
    resp[1] = 0x03;
    resp[2] = regCount * 2;
    for (uint16_t i = 0; i < regCount; i++) {
      resp[3 + i * 2] = holdingRegs[startAddr + i] >> 8;
      resp[4 + i * 2] = holdingRegs[startAddr + i] & 0xFF;
    }
    sendResponse(resp, 3 + regCount * 2);
  } else if (func == 0x06) {
    if (rxLen != 8) { rxLen = 0; return; }
    uint16_t addr = (rxBuf[2] << 8) | rxBuf[3];
    uint16_t val = (rxBuf[4] << 8) | rxBuf[5];
    if (addr >= MODBUS_REG_COUNT) { sendException(func, 0x02); rxLen = 0; return; }
    holdingRegs[addr] = val;
    sendResponse(rxBuf, 6);
  } else if (func == 0x10) {
    if (rxLen < 11) { rxLen = 0; return; }
    uint16_t startAddr = (rxBuf[2] << 8) | rxBuf[3];
    uint16_t regCount = (rxBuf[4] << 8) | rxBuf[5];
    uint8_t byteCount = rxBuf[6];
    if (regCount == 0 || startAddr + regCount > MODBUS_REG_COUNT) {
      sendException(func, 0x02); rxLen = 0; return;
    }
    if (rxLen != 9 + byteCount) { rxLen = 0; return; }
    for (uint16_t i = 0; i < regCount; i++) {
      holdingRegs[startAddr + i] = (rxBuf[7 + i * 2] << 8) | rxBuf[8 + i * 2];
    }
    uint8_t resp[6];
    resp[0] = slaveAddr;
    resp[1] = 0x10;
    resp[2] = rxBuf[2]; resp[3] = rxBuf[3];
    resp[4] = rxBuf[4]; resp[5] = rxBuf[5];
    sendResponse(resp, 6);
  } else {
    sendException(func, 0x01);
  }

  rxLen = 0;
}

void ModbusRTU::poll() {
  while (port->available()) {
    if (rxLen < 255) {
      rxBuf[rxLen++] = port->read();
      lastRxMicros = micros();
    } else {
      port->read();
    }
  }
  if (rxLen > 0 && (micros() - lastRxMicros) > 1000) {
    processFrame();
  }
}
