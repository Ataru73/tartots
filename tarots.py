#!/usr/bin/env python3
"""
Tarot Card Reading Simulation
============================

A script that simulates the extraction of tarot cards in a typical reading session.
Includes both Major and Minor Arcana cards with their meanings and various spread types.
"""

import random
import argparse
from typing import List, Dict, Tuple
from enum import Enum
import requests
import json
import os

class Suit(Enum):
    WANDS = "Wands"
    CUPS = "Cups"
    SWORDS = "Swords"
    PENTACLES = "Pentacles"

class TarotCard:
    def __init__(self, name: str, suit: Suit = None, number: int = None, 
                 upright_meaning: str = "", reversed_meaning: str = "", is_major: bool = False):
        self.name = name
        self.suit = suit
        self.number = number
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
        self.is_major = is_major
        self.is_reversed = False
    
    def __str__(self):
        suit_str = f" of {self.suit.value}" if self.suit else ""
        reversed_str = " (Reversed)" if self.is_reversed else ""
        return f"{self.name}{suit_str}{reversed_str}"
    
    def get_meaning(self):
        return self.reversed_meaning if self.is_reversed else self.upright_meaning

class TarotDeck:
    def __init__(self):
        self.cards = []
        self._create_major_arcana()
        self._create_minor_arcana()
        self.reset_deck()
    
    def _create_major_arcana(self):
        major_arcana = [
            ("The Fool", "New beginnings, innocence, spontaneity", "Recklessness, taken advantage of, inconsideration"),
            ("The Magician", "Manifestation, resourcefulness, power", "Manipulation, poor planning, untapped talents"),
            ("The High Priestess", "Intuition, sacred knowledge, divine feminine", "Secrets, disconnected from intuition, withdrawal"),
            ("The Empress", "Femininity, beauty, nature, nurturing", "Creative block, dependence on others"),
            ("The Emperor", "Authority, establishment, structure, father figure", "Domination, excessive control, lack of discipline"),
            ("The Hierophant", "Spiritual wisdom, religious beliefs, conformity", "Personal beliefs, freedom, challenging the status quo"),
            ("The Lovers", "Love, harmony, relationships, values alignment", "Self-love, disharmony, imbalance, misalignment of values"),
            ("The Chariot", "Control, willpower, success, determination", "Lack of control, lack of direction, aggression"),
            ("Strength", "Strength, courage, persuasion, influence, compassion", "Inner strength, self-doubt, low energy, raw emotion"),
            ("The Hermit", "Soul searching, introspection, inner guidance", "Isolation, loneliness, withdrawal"),
            ("Wheel of Fortune", "Good luck, karma, life cycles, destiny", "Bad luck, lack of control, clinging to control"),
            ("Justice", "Justice, fairness, truth, cause and effect", "Unfairness, lack of accountability, dishonesty"),
            ("The Hanged Man", "Waiting, surrender, letting go, new perspective", "Delays, resistance, stalling, indecision"),
            ("Death", "Endings, change, transformation, transition", "Resistance to change, personal transformation, inner purging"),
            ("Temperance", "Balance, moderation, patience, purpose", "Imbalance, excess, self-healing, re-alignment"),
            ("The Devil", "Bondage, addiction, sexuality, materialism", "Releasing limiting beliefs, exploring dark thoughts, detachment"),
            ("The Tower", "Sudden change, upheaval, chaos, revelation", "Personal transformation, fear of change, averting disaster"),
            ("The Star", "Hope, faith, purpose, renewal, spirituality", "Lack of faith, despair, self-trust, disconnection"),
            ("The Moon", "Illusion, fear, anxiety, subconscious, intuition", "Release of fear, repressed emotion, inner confusion"),
            ("The Sun", "Positivity, fun, warmth, success, vitality", "Inner child, feeling down, overly optimistic"),
            ("Judgement", "Judgement, rebirth, inner calling, forgiveness", "Self-doubt, inner critic, ignoring the call"),
            ("The World", "Completion, integration, accomplishment, travel", "Seeking personal closure, short-cuts, delays")
        ]
        
        for name, upright, reversed in major_arcana:
            self.cards.append(TarotCard(name, upright_meaning=upright, reversed_meaning=reversed, is_major=True))
    
    def _create_minor_arcana(self):
        # Court cards meanings
        court_meanings = {
            "Page": {
                "upright": "New ideas, enthusiasm, messages",
                "reversed": "Self-doubt, immaturity, lack of progress"
            },
            "Knight": {
                "upright": "Action, adventure, impulsiveness", 
                "reversed": "Inaction, haste, unfinished business"
            },
            "Queen": {
                "upright": "Compassion, calm, comfort, loyalty",
                "reversed": "Dependency, smothering, selfishness"
            },
            "King": {
                "upright": "Leadership, honor, control",
                "reversed": "Dishonesty, lack of control, weak leadership"
            }
        }
        
        # Numbered cards meanings by suit
        suit_meanings = {
            Suit.WANDS: {
                "element": "Fire",
                "keywords": "creativity, spirituality, passion, inspiration",
                "numbers": {
                    1: ("New creative energy, inspiration", "Delays, lack of motivation"),
                    2: ("Future planning, making decisions", "Fear of unknown, lack of planning"),
                    3: ("Expansion, foresight, overseas opportunities", "Lack of foresight, delays"),
                    4: ("Celebration, harmony, homecoming", "Personal celebration, inner harmony"),
                    5: ("Conflict, disagreements, competition", "Inner conflict, conflict avoidance"),
                    6: ("Public recognition, progress, self-confidence", "Private achievement, self-doubt"),
                    7: ("Challenge, competition, perseverance", "Overwhelmed, giving up"),
                    8: ("Movement, fast paced change, action", "Delays, frustration, resisting change"),
                    9: ("Resilience, courage, persistence", "Inner courage, weakness"),
                    10: ("Burden, extra responsibility, hard work", "Unable to delegate, overstressed")
                }
            },
            Suit.CUPS: {
                "element": "Water",
                "keywords": "emotion, spirituality, intuition, relationships",
                "numbers": {
                    1: ("Love, new relationships, compassion", "Self-love, intuition, repressed emotions"),
                    2: ("Unified love, partnership, mutual attraction", "Self-love, break-ups, disharmony"),
                    3: ("Celebration, friendship, creativity", "Independence, alone time"),
                    4: ("Meditation, contemplation, apathy", "Retreat, withdrawal, checking in"),
                    5: ("Regret, failure, disappointment", "Personal setbacks, self-forgiveness"),
                    6: ("Revisiting the past, childhood memories", "Living in the past, forgiveness"),
                    7: ("Opportunities, choices, wishful thinking", "Alignment, personal values, overwhelmed by choices"),
                    8: ("Disappointment, abandonment, withdrawal", "Trying one more time, indecision"),
                    9: ("Satisfaction, emotional stability, luxury", "Inner happiness, materialism, dissatisfaction"),
                    10: ("Divine love, blissful relationships, harmony", "Disconnection, misaligned values")
                }
            },
            Suit.SWORDS: {
                "element": "Air",
                "keywords": "communication, intellect, conflict, thoughts",
                "numbers": {
                    1: ("New ideas, mental clarity, breakthrough", "Inner clarity, re-thinking an idea"),
                    2: ("Difficult decisions, weighing up options", "Inner turmoil, confusion, information overload"),
                    3: ("Betrayal, hurt, grief, sorrow", "Recovery, forgiveness, moving on"),
                    4: ("Contemplation, rest, relaxation, peace", "Awakening, re-examination, self-reflection"),
                    5: ("Conflict, disagreements, competition", "Inner conflict, releasing stress"),
                    6: ("Transition, change, rite of passage", "Personal transition, resistance to change"),
                    7: ("Betrayal, deception, getting away with something", "Imposter syndrome, self-deception"),
                    8: ("Negative thoughts, self-imposed restriction", "Self-limiting beliefs, inner critic"),
                    9: ("Anxiety, worry, fear, depression", "Inner turmoil, deep-seated fears"),
                    10: ("Painful endings, deep wounds, betrayal", "Recovery, regeneration, resisting an inevitable end")
                }
            },
            Suit.PENTACLES: {
                "element": "Earth",
                "keywords": "material world, career, money, physical manifestation",
                "numbers": {
                    1: ("A new financial or career opportunity", "Lost opportunity, missed chance"),
                    2: ("Multiple priorities, time management", "Over-committed, disorganization, reprioritization"),
                    3: ("Collaboration, learning, implementation", "Disharmony, misalignment, working alone"),
                    4: ("Saving money, security, conservatism", "Over-spending, greed, self-protection"),
                    5: ("Financial insecurity, poverty, lack mindset", "Recovery from financial loss, spiritual poverty"),
                    6: ("Gifts, generosity, sharing", "Self-care, unpaid debts, one-sided charity"),
                    7: ("Long-term view, sustainable results", "Lack of long-term vision, limited success"),
                    8: ("Apprenticeship, repetitive tasks, skill development", "Self-development, perfectionism, misdirected activity"),
                    9: ("Abundance, luxury, self-sufficiency", "Self-worth, over-investment in work, hustling"),
                    10: ("Wealth, financial security, family", "The dark side of wealth, financial failure")
                }
            }
        }
        
        # Create numbered cards (Ace through 10)
        for suit in Suit:
            suit_data = suit_meanings[suit]
            for number in range(1, 11):
                if number in suit_data["numbers"]:
                    upright, reversed = suit_data["numbers"][number]
                    card_name = "Ace" if number == 1 else str(number)
                    self.cards.append(TarotCard(card_name, suit, number, upright, reversed))
        
        # Create court cards
        for suit in Suit:
            for court, meanings in court_meanings.items():
                upright = f"{meanings['upright']} - {suit_meanings[suit]['keywords']}"
                reversed = f"{meanings['reversed']} - {suit_meanings[suit]['keywords']}"
                self.cards.append(TarotCard(court, suit, upright_meaning=upright, reversed_meaning=reversed))
    
    def reset_deck(self):
        """Reset deck and shuffle"""
        self.available_cards = self.cards.copy()
        random.shuffle(self.available_cards)
    
    def draw_card(self, allow_reversed=True) -> TarotCard:
        """Draw a card from the deck"""
        if not self.available_cards:
            raise ValueError("No cards left in deck!")
        
        card = self.available_cards.pop()
        
        # 30% chance for reversed card
        if allow_reversed and random.random() < 0.3:
            card.is_reversed = True
        
        return card
    
    def draw_cards(self, count: int, allow_reversed=True) -> List[TarotCard]:
        """Draw multiple cards from the deck"""
        return [self.draw_card(allow_reversed) for _ in range(count)]

