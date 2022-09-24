# CUinClass


Notes:
1. In requirements.txt there's "pywin32==304" - when deploying to a linux server it has to be commented, when installing the requirements on windows for develop - it has to be un-commented.
2. In attendance.js under "sendImage" function, note the "const url" you're sending thru axios.post, according to the environment at the moment - domain for a server deployment or localhost for developement mode.
3. The application is using AMAZON S3 bucket for image storing and AMAZON Rekognition API for face recognition - configure AWS Credentials accordingly under settings.py (including ENV VAR on your server) and under .env files on 'fr' and 'cuinclass' foldiers.