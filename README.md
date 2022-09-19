# CUinClass

Notes:
1. In requirements.txt there's "pywin32==304" - when deploying to a linux server it as to be commented, when installing the requirements on windows to develop - it has to be un-commented.
2. In attendance.js under "sendImage" function, note the "const url" you're sending thru axios.post, according to the environment at the moment - domain for a server deployment or localhost for developement mode.
3. Make sure to set AWS credential in order to access the "rekognition" functions on awsfuncs.py, either by .env files (2) or by environment variables you set on your server.