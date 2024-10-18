import os
import sys
sys.path.append('.')
import customLogging
sys.path.append(os.path.dirname(__file__)+'/venv/Lib/site-packages')
from app import app

scriptName = os.path.basename(__file__)
scriptFolder = os.path.dirname(__file__)

logging = customLogging.setupCustomLogging(scriptName)

logging.info(scriptName + '| ------------------------------------------------------------')
logging.info(scriptName + '| Script name: [' + scriptName + ']')

if __name__ == '__main__':
    from waitress import serve
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    logging.debug(scriptName + "| PORT: [" + str(PORT) + "]...")
    logging.info(scriptName + "| Starting [waitress] on port [" + str(PORT) + "]...")
    serve(app, host="localhost", port=PORT)
    logging.info(scriptName + "| Ended execution of [waitress].")