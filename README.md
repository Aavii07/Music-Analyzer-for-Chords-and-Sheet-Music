# Music Analyzer for Chords and Sheet Music

This program is a useful tool developed for analyzing any chord you find. You can enter the notes via an input box or simply click on notes in a custom-built fully interactive piano to see your chord processed in real time. This tool also has the 'Chord Extractor' which allows you to extract any chord from any piece of sheet music (assuming you have it in MusicXML format) and analyze the chord in the chord finder. This README provides a general breakdown of what this tool excels at, as well as where its current limitations lie. It is highly encouraged that you at least skim this README if you plan to use this tool.<br><br>

This application started as a simple tool for personal music analysis. As it developed, I realized it might make sense to polish and publicize it, as I feel like someone else may find this useful in some way. The way it works is by using the Custom Tkinter GUI to interface with the music21 Python library, a library commonly used in musicology and computational music analysis. Below are important notes on how to use both the Chord Finder and Chord Extractor.

# Chord Finder
<img width="1000" alt="Chord Finder Light Mode" src="https://github.com/user-attachments/assets/b22496c1-31cc-4357-bd51-f32267cb6a04">
<img width="1000" alt="Chord Finder Dark Mode" src="https://github.com/user-attachments/assets/24ea0f30-36ac-463b-afd2-04a7fa26ca69">
<br><br>
Notes:<br>

- Accidentals can be entered using 'b' or '-' for flat and '#' for sharp. You can add up to four accidentals to one note. However, if you are using 'b', you can only enter one. Just because you can add 4 accidentals doesn't mean you should :)<br>

- The entire keyboard is fully interactable and it is highly encouraged to click the notes rather than type them out as it's quicker and easier. <br>

   - If you shift-click a note, you can get an alternative spelling for it (A# becomes B-, F becomes E#, etc). The notes D, G, and A do not have alternative spellings as it would require double sharps/flats. <br>

- You can press Command/Ctrl + Z at any time to clear all notes from the piano. <br>

- Notes can be entered in a variety of ways (C##5, c#5#, etc). If you do not enter a number next to the note, it defaults to the fourth octave.<br>

- It can be annoying to have the program give an enharmonically equivalent chord name just because you used the a different spelling of the same note (like 'F' instead of 'E#). The enharmonic simplifier is designed to ensure you don't have to be concerned with the specific names of the notes you input when determining a chord name. <br>

   - While efficient, the enharmonic simplifer does not catch and simplify every single chord. <br>
 
   - It also can tend to catch mistakes in chord analysis (for more information about accuracy, go to the **Important Limitations** section. <br>

- The chord symbols simplfier is recommended on because while unsimplified numerals tell you more about the chord, this is what they can look like:<br>
<img width="400" alt="Convoluted Numerals" src="https://github.com/user-attachments/assets/6683001b-bc77-485f-a894-8507dca04c52"> <br>
If you know how to interpret this, feel free to turn the chord symbols simplifier off.<br>

- The piano only makes sound when you click it (this feature be toggled). This setting is overriden if you have 'Keyboard Freeplay' enabled, which allows free play on the keyboard by clicking on any note without highlighting anything.<br>

# Chord Extractor
<img width="1000" alt="Chord Extractor Light Mode" src="https://github.com/user-attachments/assets/24fe67bf-0520-446d-90b0-05907807f764">
<img width="1000" alt="Chord Extractor Dark Mode" src="https://github.com/user-attachments/assets/784dad75-dddf-41c6-b048-d88b6315ec25">
<br><br>
Notes:<br><br>

- This is the first window you will see when you open the application. To extract chords, you need the sheet music in MusicXML format. You can completely ignore this feature if you do not have MusicXML sheet music.<br>

- You can filter out extracted chords using the parameters above to very quickly isolate the section of the song you need.<br>

- You can double-click to open any chord in the chord finder. You can shift-click to highlight multiple chords and double-click them while holding shift to automatically insert every note in all highlighted chords into the chord finder, The chord finder will automatically interpret the combined notes as a new chord.<br>

  - This feature is particularly useful when combined with sorting extracted chords 'By Measure and Beat' (in the bottom-right corner). This allows you to easily shift-click all chords played at any given measure(s) and beat(s), seeing the combined chord they produce.<br><br>

# Important Limitations
<br>
There are a couple of key limitations with the music21 library that are important to be aware of should you use this tool.<br><br>

- Firstly, not every chord interpretation in the Chord Finder will be correct. Here is a paper that analyzes and delves into the accuracy of the Python library called music21 running in the backend if you are interested: https://dmitri.mycpanel.princeton.edu/music21.pdf<br>

- From my experience, music21 tends to almost always be correct always for 3 or 4 unique note chords, and if you get a strange looking result or chord name then toggling the enharmonic simplifier on/off seems to do the trick.<br>

- When you get to 5 or 6 unique note chords, the errors may be slightly more frequent. One interesting quirk about many of these errors is that the chord name tends to be correct quite frequently, but you are told an inaccurate chord root. <br>

- Once you go to 7+ unique chords many of the chord names themselves become extremely technical, enough so that the average musician would have no idea what it means. These chords should probably be broken up into smaller triads or seventh chords if you are analyzing chords like this. I cannot speak for the accuracy of these chords.<br>

- Also be wary of chords that have the name of a mode (like lydian or phrygian), as these chords were frequently incorrect in my experience. These chord names tend to only appear if you input strange cluster chords. <br><br>


The music analyzer also has a few key limitations when it comes to extracting chords, mainly that the chord has to be 2+ notes played on the same beat and measure in the same staff<br><br>
 - It cannot extract arpeggiated chords (as each note is not played on the same beat).<br>
 
 - If a chord as a one-note root bass in the treble clef followed by the upper extensions in the treble clef, you wont get that one-note root in the chord and have to add it in manually after opening the treble clef's chord up in the chord finder.<br>
 
 - Many times orchestral scores will divide their chords into singular notes, divided among different instruments of the string section for example. You cannot use the trick of sorting 'By Measure and Beat' and shift-clicking to get the chords in this string section as the singular notes will not be extracted.<br>
 
 - Make sure each part has a unique name. If you have 2 pianos and they are both called 'Piano' (instead of 'Piano 1' and 'Piano 2'), the chord finder will get confused when automatically dividing up the bass and treble clefs of a given instrument. This ideally should not happen as naming duplicate instruments the exact same is really bad practice, but just be aware of this.<br><br>

Even with these limitations, in practice the chord finder tends to be very helpful with most scores as it extract a good majority of the chords for you instead of forcing you to input each note manually. What it won't do is automatically give you the entire chord progression and do all the work of reading sheet music for you.<br><br>

# Download
Go to the downloads page below to download the version for your specific operating system: <br>
https://github.com/Aavii07/Chords-Analyzer-and-Extractor-Tool/releases/tag/v1.0

Note that for MacOS, you need to right click on the extracted file and click 'Show Package Contents.' From there you navigate to Contents/MacOS and run the only file in that directory. It should open a terminal which runs the application shortly later. So far, this is the only way I got it to work<br>

Also be aware that it does take a while (~20 to 40 seconds) for the application to boot up, and during that time it may look like the terminal froze or the application did not run (when it's loading in the background).<br><br> 

You can also easily setup the project and be able to instantly run it locally by running the following commands assuming you have Python installed:

# For local setup<br>
*Note: if you only have Python3 installed use pip3 and python3 instead*<br><br>
After cloning the project, run the following commands in the root directory to setup the project dependencies in a virtual environment:<br>
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Now whenever you run ```python main.py``` in the root directory the application quickly will boot up


