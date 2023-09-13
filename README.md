# CUinClass

Facial recognition app has the potential to streamline academic attendance procedures. Students are required to stand in front of a tablet or phone running the app at the entrance of their class and click on it to register their attendance. The software automatically generates a report with all the students' attendance records for the current session, which can be emailed upon request. Furthermore, the software includes a feature where students can sign up for the system on the spot by providing their personal information and taking a photo of their face.

• Tech stack: Django Python with AWS "Rekognition", PostgreSQL for data storage, and AWS S3 for image archiving. The UI was developed using HTML, vanilla Javascript, and Bootstrap.

Notes:
The application is using AMAZON S3 bucket for image storing and AMAZON Rekognition API for face recognition - configure AWS Credentials accordingly under settings.py (including ENV VAR on your server) and under .env files on 'fr' and 'cuinclass' foldiers.
