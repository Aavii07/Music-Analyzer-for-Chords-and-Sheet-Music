from frontend.music_analyzer import MusicAnalyzer
from backend.config import SIMPLIFY_CHORDS

def main():
    app = MusicAnalyzer(simplify_chords=SIMPLIFY_CHORDS)
    app.mainloop()

if __name__ == "__main__":
    main()
