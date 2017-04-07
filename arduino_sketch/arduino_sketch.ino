#include <Adafruit_NeoPixel.h>
#include "declaration_workaround.h"

#define COMMAND_MASK 0xc0
#define COMMAND_OFFSET 6
#define DATA_MASK 0x3f

#define BUILDINFO_STATUS_MASK 0x03
#define BUILDINFO_BUILDING_MASK 0x04

#define HISTORY_SIZE 30

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(HISTORY_SIZE, 7, NEO_GRB + NEO_KHZ800);

Status history[HISTORY_SIZE];
char progress;
char building;
unsigned long lastFrameTime;

void setup() {
  Serial.begin(115200);
  
  for (int i = 0; i < HISTORY_SIZE; i++)
    history[i] = STATUS_OK;
  history[0] = STATUS_FAILURE;
  building = 0;
  progress = 0;
  lastFrameTime = millis();
  pixels.begin();
}

void serialEvent(){
  while (Serial.available()) {
    char c = (char)Serial.read();
    enum Command cmd = (enum Command)((c & COMMAND_MASK) >> COMMAND_OFFSET);
    int data = c & DATA_MASK;
    switch (cmd) {
      case COMMAND_NEW_BUILD:
        for (int i = HISTORY_SIZE - 2; i >= 0; i--)
          history[i + 1] = history[i];
        history[0] = (enum Status)(data & BUILDINFO_STATUS_MASK);
        building = !!(data & BUILDINFO_BUILDING_MASK);
        progress = 0;
        break;
      case COMMAND_PROGRESS:
        progress = data;
        break;
      case COMMAND_MODE:
        break;
      case COMMAND_BUILD_DONE:
        building = 0;
        history[0] = (enum Status)(data & BUILDINFO_STATUS_MASK);
        break;
    }
    Serial.write(c);
  }
}

void loop() {
  unsigned long newTime = millis();
  if (newTime - lastFrameTime > 20) {
    renderLastBuild(newTime);
    renderHistory(newTime);
    pixels.show();
    lastFrameTime = newTime;
  }
}

uint32_t getColor(enum Status status, uint8_t s) {
  return 
    status == STATUS_UNKNOWN ? Adafruit_NeoPixel::Color(0, 0, 0) :
    status == STATUS_OK      ? Adafruit_NeoPixel::Color(0, s, 0) :
    status == STATUS_IFFY    ? Adafruit_NeoPixel::Color(s, s, 0) :
    status == STATUS_FAILURE ? Adafruit_NeoPixel::Color(s, 0, 0) :
                               Adafruit_NeoPixel::Color(0, 0, s); // Should never happen
}

void renderLastBuild(unsigned long time) {
  unsigned long animationState = time % 3000;  
  uint8_t s = (255 * animationState) / 3000;
  if (s <= 128) {
    // ramp up
    s = min(255, 2 * s);
  } else {
    // ramp down
    s = 255 - 2 * s;
  }
  enum Status status = history[0];
  uint32_t color = getColor(status, s);
  
  pixels.setPixelColor(0, color);
}

void renderHistory(unsigned long time) {
  for (int i = 1; i < HISTORY_SIZE; i++) {
    enum Status status = history[i];
    uint8_t s = 180;
    uint32_t color = getColor(status, s);
  
    pixels.setPixelColor(i, color);
  }
}

