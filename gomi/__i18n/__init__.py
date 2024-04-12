import locale as __locale

__LANGUAGE = __locale.getdefaultlocale()[0]

import sys as __sys

if __sys.version_info >= (3, 10):

    match __LANGUAGE:
        case "en_GB":
            from .en_GB import *
        case "en_US":
            from .en_US import *
        case "zh_CN":
            from .zh_CN import *
        case _:
            raise ValueError(f'Unsupported language "{__LANGUAGE}".')

else:  # Python 3.9-

    if __LANGUAGE == "en_GB":
        from .en_GB import *
    elif __LANGUAGE == "en_US":
        from .en_US import *
    elif __LANGUAGE == "zh_CN":
        from .zh_CN import *
    else:
        raise ValueError(f'Unsupported language "{__LANGUAGE}".')
