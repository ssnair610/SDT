"""ANSI escape sequence-based formating of stream string data.
refer https://stackabuse.com/how-to-print-colored-text-in-python/
"""

__ENABLED__ = True
# __ENABLED__ = False

if __ENABLED__:

    class ANSIEscapeCodes:
        """ANSI escape sequence headers
        """
        hexadecimal = '\x1b['
        unicode = '\u001b['
        octal = '\033['

    class ANSIFormatMode:
        """ANSI escape sequence abstraction
        """
        def __init__(self, textcolor:int=0, bgcolor:int=-1, esccode:str=ANSIEscapeCodes.octal) -> None:
            self.__esc = esccode
            self.__txt = ';' + str(min(max(textcolor, 30), 37))

            if bgcolor == -1:
                self.__txt += 'm'
            elif bgcolor == 0:
                self.__txt += ';0m'
            else:
                self.__txt += ';' + str(min(max(bgcolor, 40), 47)) + 'm'

        def n(self) -> str:
            """normal style
            """
            return self.__esc + '0' + self.__txt

        def b(self) -> str:
            """bold style
            """
            return self.__esc + '1' + self.__txt

        def l(self) -> str:
            """light style
            """
            return self.__esc + '2' + self.__txt

        def i(self) -> str:
            """italic style
            """
            return self.__esc + '3' + self.__txt
        
        def u(self) -> str:
            """underlined style
            """
            return self.__esc + '4' + self.__txt

        def __str__(self) -> str:
            return self.n()

    class TextTag:
        """ANSCI text formating abstraction.\n\r
        Works as wrapper tags.
        """
        none = ANSIFormatMode(bgcolor=0)
        """reset/close
        """
        close = none
        """reset/close
        """
        error = ANSIFormatMode(textcolor=31)
        """red
        """
        warn = ANSIFormatMode(textcolor=33)
        """yellow
        """
        info = ANSIFormatMode(textcolor=32)
        """green
        """
        id = ANSIFormatMode(textcolor=36)
        """cyan
        """
        blue = ANSIFormatMode(textcolor=34)
        """blue
        """
        purp = ANSIFormatMode(textcolor=35)
        """purple
        """
        white = ANSIFormatMode(textcolor=37)
        """white
        """

else:
    class ANSIEscapeCodes:
        """ANSI escape sequence headers
        """
        hexadecimal = ''
        unicode = ''
        octal = ''

    class ANSIFormatMode:
        """ANSI escape sequence abstraction
        """
        def __init__(self, textcolor:int=0, bgcolor:int=-1, esccode:str=ANSIEscapeCodes.octal) -> None:
            pass

        def n(self) -> str:
            """normal style
            """
            return ''

        def b(self) -> str:
            """bold style
            """
            return ''

        def l(self) -> str:
            """light style
            """
            return ''

        def i(self) -> str:
            """italic style
            """
            return ''
        
        def u(self) -> str:
            """underlined style
            """
            return ''

        def __str__(self) -> str:
            return self.n()

    class TextTag:
        """ANSCI text formating abstraction.\n\r
        Works as wrapper tags.
        """
        none = ANSIFormatMode(bgcolor=0)
        """reset/close
        """
        close = none
        """reset/close
        """
        error = ANSIFormatMode(textcolor=31)
        """red
        """
        warn = ANSIFormatMode(textcolor=33)
        """yellow
        """
        info = ANSIFormatMode(textcolor=32)
        """green
        """
        id = ANSIFormatMode(textcolor=36)
        """cyan
        """
        blue = ANSIFormatMode(textcolor=34)
        """blue
        """
        purp = ANSIFormatMode(textcolor=35)
        """purple
        """
        white = ANSIFormatMode(textcolor=37)
        """white
        """