from nevermined_sdk_py import Nevermined, Config

def demo():
    # 1. Setup nevermined
    # 2. Setup accounts
    # 3. Publish assets
    # 4. Start coordinator
    # 5. Consume assets and start participant

    # 1. Setup nevermined
    nevermined = Nevermined(Config("config.ini"))


    # 2. Setup accounts
    provider_data1 = nevermined.accounts.list()[0]
    provider_data2 = nevermined.accounts.list()[0]
    provider_coordinator = nevermined.accounts.list()[0]
    consumer = None

    # 3. Publish assets

