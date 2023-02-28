import asyncio
# from logging import basicConfig as _basicConfig_, DEBUG as _DEBUG, debug as _debug_
from MyScripts.ConsoleInput.inputThread import input_thread_start as _inputThreadStart
from MyScripts.DetectExtractAndProcess.detectionThread import detection_and_extraction_update as _detectAndExtractThread, detect_thread_init as _detectThreadInit
from MyScripts.Background.backgroundThread import bg_thread_init as _bgThreadInit , bg_thread_update as _bgThreadUpdate

async def main():
    await asyncio.gather(_detectAndExtractThread(),_bgThreadUpdate())


# =============================== V Code Running V ====================================
print("====== Begin Initialization ======")

# _basicConfig_(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S',  level=_DEBUG)

print("------ Initializing Console Thread ------")
_inputThreadStart()
print("------ Console Thread Initializing Done------")

print("------ Initializing Background Thread ------")
_bgThreadInit()
_detectThreadInit()
print("------ Background Thread Initializing Done------")

print("====== Initialization Complete ======")
asyncio.run(main())
 