## GoW-Helper

#### What is it?
Gems of War automated stat data collector with GUI. Lets you manually or automatically keep track of 
token rewards while farming **Explore 12** in Gems of War. 

- Lets you manually set your rewards, and submit the stats to your current session.
- Keep track of session stats and all-time stats individually. Check-box by Done-button automatically submits the run to all-time stats as well.
- Keep log of all your sessions and specific drop data in the Session History Tab.
- Session Save button to save the current session to history.
- Auto Detection capability that will allow the app to read rewards and submit them to session/alltime stats for you. 
NOTE: App will for this functionality resize you game window to its preferences to be able to find the information it needs on the game screen. You game window also needs to be on your main screen. The Auto-Detection tab will throw an error if that is not the case.
- If you still want to manually make sure the app finds and enters the correct drops before it submits them, you can omit the Auto-submit results checkbox.

![Stats and All-Time Stats](https://i.gyazo.com/20769718ff973be7993bd2b6e0370b1f.png)

![Session History](https://i.gyazo.com/34773e5779f3d17668f00a860a630dc8.png)

![Auto-Detection](https://i.gyazo.com/24b707142efcfdb454ca1d8bcc7b22c0.png)

#### Technologies learnt thought this project:
- Tkinter GUI library (ttk Bootstrap)
- Tesseract library for reading text from the screen and using it in code.
- Multi-Threading to be able to constantly read the screen for events in the game and for GUI not to freeze.
- Manipulating user windows with finding coordinates on screen, resizing and checking if game window in on the correct screen.
