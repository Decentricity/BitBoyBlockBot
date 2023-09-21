# BitBoyBlockBot
🐔 Grabs all addresses that has transferred to BitBoy's donation address

🐔 Goes to FriendTech API to find the Twitter account of each address (if exist)

🐔 Puts all in CSV file for easy blocking


## Prereqs:

### Etherscan API key from here: [https://etherscan.io/myapikey](https://etherscan.io/myapikey)

### Friendtech JWT key:
(Note: As of Sept 21st (ironically just a few hours after i published this lol) Friendtech announced that they are allowing PC web browser logins [here](https://x.com/friendtech/status/1704608806259548592?s=20) so you can actually just grab the JWT from there (just right-click on the ft page > inspect, and see step 8). The steps below are still pretty useful for getting the JWT from your phone.)

1. Open the friend.tech PWA on your Android phone
2. Turn on Developer Mode on your phone and allow USB debug access
3. Install adb (Android Debug Bridge) on yer 'puter
4. Plug phone into puter
5. Approve the puter to connect to your phone 
6. Open the developer tools by opening Chrome and entering this in the URI bar: chrome://inspect/#devices
7. Choose friend.tech > Inspect
8. Go to the application tab
9. Under the storage section, click on the Local Storage dropdown and find the friend.tech entry
10. Copy the value of the jwt key

(Here is wer u find the jwt)
![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/aefd78de-e98c-4f05-9508-0aa1c537c284)

### BTW yes this does work, even tho FT creates its own wallet in the app. (thanks to @bacon_wassie who highlighted this to me)

### here's how:

Script uses @etherscan to check which addresses sent tokens to bitboy

Script then checks whether there are @BuildOnBase addresses that was initiated by the addresses we found (i.e, funded by L1 addie, first tx of the L2 addie) -- http://api.basescan.org was used for dis

![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/dc82625b-d4b3-4d63-a034-3685ef6be0b8)

![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/8e3b9908-206c-4e46-85d7-a91ac3f1e767)

finally, we grab dat Base addie and use the friendtech API to find twitter usernames, if they exist. (if not, then the Base addie prolly didnt interact with friendtech)

![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/a331f8ca-ee35-45f1-b7ac-0bb08fcd9dda)

![image](https://github.com/Decentricity/BitBoyBlockBot/assets/76634353/892737d0-cd66-4eda-988c-d19a460f130f)
