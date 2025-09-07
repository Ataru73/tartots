# 🔮 Tarot Reading Simulator with AI

A tarot card reading simulator that combines traditional tarot card meanings with AI-powered extensive readings using Google Gemini API.

## Features

- **Complete 78-card Tarot deck** (Major + Minor Arcana)
- **Multiple spread types** (Single card, 3-card, Celtic Cross, Relationship, Yes/No)
- **Reversed card interpretations** (30% probability)
- **🇮🇹 Italian language support** - Complete translations for card names, meanings, and interface
- **AI-powered extensive readings** via Google Gemini API (supports both English and Italian)
- **Interactive and command-line modes**
- **Beautiful formatted output** with emojis

## Installation

```bash
# Install required dependencies
pip install requests

# Make script executable
chmod +x tarots.py
```

## Google Gemini API Setup

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   Or pass it directly via `--api-key` parameter

The script uses the Gemini 1.5 Flash model, which provides fast and high-quality responses perfect for tarot readings.

## Usage

### Interactive Mode
```bash
python3 tarots.py -i
# or simply
python3 tarots.py
```

### Command Line Mode

**Basic readings:**
```bash
# Single card draw
python3 tarots.py --spread single --question "What should I focus on today?"

# Three card spread
python3 tarots.py --spread three --question "How will my week go?"

# Celtic Cross (comprehensive 10-card reading)
python3 tarots.py --spread celtic --question "What do I need to know about my life path?"

# Relationship spread
python3 tarots.py --spread relationship --question "How is my relationship progressing?"

# Yes/No reading
python3 tarots.py --spread yesno --question "Should I take this new job?"
```

**AI-Enhanced readings:**
```bash
# With extensive AI interpretation
python3 tarots.py --spread three --question "Career guidance?" --extensive

# With API key parameter
python3 tarots.py --spread celtic --api-key "your-key" --extensive --question "Life guidance?"
```

**Italian Language Support:**
```bash
# Single card in Italian
python3 tarots.py --spread single --italian --question "Che cosa devo sapere oggi?"

# Interactive mode in Italian
python3 tarots.py --interactive --italian

# Three card spread with AI reading in Italian
python3 tarots.py --spread three --italian --extensive --question "Come andrà la mia settimana?"

# Short form using -it flag
python3 tarots.py -s single -it -q "Quale carta per oggi?"
```

## Available Spreads

1. **Single Card Draw** - Daily guidance or quick insight
2. **Three Card Spread** - Past, Present, Future
3. **Celtic Cross** - Comprehensive 10-card life reading
4. **Relationship Spread** - 5-card relationship insights
5. **Yes/No Spread** - 3-card yes/no guidance

## 🇮🇹 Italian Language Support

The simulator includes complete Italian language support with:

- **Translated card names**: All Major Arcana cards (e.g., "Il Matto", "La Papessa", "L'Imperatore")
- **Italian suit names**: Minor Arcana suits ("Bastoni", "Coppe", "Spade", "Denari")
- **Italian court cards**: "Fante", "Cavaliere", "Regina", "Re"
- **Translated meanings**: Card interpretations in Italian
- **Italian interface**: All prompts, labels, and messages in Italian
- **Italian AI readings**: Gemini API generates readings in Italian when requested
- **Reversed cards**: Shows "(Rovesciata)" instead of "(Reversed)"

### Italian Example Output

```
============================================================
🔮 Stesa di Tre Carte - Passato, Presente, Futuro
============================================================
Domanda: Come andrà la mia settimana?

Carte estratte:
----------------------------------------

📍 Passato:
   🃏 Il Diavolo
   💭 Schiavitù, dipendenza, sessualità, materialismo

📍 Presente:
   🃏 La Papessa (Rovesciata)
   💭 Segreti, disconnessione dall'intuizione, ritiro

📍 Futuro:
   🃏 7 di Coppe
   💭 Opportunities, choices, wishful thinking

============================================================
```

## Example Output

```
============================================================
🔮 Three Card Spread - Past, Present, Future
============================================================
Question: How will my week go?

Cards drawn:
----------------------------------------

📍 Past:
   🃏 Queen of Swords (Reversed)
   💭 Dependency, smothering, selfishness - communication, intellect, conflict, thoughts

📍 Present:
   🃏 Judgement
   💭 Judgement, rebirth, inner calling, forgiveness

📍 Future:
   🃏 The Star
   💭 Hope, faith, purpose, renewal, spirituality

============================================================

🤖 Generating extensive reading with AI...

============================================================
📖 EXTENSIVE READING
============================================================
[AI-generated detailed interpretation appears here]
============================================================
```

## Command Line Arguments

- `--spread, -s`: Choose spread type (single, three, celtic, relationship, yesno)
- `--question, -q`: Your question for the reading
- `--interactive, -i`: Run in interactive mode
- `--italian, -it`: Display cards and meanings in Italian
- `--api-key`: Google Gemini API key for AI readings
- `--extensive, -e`: Generate extensive AI-powered interpretation

## Features Breakdown

### Traditional Elements
- Authentic tarot card meanings for all 78 cards
- Proper reversed card interpretations
- Traditional spread layouts and positions
- Realistic card shuffling simulation

### AI Enhancement
- Professional tarot reader persona in AI responses
- Comprehensive 400-600 word readings
- Card relationship analysis
- Practical guidance and advice
- Warm, empathetic tone

### Technical Features
- Clean object-oriented design
- Error handling for API calls
- Environment variable support
- Interactive and non-interactive modes
- Beautiful console formatting

## API Costs

Google Gemini API has generous free tiers. Each extensive reading uses approximately 50-100 tokens, making it very affordable for personal use.

## Privacy

- No reading data is stored or transmitted except to Google's Gemini API for processing
- Your questions and card draws are only used to generate the reading response
- API calls are made securely over HTTPS

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- Add more tarot card translations
- Improve card meanings and interpretations
- Add new spread types
- Enhance the AI prompts
- Report bugs or suggest features
