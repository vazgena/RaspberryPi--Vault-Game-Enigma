#include <FastLED.h>


#define LED_PIN           3
#define NUM_LEDS          140
#define LED_TYPE          WS2812B
#define COLOR_ORDER       GRB


// variables
int BRIGHTNESS = 255;
int minnum = 3;
int maxnum = 6;
int rl = 255;
int gl = 176;
int bl = 0;
int ru = 0;
int gu = 0;
int bu = 0;
int upperLeds = 77;
CRGB leds[NUM_LEDS];


// initial setup
void setup() {
    // start serial 
    Serial.begin(9600);
    Serial.println("Loaded Controller");
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB( ru, gu, bu); 
        }
        FastLED.show();
    for(int led = 77; led < NUM_LEDS; led++) { 
            leds[led] = CRGB( rl, gl, bl); 
        }
        FastLED.show();
}


// loop function
void loop() {
  if (Serial.available() > 0) {
      String incomingByte = Serial.readString();
      // brigntness of all LEDs adjust
      if(incomingByte == String('v')){
        Serial.println("bright ready");
        while(!Serial.available()){
            BRIGHTNESS = Serial.parseInt(); 
        }
        Serial.println(BRIGHTNESS);
        FastLED.setBrightness(BRIGHTNESS);
        runcolor();
      }
      // lower LEDs adjust
      if(incomingByte == String('l')){
        Serial.println("lower ready");
        while(!Serial.available()){
            rl = Serial.parseInt();
        }
        incomingByte = Serial.readString();
        while(!Serial.available()){
            gl = Serial.parseInt();
        }
        incomingByte = Serial.readString();
        while(!Serial.available()){
            bl = Serial.parseInt();
        }
        Serial.println(rl);
        Serial.println(gl);
        Serial.println(bl);
        for(int led = 77; led < NUM_LEDS; led++) { 
          leds[led] = CRGB( rl, gl, bl);
        }
        runcolor();
      } 
      // upper LEDs adjust
      if (incomingByte == String('u')){
        Serial.println("upper ready");
        incomingByte = Serial.readString();
        while(!Serial.available()){
            ru = Serial.parseInt();
        }
        incomingByte = Serial.readString();
        while(!Serial.available()){
            gu = Serial.parseInt();
        }
        incomingByte = Serial.readString();
        while(!Serial.available()){
            bu = Serial.parseInt();
        }
        Serial.println("3 entered");
        Serial.println(ru);
        Serial.println(gu);
        Serial.println(bu);
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB( ru, gu, bu);
        }
        runcolor();
      }
      // red top
      if (incomingByte == String('r')){
        Serial.println("red");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB( 175, 0, 0);
        }
        runcolor();
      }
      // yellow top
      if (incomingByte == String('y')){
        Serial.println("yellow");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(175,255,0);
        }
        runcolor();
      }
      
      // white top
      if (incomingByte == String('w')){
        Serial.println("white");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(175,255,255);
        }
        runcolor();
      }
      // green top
      if (incomingByte == String('g')){
        Serial.println("green");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(0,255,0);
        }
        runcolor();
      }
      if (incomingByte == String('p')){
        Serial.println("purple");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(100,0,255);
        }
        runcolor();
      }
      // blue top
      if (incomingByte == String('b')){
        Serial.println("blue");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(0,0,255);
        }
        runcolor();
      }
      //no light top
       if (incomingByte == String('n')){
        Serial.println("off");
        for(int led = 0; led < upperLeds; led++) { 
            leds[led] = CRGB(0,0,0);
        }
        runcolor();
      }
   }
}


void runcolor() {
    delay(10);
    Serial.println("Color Ran");
    FastLED.show();
}
