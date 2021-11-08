# DentAlert
#### Video Demo:  https://youtu.be/VpmPF17yAH4
#### Description: This web application was designed for the sole purpose of my CS50 final project. The goal is to display my newly acquired skill with a web application,</br> which can send automated reminders for profilactic exams to patients who are overdue according to the doctor/dentist.
#### Origins:
I was still in the first few weeks of the course, when I had to go and visit my dentist to fix two problems, and as I was laying on the dentist chair I wondered</br>
> This is rediculous - how come I get email/SMS/Viber etc. notifications if any ensurance policy is about to expire or my vignette sticker on the car, </br>
but never ever in my life I've received a reminder for any profilactic medical examination which was overdue? Moreover, to my knowledge profilactics is the </br>
core of a good health care system - it saves tons of money for the patient, it prolongs their healthy life and saves a ton of money for my government. </br>
Not to mention, in the case of dentists it is more profitable for them, as well, in terms of time vs money. And we are all too busy all the time, </br>
prone to delay anything which is not urgent, so we really need a push.

*Note: I was planning on trying to further develop and commersializing the app at some point. However, after a brief research among close friends and relatives*
*in the healthcare business I found out that, actually, virtually every software used to track patients, managing their records, etc. has such functionality*
*so the problem is not the lack of opportunities for the doctors to remind us - it's just that they are not doing it.... for whatever strange reason.*

Anyway, I decided to continue with that idea and to create a web application where:
- [X] Dentists can create and manage their own lists of patients.
- [X] Automatically send reminders to patients who are soon to be overdue on their profilactics schedule.
- [ ] *Deliver the reminder from the doctor's very own email*

First my intention was to have all messages delivered from the doctor's own emails, for which I would had to link the application through API with a </br>
messaging service (like MailChimp for example) and collect the doctors API keys. After some consideration and consultations if this would be a good user experience,</br>
I've come to the conclusion that it is too much to ask from the users to create a registration with any given third part service, collect their personal API key</br>
and for them to manage the whole "send profilactic reminders" initiative from two places. Therefore, I went a step back, removed the API setup and decided to send</br>
all reminder notifications from the mail address of the DentAlert app / service.

I've created a dummy email box in Gmail for testing purposes, which I was considering to give away with the project, however, it made more sense to
show a good example and comply with the best practice and replace the credentials with environment variables.

#### File description:
- scripts.js - this file holds the JavaScript code which I use to:
    - collect data from the page upon click on the Edit button on all_patients.html
    - insert session stored data while load the edi_patient.html form
    - send data back to the server upon click on the Delete button on all_patients.html
- styles.css - I've utilized only bootstrap styling, however, I leave this file to avoid browser loading errors
- HTML:
    - add_patient.html - html form to insert new patients into the database
    - all_patients.html - page displaying all patients from the database, which are associated with the currently logged doctor, has edit and delete
    functionalities
    - apology.html - template for displaying error messages to the user
    - edit_patient.html - renders a pre-filled form with the patient to be edit data, which will update the record
    - index.html - the homepage of the application, which displays a summary for the currently logged doctor
    - layout.html - the flask layout
    - login.html - a login form
    - register.html - a register form for creation of new users/doctors
- application.py - this file holds the flask application code and the scheduler for notifications
- helper.py - holds the code to render the apology.html and adds the capability to decorate routes to require login
- model.db - SQLite database, which has four tables:
    - users - has user/doctor information and login details
    - patients - has patient basic information
    - my_patients (link table)
    - alerts - holds the due_date for each scheduled alert, patient, doctor, and the status of the alert
- requirements.txt - this is a list of all libraries used for the development of the tool