# valetudo_custom_voicepack
Create a custom voicepack for use with Valetudo
(1-minute-code provided by ChatGPT)

## Prerequisites
You need to know which audio files your robot is using. On a Dreame D9 you can find them in /audio/EN/ on your robot. Copy them over, listen to them and create your own audio files (OGG Vorbis, 16000 Hz, mono). Put all your audio files in the same directory as create_voicepack.py and run the script. 

## Usage
Change constants PORT, COUNTRY_CODE and TAR_FILENAME to your needs.

create_voicepack.py takes all the ogg files in the current directory and puts them into a tar.gz file. This file is served on the local machine afterwards. Just copy the URL, country code and the hash the script provides.

Use http://valetudo-yourrobot.local/#/options/robot/misc to upload the voicepack.

