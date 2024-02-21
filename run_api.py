import os
os.environ['GDK_BACKEND'] = 'wayland'

from vixen_api_lib import api
api.run()