class GeminiAPI:
    """Google Gemini API integration for extensive tarot readings"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        if not self.api_key:
            print("⚠️  Warning: No Gemini API key found. Extensive readings will not be available.")
            print("   Set GEMINI_API_KEY environment variable or pass --api-key to enable.")
    
    def generate_extensive_reading(self, reading: Dict) -> str:
        """Generate an extensive tarot reading using Gemini API"""
        if not self.api_key:
            return "\n❌ Extensive reading unavailable: No Gemini API key configured."
        
        # Prepare the prompt for Gemini
        prompt = self._create_reading_prompt(reading)
        
        try:
            response = self._call_gemini_api(prompt)
            return response
        except Exception as e:
            return f"\n❌ Error generating extensive reading: {e}"
    
    def _create_reading_prompt(self, reading: Dict) -> str:
        """Create a detailed prompt for the Gemini API"""
        cards_info = []
        for position, card in reading['cards'].items():
            cards_info.append(f"- {position}: {card} - {card.get_meaning()}")
        
        cards_text = "\n".join(cards_info)
        
        prompt = f"""
You are an experienced and insightful tarot reader. Please provide a comprehensive, detailed tarot reading based on the following information:

Spread: {reading['name']}
Question: {reading['question']}

Cards drawn:
{cards_text}

