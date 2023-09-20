# BitBoyBlockBot
🐔 Grabs all addresses that has transferred to BitBoy's donation address

🐔 Goes to FriendTech API to find the Twitter account of each address (if exist)

🐔 Puts all in CSV file for easy blocking


## Prereqs:

### Etherscan API key from here: [https://etherscan.io/myapikey](https://etherscan.io/myapikey)

### Friendtech JWT key:

* Open the friend.tech PWA on your Android phone
* Turn on Developer Mode on your phone and allow USB debug access
* Install adb (Android Debug Bridge) on yer 'puter
* Plug phone into puter
* Approve the puter to connect to your phone 
* Open the developer tools by opening Chrome and entering this in the URI bar: chrome://inspect/#devices
* Choose friend.tech > Inspect
* Go to the application tab
* Under the storage section, click on the Local Storage dropdown and find the friend.tech entry
* Copy the value of the jwt key

(Just find the jwt here)

![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/21d551b5-695a-4e7a-86dd-4f03ea87959f)
