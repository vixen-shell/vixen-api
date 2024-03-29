from .constants import *
from .ModelResponses import *
# from .Models import *

class Models:
    class Commons:
        from .models import Commons_Error as Error
        from .models import Commons_KeyError as KeyError

    class Features:
        from .models import Features_Base as Base
        from .models import Features_Names as Names
        from .models import Features_State as State
        from .models import Features_LogListener as LogListener

    class Frames:
        from .models import Frames_Base as Base
        from .models import Frames_Ids as Ids
        from .models import Frames_Properties as Properties

    class Log:
        from .models import Log_LogData as LogData
        from .models import Log_Log as Log
        from .models import Log_Logs as Logs