Please provide:
1. An overview of the reading's main themes
2. Detailed interpretation of each card in its position
3. How the cards relate to each other and tell a story
4. Practical advice and guidance based on the reading
5. What the querent should focus on or be aware of

Write this as a professional, empathetic, and insightful tarot reading that would be given by an experienced reader. Use a warm, supportive tone while being honest about any challenges indicated. The reading should be approximately 400-600 words.
"""
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Make API call to Google Gemini"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Debug: print response status and content if there's an error
            if response.status_code != 200:
                print(f"API Error {response.status_code}: {response.text}")
                response.raise_for_status()
            
            result = response.json()
            
            # Check for API-level errors
            if 'error' in result:
                raise Exception(f"API Error: {result['error']['message']}")
            
            # Extract the generated text
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text']
                elif 'finishReason' in candidate:
                    raise Exception(f"Generation stopped: {candidate['finishReason']}")
            
            raise Exception(f"Unexpected API response format: {result}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")

class TarotReading:
    def __init__(self, gemini_api: GeminiAPI = None):
        self.deck = TarotDeck()
        self.gemini_api = gemini_api
        
    def three_card_spread(self, question: str = None) -> Dict:
        """Past, Present, Future spread"""
        self.deck.reset_deck()
        cards = self.deck.draw_cards(3)
        
        spread = {
            "name": "Three Card Spread - Past, Present, Future",
            "question": question or "General guidance",
            "cards": {
                "Past": cards[0],
                "Present": cards[1], 
                "Future": cards[2]
            }
        }
        return spread
    
    def celtic_cross_spread(self, question: str = None) -> Dict:
        """Traditional 10-card Celtic Cross spread"""
        self.deck.reset_deck()
        cards = self.deck.draw_cards(10)
        
        spread = {
            "name": "Celtic Cross Spread",
            "question": question or "Comprehensive life guidance",
            "cards": {
                "Present Situation": cards[0],
                "Challenge/Cross": cards[1],
                "Distant Past/Foundation": cards[2],
                "Recent Past": cards[3],
                "Possible Outcome": cards[4],
                "Near Future": cards[5],
                "Your Approach": cards[6],
                "External Influences": cards[7],
                "Hopes and Fears": cards[8],
                "Final Outcome": cards[9]
            }
        }
        return spread
    
    def relationship_spread(self, question: str = None) -> Dict:
        """5-card relationship spread"""
        self.deck.reset_deck()
        cards = self.deck.draw_cards(5)
        
        spread = {
            "name": "Relationship Spread",
            "question": question or "Relationship guidance",
            "cards": {
                "You": cards[0],
                "Your Partner": cards[1],
                "The Relationship": cards[2],
                "Challenges": cards[3],
                "Potential/Outcome": cards[4]
            }
        }
        return spread
    
    def single_card_draw(self, question: str = None) -> Dict:
        """Single card for daily guidance"""
        self.deck.reset_deck()
        card = self.deck.draw_card()
        
        spread = {
            "name": "Single Card Draw",
            "question": question or "Daily guidance",
            "cards": {
                "Your Card": card
            }
        }
        return spread
    
    def yes_no_spread(self, question: str = None) -> Dict:
        """3-card yes/no spread"""
        self.deck.reset_deck()
        cards = self.deck.draw_cards(3)
        
        # Calculate yes/no based on upright vs reversed cards
        upright_count = sum(1 for card in cards if not card.is_reversed)
        answer = "Yes" if upright_count >= 2 else "No"
        confidence = "Strong" if upright_count == 3 or upright_count == 0 else "Moderate"
        
        spread = {
            "name": "Yes/No Spread",
            "question": question or "Yes or No question",
            "answer": f"{answer} ({confidence} indication)",
            "cards": {
                "Card 1": cards[0],
                "Card 2": cards[1],
                "Card 3": cards[2]
            }
        }
        return spread

def print_reading(reading: Dict, gemini_api: GeminiAPI = None, extensive: bool = False):
    """Print a formatted tarot reading"""
    print("=" * 60)
    print(f"🔮 {reading['name']}")
    print("=" * 60)
    print(f"Question: {reading['question']}")
    
    if 'answer' in reading:
        print(f"\nAnswer: {reading['answer']}")
    
    print("\nCards drawn:")
    print("-" * 40)
    
    for position, card in reading['cards'].items():
        print(f"\n📍 {position}:")
        print(f"   🃏 {card}")
        print(f"   💭 {card.get_meaning()}")
    
    print("\n" + "=" * 60)
    
    # Generate extensive reading if requested and API is available
    if extensive and gemini_api:
        print("\n🤖 Generating extensive reading with AI...")
        extensive_reading = gemini_api.generate_extensive_reading(reading)
        print("\n" + "=" * 60)
        print("📖 EXTENSIVE READING")
        print("=" * 60)
        print(extensive_reading)
        print("\n" + "=" * 60)

def interactive_reading(gemini_api: GeminiAPI = None):
    """Interactive tarot reading session"""
    reader = TarotReading(gemini_api)
    
    print("🔮 Welcome to the Tarot Reading Simulator! 🔮")
    if gemini_api and gemini_api.api_key:
        print("✨ AI-powered extensive readings available!")
    print("\nAvailable spreads:")
    print("1. Single Card Draw")
    print("2. Three Card Spread (Past, Present, Future)")
    print("3. Celtic Cross (10 cards)")
    print("4. Relationship Spread (5 cards)")
    print("5. Yes/No Spread (3 cards)")
    
    while True:
        try:
            choice = input("\nChoose a spread (1-5) or 'q' to quit: ").strip().lower()
            
            if choice == 'q':
                print("Thank you for using the Tarot Reading Simulator! 🌟")
                break
            
            question = input("Enter your question (or press Enter for general guidance): ").strip()
            if not question:
                question = None
            
            # Ask about extensive reading if Gemini API is available
            extensive = False
            if gemini_api and gemini_api.api_key:
                extensive_choice = input("Would you like an extensive AI-powered reading? (y/n): ").strip().lower()
                extensive = extensive_choice == 'y'
            
            print("\n🃏 Shuffling the cards...")
            
            if choice == '1':
                reading = reader.single_card_draw(question)
            elif choice == '2':
                reading = reader.three_card_spread(question)
            elif choice == '3':
                reading = reader.celtic_cross_spread(question)
            elif choice == '4':
                reading = reader.relationship_spread(question)
            elif choice == '5':
                reading = reader.yes_no_spread(question)
            else:
                print("Invalid choice. Please select 1-5.")
                continue
            
            print_reading(reading, gemini_api, extensive)
            
            another = input("\nWould you like another reading? (y/n): ").strip().lower()
            if another != 'y':
                print("Thank you for using the Tarot Reading Simulator! 🌟")
                break
                
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tarot Reading Simulator! 🌟")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Tarot Card Reading Simulator")
    parser.add_argument("--spread", "-s", choices=["single", "three", "celtic", "relationship", "yesno"], 
                       help="Type of spread to perform")
    parser.add_argument("--question", "-q", type=str, help="Question for the reading")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--api-key", type=str, help="Google Gemini API key for extensive readings")
    parser.add_argument("--extensive", "-e", action="store_true", 
                       help="Generate extensive AI-powered reading")
    
    args = parser.parse_args()
    
    # Initialize Gemini API
    gemini_api = GeminiAPI(args.api_key)
    
    if args.interactive or not args.spread:
        interactive_reading(gemini_api)
        return
    
    # Non-interactive mode
    reader = TarotReading(gemini_api)
    
    if args.spread == "single":
        reading = reader.single_card_draw(args.question)
    elif args.spread == "three":
        reading = reader.three_card_spread(args.question)
    elif args.spread == "celtic":
        reading = reader.celtic_cross_spread(args.question)
    elif args.spread == "relationship":
        reading = reader.relationship_spread(args.question)
    elif args.spread == "yesno":
        reading = reader.yes_no_spread(args.question)
    
    print_reading(reading, gemini_api, args.extensive)

if __name__ == "__main__":
    main()
