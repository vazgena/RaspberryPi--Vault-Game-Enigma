#include <FastLED.h>

FASTLED_USING_NAMESPACE

// FastLED "100-lines-of-code" demo reel, showing just a few 
// of the kinds of animation patterns you can quickly and easily 
// compose using FastLED.  
//
// This example also shows one easy way to define multiple 
// animations patterns and have them automatically rotate.
//
// -Mark Kriegsman, December 2014

#if defined(FASTLED_VERSION) && (FASTLED_VERSION < 3001000)
#warning "Requires FastLED 3.1 or later; check github for latest code."
#endif

#define DATA_PIN    3
//#define CLK_PIN   4
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    50
CRGB leds[NUM_LEDS];
extern const TProgmemPalette16 RedPalette PROGMEM;
extern const TProgmemPalette16 GreenPalette PROGMEM;
extern const TProgmemPalette16 BluePalette PROGMEM;
extern const TProgmemPalette16 YellowPalette PROGMEM;
extern const TProgmemPalette16 PurplePalette PROGMEM;
CRGBPalette16 currentPalette;
TBlendType    currentBlending;
#define playtime 1500
#define over_number 1000
#define over_number2 300

#define BRIGHTNESS          96
#define FRAMES_PER_SECOND  1200
#define rainbow_ms_delay 75

uint8_t gCurrentPatternNumber = 0; // Index number of which pattern is current
uint8_t gHue = 0; // rotating "base color" used by many of the patterns


void setup() {
  Serial.begin(9600);
  Serial.println("Loaded Controller");
  delay( 3000 ); // power-up safety delay
  delay(3000); // 3 second delay for recovery
  
  // tell FastLED about the LED strip configuration
  FastLED.addLeds<LED_TYPE,DATA_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  //FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  // set master brightness control
  FastLED.setBrightness(BRIGHTNESS);
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; /* motion speed */
  
  FillLEDsFromPaletteColors(startIndex);
  
  FastLED.show();
  FastLED.delay(over_number / FRAMES_PER_SECOND);
}


void loop()
{
  // Call the current pattern function once, updating the 'leds' array
  rainbow();
  // send the 'leds' array out to the actual LED strip
  FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(over_number/FRAMES_PER_SECOND); 
  // do some periodic updates
  if (Serial.available() > 0) {
    String incomingByte = Serial.readString();
    if (incomingByte == String('r')){
          Serial.println("red");
          playpattern("r");
    }
    if (incomingByte == String('g')){
          Serial.println("green");
          playpattern("g");
    }
    if (incomingByte == String('b')){
          Serial.println("blue");
          playpattern("b");
    }
    if (incomingByte == String('p')){
          Serial.println("purple");
          playpattern("p");
    }
    if (incomingByte == String('y')){
          Serial.println("yellow");
          playpattern("y");
    }
  }

}



void playpattern(String color){
  for(int i = 0; i < playtime; i++) {
    static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    
    FastLED.show();
    FastLED.delay(over_number2 / FRAMES_PER_SECOND);
    if (color == String('r')){
      currentPalette = RedPalette; 
    }
    if (color == String('b')){
      currentPalette = BluePalette; 
    }
    if (color == String('g')){
      currentPalette = GreenPalette; 
    }
    
    if (color == String('y')){
      currentPalette = YellowPalette; 
    }
    if (color == String('p')){
      currentPalette = PurplePalette; 
    }
    currentBlending = NOBLEND;
    fadeall();
  }
}


void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}




void fadeall() { for(int i = 0; i < NUM_LEDS; i++) { leds[i].nscale8(250); } }


void rainbow() 
{
  EVERY_N_MILLISECONDS( rainbow_ms_delay ) { gHue++; } // slowly cycle the "base color" through the rainbow
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, gHue, 7);
}

const TProgmemPalette16 BluePalette PROGMEM =
{
    CRGB::Blue,
    CRGB::Blue, 
    CRGB::Blue,
    CRGB::Blue,
    
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Blue,
    
    CRGB::Blue,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black
};

const TProgmemPalette16 YellowPalette PROGMEM =
{
    CRGB::Yellow,
    CRGB::Yellow, 
    CRGB::Yellow,
    CRGB::Yellow,
    
    CRGB::Yellow,
    CRGB::Yellow,
    CRGB::Yellow,
    CRGB::Yellow,
    
    CRGB::Yellow,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black
};

const TProgmemPalette16 RedPalette PROGMEM =
{
    CRGB::Red,
    CRGB::Red, 
    CRGB::Red,
    CRGB::Red,
    
    CRGB::Red,
    CRGB::Red,
    CRGB::Red,
    CRGB::Red,
    
    CRGB::Red,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black
};

const TProgmemPalette16 GreenPalette PROGMEM =
{
    CRGB::Green,
    CRGB::Green,
    CRGB::Green,
    CRGB::Green,
    
    CRGB::Green,
    CRGB::Green,
    CRGB::Green,
    CRGB::Green,
    
    CRGB::Green,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black
};

const TProgmemPalette16 PurplePalette PROGMEM =
{
    CRGB::Purple,
    CRGB::Purple, 
    CRGB::Purple,
    CRGB::Purple,
    
    CRGB::Purple,
    CRGB::Purple,
    CRGB::Purple,
    CRGB::Purple,
    
    CRGB::Purple,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black,
    CRGB::Black
};
