# Bleepie

With this app, users can create a pet which will become sick and die if the user drinks too much alcohol (an alcohol linked "tamagotchi" of sorts). Version 1.0 of the app will ask users for a Blood Alcohol Level ("BAL") at a certain time daily using the Twilio API for SMS. A certain BAL level will make your pet sick and a very high level will kill your bleepie pet. The design for the Bleepie creature was (rather inexplicably) inspired by a shallot. Bleepie is too cute - don't let it die! Users will receive points for keeping their pet alive for more days.

# Detail on how it works: 1.0

Users will be texted daily at 9pm Pacific. The text will be a request for the user's BAL - use of a breathalyzer is required for this. If a user's BAL is over 0.0, they will be "on watch" and will be texted again at 10pm Pacific. If their BAL has increased or stayed the same over this hour, they will remain "on watch". If it has decreased, they are removed from watch. Users still "on watch" at 11pm Pacific receive a third BAL request. At any point, if the user's BAL is over 0.10, the pet will become sick. A BAL over 0.12 will kill the pet. If a pet has been sick for over 24 hours, BAL data is multipled by 1.5. All BAL data is timestamped and saved. 

This app is in no way intended to be a solution for someone with a drinking problem. Bleepie is just a simple, fun game and data collector :) safe drinking everyone! 

Check out the deployed app <a href="https://bleepie.herokuapp.com">here</a>
