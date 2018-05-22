# Auto reboot test for bluetooth paired data
#
# a loop to run for MTK-439, reboot and check :
#  adb wait-for-device
#  adb root
#  adb wait-for-device
#  adb shell grep QS /data/misc/bluedroid/bt_config.conf
#  adb reboot

import subprocess
import logging
import sys
import time

TOTAL_TEST_TIMES            = 100000
ADB_ROOT_DELALY_TIME        = 6 #60 s for charging
ADB_WAIT_FOR_DEVICE         = "adb wait-for-device"
ADB_DEVICES                 = "adb devices"
ADB_ROOT                    = "adb root"
ADB_GET_BT_PRINTER          = "adb shell grep QSPrinter /data/misc/bluedroid/bt_config.conf"
ADB_REBOOT                  = "adb reboot"
ADB_LOGCAT                  = "adb logcat -v time -d > bt_logcat.log"
ADB_GET_BT_SETTINGS         = "adb pull /data/misc/bluedroid/bt_config.conf"
ADB_GET_BUILD_FINGERPRINT   = "adb shell getprop ro.build.fingerprint"
ADB_GET_BUILD_DATE          = "adb shell getprop ro.build.date"
ADB_SEND_POWER_KEY          = "adb shell input keyevent KEYCODE_POWER"

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('bttest.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


def main():
    logger = setup_custom_logger('bttest')
    logger.info("Bluetooth printer paired device test start.")
    output = subprocess.check_output(ADB_GET_BUILD_FINGERPRINT)
    logger.info("Build Fingerprint: %s", output.decode('utf-8').replace('\r','').replace('\n',''))
    output = subprocess.check_output(ADB_GET_BUILD_DATE)
    logger.info("Build Date: %s", output.decode('utf-8'))

    for i in range(TOTAL_TEST_TIMES):
        output = subprocess.call(ADB_WAIT_FOR_DEVICE)
        logger.info("Device is rebooted.")

        # suspend 5 seconds to charge a while
        output = subprocess.call(ADB_SEND_POWER_KEY)
        time.sleep(ADB_ROOT_DELALY_TIME)
        # output = subprocess.call(ADB_DEVICES)
        output = subprocess.check_output(ADB_ROOT)
        logger.info(output.decode('utf-8').replace('\r','').replace('\n',''))
        output = subprocess.call(ADB_WAIT_FOR_DEVICE)
        logger.info("Checking QSPrinter Paring status test %d", i+1)
        output = subprocess.call(ADB_WAIT_FOR_DEVICE)
        output = subprocess.check_output(ADB_GET_BT_PRINTER)

        if output == b'Name = QSPrinter\r\r\n':
            logger.info("Paired device QSPrinter exists. TEST %d PASS !", i+1)
            logger.info("Rebooting device...")
            output = subprocess.call(ADB_REBOOT)
        else:
            logger.warning("Paired device QSPrinter not exist %s", output.decode('utf-8'))
            logger.warning("Getting logcat ", ADB_LOGCAT)
            output = subprocess.call(ADB_LOGCAT, shell=True)
            logger.warning("Getting bt_config ", ADB_GET_BT_SETTINGS)
            output = subprocess.call(ADB_GET_BT_SETTINGS, shell=True)




if __name__ == "__main__":
    main()
