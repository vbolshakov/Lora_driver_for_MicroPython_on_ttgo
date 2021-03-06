from machine import Pin, SPI, reset

from sx127x import config
from sx127x.controller import base_controller

class ESPController(base_controller.BaseController):

    # LoRa config
    LORA_RESET = 4

    LORA_CS = 15
    LORA_SCK = 14
    LORA_MOSI = 13
    LORA_MISO = 12

    PIN_ID_FOR_LORA_DI01 = 5
    LORA_DIO1 = None
    LORA_DIO2 = None
    LORA_DIO3 = None
    LORA_DIO4 = None
    LORA_DIO5 = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def prepare_pin(self, pin_id, in_out = Pin.OUT):
        if pin_id:
            pin = Pin(pin_id, in_out)
            return pin
        return None


    def prepare_irq_pin(self, pin_id):
        return self.prepare_pin(pin_id, in_out=Pin.IN)

    def prepare_spi(self, spi):
        if spi:
            return spi

    def __exit__(self):
        self.spi.deinit()



class ESP32Controller(ESPController):

    # LoRa config
    LORA_RESET = 4

    LORA_CS = 15
    LORA_SCK = 14
    LORA_MOSI = 13
    LORA_MISO = 12

    LORA_DIO0 = 5
    LORA_DIO1 = None
    LORA_DIO2 = None
    LORA_DIO3 = None
    LORA_DIO4 = None
    LORA_DIO5 = None
    
    

    ON_BOARD_LED_PIN_NO = 2
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                 12, 13, 14, 15, 16, 17, 18, 19, 21, 22,
                 23, 25, 26, 27, 32, 34, 35, 36, 37, 38, 39)

    
    def __init__(self,   
                 pin_id_led = ON_BOARD_LED_PIN_NO,
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5)):
                
        super().__init__(pin_id_led,
                         on_board_led_high_is_on,
                         pin_id_reset,
                         blink_on_start)


    def get_spi(self): 

        if config.CONFIG.SOFT_SPI:
            spi_id = -1
        else:
            spi_id = 1

        try:
            spi = SPI(spi_id, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                      sck = Pin(self.LORA_SCK, Pin.OUT, Pin.PULL_DOWN),
                      mosi = Pin(self.LORA_MOSI, Pin.OUT, Pin.PULL_UP),
                      miso = Pin(self.LORA_MISO, Pin.IN, Pin.PULL_UP))
            spi.init()

        except Exception as e:
            print(e)
            if spi:
                spi.deinit()
            reset()  # in case SPI is already in use, need to reset.
            raise

        return spi
        
            
class ESP8266Controller(ESPController):

    # LoRa config
    LORA_RESET = 4

    LORA_CS = 15
    LORA_SCK = 14
    LORA_MOSI = 13
    LORA_MISO = 12

    LORA_DIO0= 5
    LORA_DIO1 = None
    LORA_DIO2 = None
    LORA_DIO3 = None
    LORA_DIO4 = None
    LORA_DIO5 = None


    ON_BOARD_LED_PIN_NO = 2
    ON_BOARD_LED_HIGH_IS_ON = False
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)

    def __init__(self,
                 pin_id_led = ON_BOARD_LED_PIN_NO,
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5)):

        super().__init__(pin_id_led,
                         on_board_led_high_is_on,
                         pin_id_reset,
                         blink_on_start)


    def get_spi(self):
        spi = None
        spi_id = 1

        spi = SPI(spi_id, baudrate = 10000000, polarity = 0, phase = 0)
        spi.init()
        return spi


