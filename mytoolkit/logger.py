"""text for logger.py
"""
from txttag import TextTag as tag

class Logger:
    """logger system
    """

    class LogTag:
        class Enum:
            def __init__(self, enum:int = 0) -> None:
                self.__enum = enum
            
            def __int__(self) -> int:
                return self.__enum

        error = Enum(6)
        warn = Enum(4)
        info = Enum(2)
        flavor = Enum(0)

    @ staticmethod
    def autotag(tag_profile:LogTag.Enum, exttag:int, arg:str) -> str:
        message = arg
        procsymb = "[+]" if exttag == 0 else "[*]" if exttag == 1 else "[-]" if exttag == 2 else ""
        if tag_profile == Logger.LogTag.error:
            message = f"{tag.error.b()}{procsymb}{tag.error}" + message + f"{tag.close}\r\n"
        
        elif tag_profile == Logger.LogTag.warn:
            message = f"{tag.warn.b()}{procsymb}{tag.warn}" + message + f"{tag.close}\r\n"
        
        elif tag_profile == Logger.LogTag.info:
            message = f"{tag.info.b()}{procsymb}{tag.info}" + message + f"{tag.close}\r\n"
        
        elif tag_profile == Logger.LogTag.flavor:
            message = f"{tag.white.b()}{procsymb}{tag.white}" + message + f"{tag.close}\r\n"
        
        return message

    def __init__(self, severity:LogTag.Enum = LogTag.flavor, automateFlush = True, outstream = lambda tag, x: print(x)) -> None:
        self.__log_stacks:dict = {
            Logger.LogTag.error : '',
            Logger.LogTag.warn : '',
            Logger.LogTag.info : '',
            Logger.LogTag.flavor : f'{tag.info.b()}[+]{tag.info} logger initialized.{tag.close}\r\n'
        }

        self.__aflush = automateFlush
        self.__severity = severity
        self.__preproc = Logger.autotag
        self.__outsteam = outstream

    def log(self, *args, tag_profile:LogTag.Enum = LogTag.flavor, exttag:int=-1) -> None:
        if self.__aflush:
            if int(tag_profile) < int(self.__severity):
                self.__outsteam(tag=tag_profile, x=self.__preproc(arg='\r\n'.join(args), tag_profile=tag_profile, exttag=exttag))

        else:
            try:
                self.__log_stacks[tag] += self.__preproc(arg='\r\n'.join(args), tag_profile=tag_profile, exttag=exttag)
            except KeyError:
                raise KeyError("tag profile not found")
    
    def logs(self, args:str, tag_profile:LogTag.Enum = LogTag.flavor, exttag:int=-1) -> None:
        if self.__aflush:
            if int(tag_profile) < int(self.__severity):
                self.__outsteam(tag=tag_profile, x=self.__preproc(arg=args + '\r\n', tag_profile=tag_profile, exttag=exttag))

        else:
            try:
                self.__log_stacks[tag] += self.__preproc(arg=args+'\r\n', tag_profile=tag_profile, exttag=exttag)
            except KeyError:
                raise KeyError("tag profile not found")
    
    def addProfile(self, severity:int) -> LogTag.Enum:
        profile = Logger.LogTag.Enum(severity)
        self.__log_stacks[profile] = ''
        
        return profile
    
    def removeProfile(self, profile:LogTag.Enum):
        try:
            if profile not in (Logger.LogTag.error, Logger.LogTag.warn, Logger.LogTag.info, Logger.LogTag.flavor):
                self.__log_stacks.pop(profile)
            else:
                raise KeyError("cannot remove default tag profiles")
        except KeyError:
            raise KeyError("tag profile not found")

    def forceFlush(self) -> None:
        for tag in self.__log_stacks:
            if int(tag) < int(self.__severity):
                break

            self.__outsteam(tag, self.__log_stacks[tag])