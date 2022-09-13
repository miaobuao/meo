'''
    Display input and output
'''

SYMBOL_PLAIN          = "\33[0m"
SYMBOL_CURSOR_HIDDEN  = "\33[?25l"
SYMBOL_CURSOR_DISPLAY = "\33[?25h"
SYMBOL_BLANKING       = "\33[8m"

FORMAT_FONT_BLACK    = "\33[30;1m{}\33[0m"
FORMAT_FONT_RED      = "\33[31;1m{}\33[0m"
FORMAT_FONT_GREEN    = "\33[32;1m{}\33[0m"
FORMAT_FONT_YELLOW   = "\33[33;1m{}\33[0m"
FORMAT_FONT_BLUE     = "\33[34;1m{}\33[0m"
FORMAT_FONT_PRUPLE   = "\33[35;1m{}\33[0m"
FORMAT_FONT_SKY_BLUE = "\33[36;1m{}\33[0m"
FORMAT_FONT_WHITE    = "\33[37;1m{}\33[0m"

FORMAT_BG_BLACK    = "\33[40;1m{}\33[0m"
FORMAT_BG_RED      = "\33[41;1m{}\33[0m"
FORMAT_BG_GREEN    = "\33[42;1m{}\33[0m"
FORMAT_BG_YELLOW   = "\33[43;1m{}\33[0m"
FORMAT_BG_BLUE     = "\33[44;1m{}\33[0m"
FORMAT_BG_PRUPLE   = "\33[45;1m{}\33[0m"
FORMAT_BG_SKY_BLUE = "\33[46;1m{}\33[0m"
FORMAT_BG_WHITE    = "\33[47;1m{}\33[0m"

FORMAT_UNDERLINE       = "\33[4m{}\33[0m"
FORMAT_TWINKLE         = "\33[5m{}\33[0m"
FORMAT_REVERSE_DISPLAY = "\33[7m{}\33[0m"
FORMAT_BLANKING        = "\33[8m{}\33[0m"

FORMAT_CURSOR_MOVE_UP    = "\33[{}A"
FORMAT_CURSOR_MOVE_DOWN  = "\33[{}B"
FORMAT_CURSOR_MOVE_RIGHT = "\33[{}C"
FORMAT_CURSOR_MOVE_LEFT  = "\33[{}D"

def red_font(text, end='\n'):
    '''print ```text``` red font'''
    print(FORMAT_FONT_RED.format(text), end=end)

def green_font(text, end="\n"):
    '''print ```text``` green font'''
    print(FORMAT_FONT_GREEN.format(text), end=end)

def blue_font(text, end="\n"):
    '''print ```text``` blue font'''
    print(FORMAT_FONT_BLUE.format(text), end=end)

def sformat(text, *styles):
    '''format string```text```'''
    for _s in styles:
        text = _s.format(text)
    return text

def clear_screen():
    '''clear screen'''
    print("\33[2J")

def hidden_input(__prompt: object):
    """ hidden keyboard input """
    text = input("{}{}{}".format(__prompt, SYMBOL_CURSOR_HIDDEN, SYMBOL_BLANKING))
    print("{}{}".format(SYMBOL_PLAIN, SYMBOL_CURSOR_DISPLAY), end='')
    return text

if __name__ == "__main__":

    # _text = sformat("hello world", FORMAT_BG_BLUE, FORMAT_FONT_YELLOW, FORMAT_UNDERLINE)
    # print(_text)
    # print(FORMAT_CURSOR_MOVE_UP.format(20))
    # clear_screen()
    # __psw = hidden_input("psw: ")
    # print(__psw)
    ...
