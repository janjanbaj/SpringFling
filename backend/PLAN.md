= Backend Functionality

- login-less infrastructure where you use your email and some OTP passowrd to login 
- pocketbase does OTPs by itself, so we dont really have to implement it by ourselves either.
- assign some special adjective + animal name combo for anonymous interactions.

This is how I envision onboarding will look like:

1. User signs up with *@mail.wlu.edu then we use our mail server to send out an email saying here is the OTP. 
2. User puts in OTP and gets assigned some fun "adjective+animal" username. They will only need this to login and complete the questionare. Users must make this anonymous until they finish the questionare. After which it will be used to anonmyize the data on the frontend.
3. Then run matching algorithm and then send out pairs of adj + noun names as an email as well.
4. Reveal match by logging into your own personal pseudo names and then a few days later prevent all logins. Then do the data-science bs


== Representing Questionares in Databases

- since we are using sqlite inside pocketbase, we are able to use a GUI to draw out our questionare
- there should be different types of questions:
    - General Questions:
    - Categorical Questions:
