# Music Analyzer for Chords (and Sheet Music)

This program is a useful tool developed for analyzing any chord you find. You can enter the notes via an input box or simply click on notes in a custom-built fully interactive piano to see your chord processed in real time. This tool also has the 'Chord Extractor' which allows you to extract any chord from any piece of sheet music (assuming you have it in MusicXML format) and analyze the chord in the chord finder. This tool does have a few limitations in its current state however, and I strongly encourage you to at least read the **Important Limitations** section before trying the application for yourself.<br><br>

This application started as a simple tool for myself, but as it grew I decided it would make sense to make it public as I have not found anything like this yet. The way it works is by using the Custom Tkinter GUI to interface with the music21 Python library, a library that has been commonly used in musicology and computational music analysis. Below are notes on how to use both the Chord Finder and Chord Extractor

# Chord Finder
<img width="1000" alt="Chord Finder Light Mode" src="https://github.com/user-attachments/assets/b22496c1-31cc-4357-bd51-f32267cb6a04">
<img width="1000" alt="Chord Finder Dark Mode" src="https://github.com/user-attachments/assets/24ea0f30-36ac-463b-afd2-04a7fa26ca69">
<br><br>
Notes:<br>

- Accidentals can be entered using 'b' or '-' for flat and '#' for sharp. You can add up to 4 accidentals on one note, unless you are using the 'b' in which case you can only enter one. Just because you can add 4 accidentals doesn't mean you should :)<br>

- The entire keyboard is fully interactable and it is encouraged to click the notes rather than type them out as its quicker and easier. If you shift-click a note, you can get an alternative spelling for it (a# becomes b-, f becomes e#, etc). The notes d, g and, a do not have alternative spellings as it would require double sharps/flats. <br>

- You can press command/control + z at any time to clear all notes off piano.<br>

- The enharmonic simplifer is recommended on because it can be annoying to have the program say you wrote the enharmonic equivalent to C# major just beacuse you used 'f' instead of 'e#'. The enharmonic simplifer does not catch and simplify everything though. It also can sometimes catches mistakes in chord analysis (for more information about accuracy, go to the **Important Limitations** section. <br>

- The chord symbols simplfier is recommended on because while unsimplified numerals tell you more about the chord, this is what they can look like:<br>
<img width="400" alt="Convoluted Numerals" src="https://github.com/user-attachments/assets/6683001b-bc77-485f-a894-8507dca04c52"> <br>
If you know how to interpret this, by all means turn the chord symbols simplifier off.<br>

- The piano only makes sound when you click it (which can be toggled). This setting is overriden if you have 'Keyboard Freeplay' enabled, which allows you to play the keyboard by clicking on all the notes without highlighting anything.<br>

# Chord Extractor
<img width="1000" alt="Chord Extractor Light Mode" src="https://github.com/user-attachments/assets/24fe67bf-0520-446d-90b0-05907807f764">
<img width="1000" alt="Chord Extractor Dark Mode" src="https://github.com/user-attachments/assets/784dad75-dddf-41c6-b048-d88b6315ec25">
<br><br>
Notes:<br><br>

- This is the first window you will see when you open the application. In order to extract chords you need the sheet music in the format of MusicXML. You can completely ignore this feature if you do not have a MusicXML sheet music.<br><br>
- You can filter out extracted chords using the parameters above to very quickly isolate the section of the song you need.<br><br>
- You can double click to open any chord in the chord finder. You can shift-click to highlight multiple chords, and double click them while holding shift to automatically insert all the notes in all highlighted chords in the chord finder, The chord finder will automatically interpret the combined notes as a new chord.<br><br>
  - This feature is particularly useful when combined with sorting the chord 'By Measure and Beat' in the bottom right corner as opposed to 'By Instrument', as it allows you to easily shift-click all the notes in all the chords played at any given measure and beat, seeing the combined chord they produce.<br><br>

# Important Limitations
<br>
There are a couple of key limitations it is important to be aware of should you use this tool.<br><br>

- Firstly, not every chord interpretation in the Chord Finder will be correct. Here is a paper that analyzes and delves into the accuracy of the Python library called music21 running in the backend if you are interested: https://dmitri.mycpanel.princeton.edu/music21.pdf<br><br>
- From my experience, music21 tends to almost always be correct always for 3 or 4 unique note chords, and if you get a strange looking result or chord name then toggling the enharmonic simplifier on/off seems to do the trick.<br><br>
- When you get to 5 or 6 unique note chords, the errors do start to seem slightly more frequent. One interesting quirk about many of these errors is that the chord name tends to be correct quite frequently, but you are told an inaccurate chord root. <br><br>
- Once you go to 7+ unique chords many of the chord names themselves become extremely technical, enough so that the average musician would have no idea what it means. These chords should probably be broken up into smaller triads or seventh chords if you are analyzing chords like this. I cannot speak for the accuracy of these chords.<br><br>
- Also be wary of chords that have the name of a mode in them (like lydian or phrygian), as these chord based off of the mode of a scale were frequently incorrect in my experience. In fact, music21 was so bad with scales in general that I just stopped it from outputting the names of scales altogether.<br><br>


The music analyzer also has a few key limitations when it comes to extracting chords, mainly that the chord has to be 2+ notes played on the same beat and measure in the same staff<br><br>
 - it cannot extract arpeggiated chords (since they are not played of the same beat).<br><br>
 - if a chord as a one note root bass in the treble clef following by the upper extensions in the treble clef, you wont get that one note root in the chord and have to add it in manually after opening the treble clef's chord up in the chord finder.<br><br>
 - many times orchestral scores will divide their chords into groups of one note, divided among different instruments of the string section for example. You cannot just sort 'By Measure and Beat' and shift-click all the chords in this string section as the singular notes will not be extracted.<br><br>
 - Make sure each part has a unique name. If you have 2 pianos and they are both called 'Piano' (instead of 'Piano 1' and 'Piano 2'), the chord finder will get confused when automatically dividing up the bass and treble clefs. This ideally should not happen as naming duplicate instruments the exact same is really bad practice, but just be aware of this.<br><br>

Even with these limitations, in practice the chord finder tends to be very helpful with most scores as it extract a good majority of the chords for you instead of forcing you to input each note manually. What it won't do, however, is automatically give you the entire chord progression and do all the work of reading sheet music for you.<br><br>

# Download
Go to the downloads page below to download the version for your specific operating system: <br>
https://github.com/Aavii07/Chords-Analyzer-and-Extractor-Tool/releases/tag/v1.0

Note that for MacOS, you need to right click on the extracted file and click 'Show Package Contents,' from there you navigate to Contents/MacOS and run the only file in that directory. It should open a terminal which runs the application shortly later (it may like it nothing is happening but its loading in the background). So far, this is the only way I got it to work

You can also run the project locally by running the following commands assuming you have Python installed:

# For local setup<br>
*Note: if you only have Python3 installed use pip3 and Python3 instead*<br><br>
Run the following commands to setup the project dependecies in a virtual environment:<br>
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Now whenever you run ```python main.py``` in the root directory the application will boot up quickly


