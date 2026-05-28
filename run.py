from dotenv import load_dotenv
import customLogging
import sys
from app.main import create_app
import os

scriptName = os.path.basename(__file__)
scriptFolder = os.path.dirname(__file__)

logging = customLogging.setupCustomLogging(scriptName)

logging.info(
    scriptName + "| ------------------------------------------------------------"
)
logging.info(scriptName + "| Script name: [" + scriptName + "]")

# Determine if the application is a script file or a frozen executable file
if getattr(sys, "frozen", False):
    scriptFolder = os.path.dirname(sys.executable)
    logging.debug(
        scriptName
        + "| Application was launched from frozen executable located in: ["
        + scriptFolder
        + "]"
    )
    scriptFolder = os.path.dirname(__file__)
    logging.debug(
        scriptName
        + "| Extracted temp files location from the frozen executable: ["
        + scriptFolder
        + "]"
    )
elif __file__:
    scriptFolder = os.path.dirname(__file__)
    logging.debug(
        scriptName
        + "| Application was launched from python script located in: ["
        + scriptFolder
        + "]"
    )
logging.info(scriptName + "| Application folder: [" + scriptFolder + "]")

load_dotenv()

port = int(os.environ.get("SERVER_PORT", "5555"))  # debug port when app is run directly

app = create_app()

if __name__ == "__main__":

    if port is None:
        app.run(host="localhost", port=5000, debug=True, threaded=True)

    else:
        app.run(host="0.0.0.0", port=int(port), debug=False, threaded=True)
