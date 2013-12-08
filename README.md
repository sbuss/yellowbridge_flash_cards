Download flashcards from Yellowbridge

Currently this only works with Integrated Chinese Level 2, 3rd edition. The
data URLs for the various decks differ in such a way that they require special
casing all of them, and I only wanted to build a flash card deck for ICL2

# Running

```
git clone https://github.com/sbuss/yellowbridge_flash_cards.git
cd yellowbridge_flash_cards
pip install -r requirements.txt
python scrape.py
```

The above checks out & installs dependencies, as well as generate 'deck.txt'.
