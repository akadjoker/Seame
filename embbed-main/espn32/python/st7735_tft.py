import time
from typing import Union, Iterable
from PIL import Image, ImageChops
import numpy as np
import spidev

try:
    import pigpio
    LIB_PIGPIO = True
except ImportError:
    LIB_PIGPIO = False
try:
    import RPi.GPIO
    LIB_RPIGPIO = True
except ImportError:
    LIB_RPIGPIO = False


class ST7735_TFT:
    ###
    # System function Command
    ST7735_NOP = 0x00           # No operation
    ST7735_SWRESET = 0x01       # Software reset
    ST7735_RDDID = 0x04         # Read Display ID
    ST7735_RDDST = 0x09         # Read Display Status

    ST7735_SLPIN = 0x10         # Sleep in & booster off
    ST7735_SLPOUT = 0x11        # Sleep out & booster on
    ST7735_PTLON = 0x12         # Partial mode on
    ST7735_NORON = 0x13         # Partial off (Normal)

    ST7735_INVOFF = 0x20        # Display inversion off
    ST7735_INVON = 0x21         # Display inversion on
    ST7735_DISPOFF = 0x28       # Display off
    ST7735_DISPON = 0x29        # Display on

    ST7735_CASET = 0x2A         # Column address set
    ST7735_RASET = 0x2B         # Row address set
    ST7735_RAMWR = 0x2C         # Memory write
    ST7735_RAMRD = 0x2E         # Memory read

    ST7735_PTLAR = 0x30         # Partial start/end address set
    ST7735_MADCTL = 0x36        # Memory data access control
    ST7735_COLMOD = 0x3A        # Interface pixel format

    ###
    # Panel Function Commands
    ST7735_FRMCTR1 = 0xB1       # Frame Rate Control (In normal mode/ Full colors)
    ST7735_FRMCTR2 = 0xB2       # Frame Rate Control (In Idle mode/ 8-colors)
    ST7735_FRMCTR3 = 0xB3       # Frame Rate Control (In Partial mode/ full colors)
    ST7735_INVCTR = 0xB4        # Display Inversion Control
    ST7735_DISSET5 = 0xB6       # Display Function set 5

    ST7735_PWCTR1 = 0xC0        # Power control 1
    ST7735_PWCTR2 = 0xC1        # Power control 2
    ST7735_PWCTR3 = 0xC2        # Power control 3 (in Normal mode/ Full colors)
    ST7735_PWCTR4 = 0xC3        # Power control 4 (in Idle mode/ 8-colors)
    ST7735_PWCTR5 = 0xC4        # Power control 5 (in Partial mode/ full-colors)
    ST7735_PWCTR6 = 0xFC        # Power Control 6 (Gamma control adjust)
    ST7735_VMCTR1 = 0xC5        # VCOM Control 1

    ST7735_GMCTRP1 = 0xE0       # Gamma ('+'polarity) Correction Characteristics
    ST7735_GMCTRN1 = 0xE1       # Gamma ('-'polarity) Correction Characteristics

    DC_DATA = 1
    DC_COMMAND = 0

    ST7735_COLS = 132
    ST7735_ROWS = 162

    ROTATION_METHODS = {
        90: Image.ROTATE_90,
        180: Image.ROTATE_180,
        270: Image.ROTATE_270
    }

    def __init__(self, port: int, cs: int, dc: int, bl: int = None, rst: int = None,
                 width=80, height=160, rotation=90, offset_left=None, offset_top=None,
                 invert=True, spi_speed_hz=4000000, **kwargs):

        # Setup SPI
        self._spi = spidev.SpiDev(port, cs)
        self._spi.max_speed_hz = spi_speed_hz
        self._spi.mode = 0
        self._spi.lsbfirst = False

        # Setup I/O
        self.iolib = None       # type: str
        if LIB_PIGPIO:
            self.pi = pigpio.pi(**kwargs.get('pigpio_args', {}), show_errors=False)
            if self.pi.connected:
                self.iolib = 'pigpio'
        if LIB_RPIGPIO and self.iolib is None:
            RPi.GPIO.setwarnings(False)
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            self.iolib = 'rpi.gpio'
        if self.iolib is None:
            raise ImportError('No compatible IO module found! (Install \'pigpio\' or \'RPi.GPIO\')')
        print('Using {} library'.format(self.iolib))

        self._dc = dc
        self.set_io_mode(self._dc, 'O')
        self._bl = bl
        if self._bl is not None:
            self.set_io_mode(self._bl, 'O')
            self.set_io_state(self._bl, 1)
        self._rst = rst
        if self._rst is not None:
            self.set_io_mode(self._rst, 'O')

        # Display information
        self._width = width
        self._height = height
        self._rotation = rotation
        if self._rotation not in [0,90,180,270]:
            raise ValueError("'rotation' should be one of [0,90,180,270]")
        # Default left offset to center display
        if offset_left is None:
            offset_left = (self.ST7735_COLS - width) // 2
        self._offset_left = offset_left

        # Default top offset to center display
        if offset_top is None:
            offset_top = (self.ST7735_ROWS - height) // 2
        self._offset_top = offset_top
        self._invert = invert

        self._image = None          # type: Image
        self._init()

    def begin(self):
        pass

    def set_io_mode(self, pin: int, mode: str):
        assert mode in ['i', 'I', 'o', 'O'], "Mode should either be 'I' or 'O'"
        mode = mode.upper()
        if self.iolib == 'pigpio':
            self.pi.set_mode(pin, pigpio.INPUT if mode == 'I' else pigpio.OUTPUT)
        elif self.iolib == 'rpi.gpio':
            RPi.GPIO.setup(pin, RPi.GPIO.IN if mode == 'I' else RPi.GPIO.OUT)

    def set_io_state(self, pin: int, state: Union[bool, int]):
        if self.iolib == 'pigpio':
            self.pi.write(pin, state)
        elif self.iolib == 'rpi.gpio':
            RPi.GPIO.output(pin, RPi.GPIO.HIGH if state else RPi.GPIO.LOW)

    def set_backlight(self, value):
        """Set the backlight on/off."""
        if self._bl is not None:
            self.set_io_state(self._bl, value)

    @property
    def width(self):
        return self._width if self._rotation == 0 or self._rotation == 180 else self._height

    @property
    def height(self):
        return self._height if self._rotation == 0 or self._rotation == 180 else self._width

    def send(self, data: Union[Iterable, bytes, int], is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        # Set DC low for command, high for data.
        self.set_io_state(self._dc, self.DC_DATA if is_data else self.DC_COMMAND)
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, int):
            data = [data & 0xFF]
        # Write data a chunk at a time.
        for start in range(0, len(data), chunk_size):
            end = min(start + chunk_size, len(data))
            self._spi.xfer(data[start:end])

    def send_framedata(self, data: Union['np.ndarray', Iterable[Union[int, bytes]]]):
        """ Write pixel data to LCD
        :param data: The pixel data to send (565 RGB)
        """
        self.command(self.ST7735_RAMWR)
        self.set_io_state(self._dc, self.DC_DATA)
        self._spi.writebytes2(data)

    def command(self, data):
        """Write a byte or array of bytes to the display as command data."""
        self.send(data, False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send(data, True)

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            self.set_io_state(self._rst, 1)
            time.sleep(0.500)
            self.set_io_state(self._rst, 0)
            time.sleep(0.500)
            self.set_io_state(self._rst, 1)
            time.sleep(0.500)
            self._image = None

    def _init(self):
        # Initialize the display.
        self.command(self.ST7735_SWRESET)       # Software reset
        time.sleep(0.150)                           # delay 150 ms

        self.command(self.ST7735_SLPOUT)        # Out of sleep mode
        time.sleep(0.500)                           # delay 500 ms

        self.command(self.ST7735_FRMCTR1)       # Frame rate ctrl - normal mode
        self.data([0x01, 0x2C, 0x2D])

        self.command(self.ST7735_FRMCTR2)       # Frame rate ctrl - idle mode
        self.data([0x01, 0x2C, 0x2D])

        self.command(self.ST7735_FRMCTR3)       # Frame rate ctrl - partial mode
        self.data([0x01, 0x2C, 0x2D,                # Dot inversion mode
                   0x01, 0x2C, 0x2D])               # Line inversion mode

        self.command(self.ST7735_INVCTR)        # Display inversion ctrl
        self.data([0x07])                           # No inversion

        self.command(self.ST7735_PWCTR1)        # Power control
        self.data([0xA2, 0x02, 0x84])               # -4.6V, auto mode

        self.command(self.ST7735_PWCTR2)        # Power control
        self.data([0x0A, 0x00])                     # Opamp current small, boost freq

        self.command(self.ST7735_PWCTR4)        # Power control
        self.data([0x8A, 0x2A])                     # BCLK/2, Opamp current small & Medium low

        self.command(self.ST7735_PWCTR5)        # Power control
        self.data([0x8A, 0xEE])

        self.command(self.ST7735_VMCTR1)        # Power control
        self.data([0x0E])

        if self._invert:
            self.command(self.ST7735_INVON)     # Invert display
        else:
            self.command(self.ST7735_INVOFF)    # Don't invert display

        self.command(self.ST7735_MADCTL)        # Memory access control (directions)
        self.data([0xC8])                           # row addr/col addr, bottom to top refresh

        self.command(self.ST7735_COLMOD)        # set color mode
        self.data([0x05])                           # 16-bit color

        self.command(self.ST7735_CASET)         # Column addr set
        self.data([0x00, self._offset_left,
                   0x00, self._width + self._offset_left - 1])

        self.command(self.ST7735_RASET)         # Row addr set
        self.data([0x00, self._offset_top,
                   0x00, self._height + self._offset_top - 1])

        self.command(self.ST7735_GMCTRP1)       # Set Gamma
        self.data([0x02, 0x1c, 0x07, 0x12,
                   0x37, 0x32, 0x29, 0x2d,
                   0x29, 0x25, 0x2B, 0x39,
                   0x00, 0x01, 0x03, 0x10])

        self.command(self.ST7735_GMCTRN1)       # Set Gamma
        self.data([0x03, 0x1d, 0x07, 0x06,
                   0x2E, 0x2C, 0x29, 0x2D,
                   0x2E, 0x2E, 0x37, 0x3F,
                   0x00, 0x00, 0x02, 0x10])

        self.command(self.ST7735_NORON)         # Normal display on
        time.sleep(0.010)                           # 10 ms

        self.command(self.ST7735_DISPON)        # Display on
        time.sleep(0.100)                           # 100 ms

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to width-1,height-1.
        """
        if x1 is None:
            x1 = self._width - 1

        if y1 is None:
            y1 = self._height - 1

        y0 += self._offset_top
        y1 += self._offset_top

        x0 += self._offset_left
        x1 += self._offset_left

        self.command(self.ST7735_CASET)       # Column addr set
        self.data(x0 >> 8)
        self.data(x0)                    # XSTART
        self.data(x1 >> 8)
        self.data(x1)                    # XEND
        self.command(self.ST7735_RASET)       # Row addr set
        self.data(y0 >> 8)
        self.data(y0)                    # YSTART
        self.data(y1 >> 8)
        self.data(y1)                    # YEND
        self.command(self.ST7735_RAMWR)       # write to RAM

    @staticmethod
    def image_to_data(image: Image.Image):
        """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
        # NumPy is much faster at doing this. NumPy code provided by:
        # Keith (https://www.blogger.com/profile/02555547344016007163)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        pb = np.array(image).astype('uint16')
        color = ((pb[:, :, 0] & 0xF8) << 8) | ((pb[:, :, 1] & 0xFC) << 3) | (pb[:, :, 2] >> 3)
        return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).astype('uint8').flatten().tolist()

    def display(self, image: Image.Image, full_update=False):
        """Write the provided image to the hardware.

        :param image: Should be RGB format and the same dimensions as the display hardware.
        :param full_update: If True, send pixel data of whole screen. Else, only update changed pixels
        """
        image = image.copy()
        w, h = image.size
        if w != self.width or h != self.height:
            raise ValueError('Image should be the same size as the display! ({}, {})'.format(self.width, self.height))
        if image.mode != 'RGB':
            image = image.convert('RGB')

        if self._rotation != 0:
            image = image.transpose(self.ROTATION_METHODS[self._rotation])
        else:
            image = image.copy()

        if full_update or self._image is None:
            self.set_window()
            self._image = image
        else:
            bbox = ImageChops.difference(image, self._image).getbbox()
            if bbox is None:
                # Image is same as is already being displayed, skip update
                return
            x0, y0, x1, y1 = bbox
            self.set_window(x0, y0, x1-1, y1-1)
            self._image = image
            image = image.crop(bbox)

        # Convert image to array of 16bit 565 RGB data bytes.
        # Unfortunate that this copy has to occur, but the SPI byte writing
        # function needs to take an array of bytes and PIL doesn't natively
        # store images in 16-bit 565 RGB format.
        pixelbytes = self.image_to_data(image)
        # Write data to hardware.
        self.send_framedata(pixelbytes)
