## Script for farming referrals on [Backpack](https://twitter.com/xNFT_Backpack)
Contact developer via [Telegram](https://t.me/CryptoBusher), [Twitter](https://twitter.com/CryptoBusher). Join our [Telegram Channel](https://t.me/CryptoKiddiesClub) and [Telegram Chat](https://t.me/CryptoKiddiesChat).

Script helps in farming referrals in Backpack project. Supports multithreading, proxies, custom usernames, multiple referral links and codes. Script is based on Selenium.

### First start
1. Download this repository
2. Install [python v 3.10.9](https://www.python.org/downloads/release/python-3109/)
3. Install all dependencies by typing 'pip install -r requirements.txt' in cmd (cd to the project directory first)
4. [Check](chrome://version/) your Chrome version (for example 110)
5. [Download](https://chromedriver.chromium.org/downloads) chromedriver based on your Chrome version
6. Extract 'chromedriver.exe' to the project repository
7. Open 'config.py' file using any text editor
   1. *refs_to_register:* total amount of accounts to be registered
   2. *threads:* max amount of threads
   3. *wait_element_sec:* how long Selenium should wait for any button, do not change it if you are not sure what you are doing
   4. *referrals:* your main accounts, each account has referral link and invite code. In case you use more than one main account - all refs will be evenly distributed
8. Open 'data/proxies.txt' file and enter your proxies, line by line
   1. In case you have f.e. 10 proxies, and you wish to register 20 accounts - just enter 10 proxies, script will reuse them
   2. In case you wish to register accounts without proxies - just leave this file empty
9. Open 'data/usernames.txt' file and enter your usernames, line by line
   1. In case you have f.e. 10 usernames, and you wish to register 20 accounts - just enter 10 usernames, script will generate additional usernames for remaining accounts
   2. In case username will be already claimed by other member - script will generate new username instead
   3. In case you do not wish to use your custom usernames - just leave this file empty
10. Run the bot using 'python main.py'
11. Information regarding registered accounts will be stored in 'data/backup' folder, separator '|' is used
    1. nickname
    2. seed phrase
    3. extension pass
    4. proxy used
    5. invite code used
    6. referral link used