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
    
    def italian_name(self):
        italian_suits = {
            "Wands": "Bastoni",
            "Cups": "Coppe", 
            "Swords": "Spade",
            "Pentacles": "Denari"
        }
        return italian_suits[self.value]

class TarotCard:
    def __init__(self, name: str, suit: Suit = None, number: int = None, 
                 upright_meaning: str = "", reversed_meaning: str = "", is_major: bool = False,
                 italian_name: str = "", italian_upright: str = "", italian_reversed: str = ""):
        self.name = name
        self.suit = suit
        self.number = number
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
        self.is_major = is_major
        self.is_reversed = False
        self.italian_name = italian_name
        self.italian_upright = italian_upright
        self.italian_reversed = italian_reversed
    
    def __str__(self, italian=False):
        if italian and self.italian_name:
            name = self.italian_name
            suit_str = f" di {self.suit.italian_name()}" if self.suit else ""
            reversed_str = " (Rovesciata)" if self.is_reversed else ""
        else:
            name = self.name
            suit_str = f" of {self.suit.value}" if self.suit else ""
            reversed_str = " (Reversed)" if self.is_reversed else ""
        return f"{name}{suit_str}{reversed_str}"
    
    def get_meaning(self, italian=False):
        if italian and self.italian_upright and self.italian_reversed:
            return self.italian_reversed if self.is_reversed else self.italian_upright
        else:
            return self.reversed_meaning if self.is_reversed else self.upright_meaning

class TarotDeck:
    def __init__(self):
        self.cards = []
        self._create_major_arcana()
        self._create_minor_arcana()
        self.reset_deck()
    
    def _create_major_arcana(self):
        major_arcana = [
            ("The Fool", "New beginnings, innocence, spontaneity", "Recklessness, taken advantage of, inconsideration",
             "Il Matto", "Nuovi inizi, innocenza, spontaneità", "Imprudenza, essere ingannati, sconsideratezza"),
            ("The Magician", "Manifestation, resourcefulness, power", "Manipulation, poor planning, untapped talents",
             "Il Mago", "Manifestazione, intraprendenza, potere", "Manipolazione, scarsa pianificazione, talenti non sfruttati"),
            ("The High Priestess", "Intuition, sacred knowledge, divine feminine", "Secrets, disconnected from intuition, withdrawal",
             "La Papessa", "Intuizione, conoscenza sacra, femminino divino", "Segreti, disconnessione dall'intuizione, ritiro"),
            ("The Empress", "Femininity, beauty, nature, nurturing", "Creative block, dependence on others",
             "L'Imperatrice", "Femminilità, bellezza, natura, nutrimento", "Blocco creativo, dipendenza dagli altri"),
            ("The Emperor", "Authority, establishment, structure, father figure", "Domination, excessive control, lack of discipline",
             "L'Imperatore", "Autorità, istituzione, struttura, figura paterna", "Dominazione, controllo eccessivo, mancanza di disciplina"),
            ("The Hierophant", "Spiritual wisdom, religious beliefs, conformity", "Personal beliefs, freedom, challenging the status quo",
             "Il Papa", "Saggezza spirituale, credenze religiose, conformità", "Credenze personali, libertà, sfida dello status quo"),
            ("The Lovers", "Love, harmony, relationships, values alignment", "Self-love, disharmony, imbalance, misalignment of values",
             "Gli Amanti", "Amore, armonia, relazioni, allineamento dei valori", "Amor proprio, disarmonia, squilibrio, disallineamento dei valori"),
            ("The Chariot", "Control, willpower, success, determination", "Lack of control, lack of direction, aggression",
             "Il Carro", "Controllo, forza di volontà, successo, determinazione", "Mancanza di controllo, mancanza di direzione, aggressività"),
            ("Strength", "Strength, courage, persuasion, influence, compassion", "Inner strength, self-doubt, low energy, raw emotion",
             "La Forza", "Forza, coraggio, persuasione, influenza, compassione", "Forza interiore, dubbi su se stessi, poca energia, emozioni crude"),
            ("The Hermit", "Soul searching, introspection, inner guidance", "Isolation, loneliness, withdrawal",
             "L'Eremita", "Ricerca dell'anima, introspezione, guida interiore", "Isolamento, solitudine, ritiro"),
            ("Wheel of Fortune", "Good luck, karma, life cycles, destiny", "Bad luck, lack of control, clinging to control",
             "La Ruota della Fortuna", "Buona fortuna, karma, cicli di vita, destino", "Sfortuna, mancanza di controllo, aggrapparsi al controllo"),
            ("Justice", "Justice, fairness, truth, cause and effect", "Unfairness, lack of accountability, dishonesty",
             "La Giustizia", "Giustizia, equità, verità, causa ed effetto", "Ingiustizia, mancanza di responsabilità, disonestà"),
            ("The Hanged Man", "Waiting, surrender, letting go, new perspective", "Delays, resistance, stalling, indecision",
             "L'Appeso", "Attesa, resa, lasciare andare, nuova prospettiva", "Ritardi, resistenza, procrastinazione, indecisione"),
            ("Death", "Endings, change, transformation, transition", "Resistance to change, personal transformation, inner purging",
             "La Morte", "Fine, cambiamento, trasformazione, transizione", "Resistenza al cambiamento, trasformazione personale, purificazione interiore"),
            ("Temperance", "Balance, moderation, patience, purpose", "Imbalance, excess, self-healing, re-alignment",
             "La Temperanza", "Equilibrio, moderazione, pazienza, scopo", "Squilibrio, eccesso, auto-guarigione, riallineamento"),
            ("The Devil", "Bondage, addiction, sexuality, materialism", "Releasing limiting beliefs, exploring dark thoughts, detachment",
             "Il Diavolo", "Schiavitù, dipendenza, sessualità, materialismo", "Liberazione dalle credenze limitanti, esplorazione di pensieri oscuri, distacco"),
            ("The Tower", "Sudden change, upheaval, chaos, revelation", "Personal transformation, fear of change, averting disaster",
             "La Torre", "Cambiamento improvviso, sconvolgimento, chaos, rivelazione", "Trasformazione personale, paura del cambiamento, evitare il disastro"),
            ("The Star", "Hope, faith, purpose, renewal, spirituality", "Lack of faith, despair, self-trust, disconnection",
             "La Stella", "Speranza, fede, scopo, rinnovamento, spiritualità", "Mancanza di fede, disperazione, fiducia in se stessi, disconnessione"),
            ("The Moon", "Illusion, fear, anxiety, subconscious, intuition", "Release of fear, repressed emotion, inner confusion",
             "La Luna", "Illusione, paura, ansia, subconscio, intuizione", "Liberazione dalla paura, emozioni represse, confusione interiore"),
            ("The Sun", "Positivity, fun, warmth, success, vitality", "Inner child, feeling down, overly optimistic",
             "Il Sole", "Positività, divertimento, calore, successo, vitalità", "Bambino interiore, sentirsi giù, eccessivamente ottimista"),
            ("Judgement", "Judgement, rebirth, inner calling, forgiveness", "Self-doubt, inner critic, ignoring the call",
             "Il Giudizio", "Giudizio, rinascita, chiamata interiore, perdono", "Dubbi su se stessi, critico interiore, ignorare la chiamata"),
            ("The World", "Completion, integration, accomplishment, travel", "Seeking personal closure, short-cuts, delays",
             "Il Mondo", "Completamento, integrazione, realizzazione, viaggio", "Ricerca di chiusura personale, scorciatoie, ritardi")
        ]
        
        for name, upright, reversed, italian_name, italian_upright, italian_reversed in major_arcana:
            self.cards.append(TarotCard(name, upright_meaning=upright, reversed_meaning=reversed, is_major=True,
                                      italian_name=italian_name, italian_upright=italian_upright, italian_reversed=italian_reversed))
    
    def _create_minor_arcana(self):
        # Court cards meanings
        court_meanings = {
            "Page": {
                "upright": "New ideas, enthusiasm, messages",
                "reversed": "Self-doubt, immaturity, lack of progress",
                "italian_name": "Fante",
                "italian_upright": "Nuove idee, entusiasmo, messaggi",
                "italian_reversed": "Dubbi su se stessi, immaturità, mancanza di progresso"
            },
            "Knight": {
                "upright": "Action, adventure, impulsiveness", 
                "reversed": "Inaction, haste, unfinished business",
                "italian_name": "Cavaliere",
                "italian_upright": "Azione, avventura, impulsività",
                "italian_reversed": "Inazione, fretta, affari incompiuti"
            },
            "Queen": {
                "upright": "Compassion, calm, comfort, loyalty",
                "reversed": "Dependency, smothering, selfishness",
                "italian_name": "Regina",
                "italian_upright": "Compassione, calma, comfort, lealtà",
                "italian_reversed": "Dipendenza, soffocamento, egoismo"
            },
            "King": {
                "upright": "Leadership, honor, control",
                "reversed": "Dishonesty, lack of control, weak leadership",
                "italian_name": "Re",
                "italian_upright": "Leadership, onore, controllo",
                "italian_reversed": "Disonestà, mancanza di controllo, leadership debole"
            }
        }
        
        # Numbered cards meanings by suit
        suit_meanings = {
            Suit.WANDS: {
                "element": "Fire",
                "keywords": "creativity, spirituality, passion, inspiration",
                "italian_keywords": "creatività, spiritualità, passione, ispirazione",
                "numbers": {
                    1: ("New creative energy, inspiration", "Delays, lack of motivation", 
                        "Nuova energia creativa, ispirazione", "Ritardi, mancanza di motivazione"),
                    2: ("Future planning, making decisions", "Fear of unknown, lack of planning",
                        "Pianificazione del futuro, prendere decisioni", "Paura dell'ignoto, mancanza di pianificazione"),
                    3: ("Expansion, foresight, overseas opportunities", "Lack of foresight, delays",
                        "Espansione, lungimiranza, opportunità all'estero", "Mancanza di lungimiranza, ritardi"),
                    4: ("Celebration, harmony, homecoming", "Personal celebration, inner harmony",
                        "Celebrazione, armonia, ritorno a casa", "Celebrazione personale, armonia interiore"),
                    5: ("Conflict, disagreements, competition", "Inner conflict, conflict avoidance",
                        "Conflitto, disaccordi, competizione", "Conflitto interiore, evitare i conflitti"),
                    6: ("Public recognition, progress, self-confidence", "Private achievement, self-doubt",
                        "Riconoscimento pubblico, progresso, fiducia in sé", "Successo privato, dubbi su se stessi"),
                    7: ("Challenge, competition, perseverance", "Overwhelmed, giving up",
                        "Sfida, competizione, perseveranza", "Sopraffatti, arrendersi"),
                    8: ("Movement, fast paced change, action", "Delays, frustration, resisting change",
                        "Movimento, cambiamento veloce, azione", "Ritardi, frustrazione, resistenza al cambiamento"),
                    9: ("Resilience, courage, persistence", "Inner courage, weakness",
                        "Resilienza, coraggio, persistenza", "Coraggio interiore, debolezza"),
                    10: ("Burden, extra responsibility, hard work", "Unable to delegate, overstressed",
                         "Fardello, responsabilità extra, lavoro duro", "Incapacità di delegare, troppo stress")
                }
            },
            Suit.CUPS: {
                "element": "Water",
                "keywords": "emotion, spirituality, intuition, relationships",
                "italian_keywords": "emozione, spiritualità, intuizione, relazioni",
                "numbers": {
                    1: ("Love, new relationships, compassion", "Self-love, intuition, repressed emotions",
                        "Amore, nuove relazioni, compassione", "Amor proprio, intuizione, emozioni represse"),
                    2: ("Unified love, partnership, mutual attraction", "Self-love, break-ups, disharmony",
                        "Amore unificato, partnership, attrazione reciproca", "Amor proprio, rotture, disarmonia"),
                    3: ("Celebration, friendship, creativity", "Independence, alone time",
                        "Celebrazione, amicizia, creatività", "Indipendenza, tempo da soli"),
                    4: ("Meditation, contemplation, apathy", "Retreat, withdrawal, checking in",
                        "Meditazione, contemplazione, apatia", "Ritirata, ritiro, fare il punto"),
                    5: ("Regret, failure, disappointment", "Personal setbacks, self-forgiveness",
                        "Rimpianto, fallimento, delusione", "Battute d'arresto personali, auto-perdono"),
                    6: ("Revisiting the past, childhood memories", "Living in the past, forgiveness",
                        "Rivisitare il passato, ricordi d'infanzia", "Vivere nel passato, perdono"),
                    7: ("Opportunities, choices, wishful thinking", "Alignment, personal values, overwhelmed by choices",
                        "Opportunità, scelte, pensiero illusorio", "Allineamento, valori personali, sopraffatti dalle scelte"),
                    8: ("Disappointment, abandonment, withdrawal", "Trying one more time, indecision",
                        "Delusione, abbandono, ritiro", "Provare ancora una volta, indecisione"),
                    9: ("Satisfaction, emotional stability, luxury", "Inner happiness, materialism, dissatisfaction",
                        "Soddisfazione, stabilità emotiva, lusso", "Felicità interiore, materialismo, insoddisfazione"),
                    10: ("Divine love, blissful relationships, harmony", "Disconnection, misaligned values",
                         "Amore divino, relazioni felici, armonia", "Disconnessione, valori disallineati")
                }
            },
            Suit.SWORDS: {
                "element": "Air",
                "keywords": "communication, intellect, conflict, thoughts",
                "italian_keywords": "comunicazione, intelletto, conflitto, pensieri",
                "numbers": {
                    1: ("New ideas, mental clarity, breakthrough", "Inner clarity, re-thinking an idea",
                        "Nuove idee, chiarezza mentale, svolta", "Chiarezza interiore, ripensare un'idea"),
                    2: ("Difficult decisions, weighing up options", "Inner turmoil, confusion, information overload",
                        "Decisioni difficili, valutare le opzioni", "Tumulto interiore, confusione, sovraccarico di informazioni"),
                    3: ("Betrayal, hurt, grief, sorrow", "Recovery, forgiveness, moving on",
                        "Tradimento, dolore, lutto, tristezza", "Recupero, perdono, andare avanti"),
                    4: ("Contemplation, rest, relaxation, peace", "Awakening, re-examination, self-reflection",
                        "Contemplazione, riposo, rilassamento, pace", "Risveglio, riesame, auto-riflessione"),
                    5: ("Conflict, disagreements, competition", "Inner conflict, releasing stress",
                        "Conflitto, disaccordi, competizione", "Conflitto interiore, liberazione dallo stress"),
                    6: ("Transition, change, rite of passage", "Personal transition, resistance to change",
                        "Transizione, cambiamento, rito di passaggio", "Transizione personale, resistenza al cambiamento"),
                    7: ("Betrayal, deception, getting away with something", "Imposter syndrome, self-deception",
                        "Tradimento, inganno, farla franca", "Sindrome dell'impostore, auto-inganno"),
                    8: ("Negative thoughts, self-imposed restriction", "Self-limiting beliefs, inner critic",
                        "Pensieri negativi, restrizione auto-imposta", "Credenze auto-limitanti, critico interiore"),
                    9: ("Anxiety, worry, fear, depression", "Inner turmoil, deep-seated fears",
                        "Ansia, preoccupazione, paura, depressione", "Tumulto interiore, paure profonde"),
                    10: ("Painful endings, deep wounds, betrayal", "Recovery, regeneration, resisting an inevitable end",
                         "Fine dolorose, ferite profonde, tradimento", "Recupero, rigenerazione, resistenza a una fine inevitabile")
                }
            },
            Suit.PENTACLES: {
                "element": "Earth",
                "keywords": "material world, career, money, physical manifestation",
                "italian_keywords": "mondo materiale, carriera, denaro, manifestazione fisica",
                "numbers": {
                    1: ("A new financial or career opportunity", "Lost opportunity, missed chance",
                        "Una nuova opportunità finanziaria o di carriera", "Opportunità persa, occasione mancata"),
                    2: ("Multiple priorities, time management", "Over-committed, disorganization, reprioritization",
                        "Priorità multiple, gestione del tempo", "Impegni eccessivi, disorganizzazione, ripriorizzazione"),
                    3: ("Collaboration, learning, implementation", "Disharmony, misalignment, working alone",
                        "Collaborazione, apprendimento, implementazione", "Disarmonia, disallineamento, lavorare da soli"),
                    4: ("Saving money, security, conservatism", "Over-spending, greed, self-protection",
                        "Risparmiare denaro, sicurezza, conservatorismo", "Spesa eccessiva, avidità, auto-protezione"),
                    5: ("Financial insecurity, poverty, lack mindset", "Recovery from financial loss, spiritual poverty",
                        "Insicurezza finanziaria, povertà, mentalità di scarsità", "Recupero da perdite finanziarie, povertà spirituale"),
                    6: ("Gifts, generosity, sharing", "Self-care, unpaid debts, one-sided charity",
                        "Doni, generosità, condivisione", "Cura di sé, debiti non pagati, carità unilaterale"),
                    7: ("Long-term view, sustainable results", "Lack of long-term vision, limited success",
                        "Visione a lungo termine, risultati sostenibili", "Mancanza di visione a lungo termine, successo limitato"),
                    8: ("Apprenticeship, repetitive tasks, skill development", "Self-development, perfectionism, misdirected activity",
                        "Apprendistato, compiti ripetitivi, sviluppo di competenze", "Auto-sviluppo, perfezionismo, attività mal indirizzata"),
                    9: ("Abundance, luxury, self-sufficiency", "Self-worth, over-investment in work, hustling",
                        "Abbondanza, lusso, auto-sufficienza", "Autostima, sovra-investimento nel lavoro, darsi da fare"),
                    10: ("Wealth, financial security, family", "The dark side of wealth, financial failure",
                         "Ricchezza, sicurezza finanziaria, famiglia", "Il lato oscuro della ricchezza, fallimento finanziario")
                }
            }
        }
        
        # Create numbered cards (Ace through 10)
        for suit in Suit:
            suit_data = suit_meanings[suit]
            for number in range(1, 11):
                if number in suit_data["numbers"]:
                    upright, reversed, italian_upright, italian_reversed = suit_data["numbers"][number]
                    card_name = "Ace" if number == 1 else str(number)
                    italian_card_name = "Asso" if number == 1 else str(number)
                    self.cards.append(TarotCard(card_name, suit, number, upright, reversed,
                                              italian_name=italian_card_name, italian_upright=italian_upright, italian_reversed=italian_reversed))
        
        # Create court cards
        for suit in Suit:
            for court, meanings in court_meanings.items():
                upright = f"{meanings['upright']} - {suit_meanings[suit]['keywords']}"
                reversed = f"{meanings['reversed']} - {suit_meanings[suit]['keywords']}"
                italian_upright = f"{meanings['italian_upright']} - {suit_meanings[suit]['italian_keywords']}"
                italian_reversed = f"{meanings['italian_reversed']} - {suit_meanings[suit]['italian_keywords']}"
                self.cards.append(TarotCard(court, suit, upright_meaning=upright, reversed_meaning=reversed,
                                          italian_name=meanings['italian_name'], italian_upright=italian_upright, italian_reversed=italian_reversed))
    
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
    
    def generate_extensive_reading(self, reading: Dict, italian: bool = False) -> str:
        """Generate an extensive tarot reading using Gemini API"""
        if not self.api_key:
            error_msg = "\n❌ Lettura estesa non disponibile: Nessuna chiave API Gemini configurata." if italian else "\n❌ Extensive reading unavailable: No Gemini API key configured."
            return error_msg
        
        # Prepare the prompt for Gemini
        prompt = self._create_reading_prompt(reading, italian)
        
        try:
            response = self._call_gemini_api(prompt)
            return response
        except Exception as e:
            error_msg = f"\n❌ Errore nella generazione della lettura estesa: {e}" if italian else f"\n❌ Error generating extensive reading: {e}"
            return error_msg
    
    def _create_reading_prompt(self, reading: Dict, italian: bool = False) -> str:
        """Create a detailed prompt for the Gemini API"""
        cards_info = []
        for position, card in reading['cards'].items():
            cards_info.append(f"- {position}: {card.__str__(italian)} - {card.get_meaning(italian)}")
        
        cards_text = "\n".join(cards_info)
        
        if italian:
            prompt = f"""
Sei un lettore di tarocchi esperto e perspicace. Fornisci una lettura dei tarocchi completa e dettagliata basata sulle seguenti informazioni:

Stesa: {reading['name']}
Domanda: {reading['question']}

Carte estratte:
{cards_text}

Per favore fornisci:
1. Una panoramica dei temi principali della lettura
2. Interpretazione dettagliata di ogni carta nella sua posizione
3. Come le carte si relazionano tra loro e raccontano una storia
4. Consigli pratici e guida basati sulla lettura
5. Su cosa il consultante dovrebbe concentrarsi o essere consapevole

Scrivi questa come una lettura dei tarocchi professionale, empatica e perspicace che verrebbe data da un lettore esperto. Usa un tono caloroso e di supporto mentre sei onesto riguardo a eventuali sfide indicate. La lettura dovrebbe essere di circa 400-600 parole.
"""
        else:
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

def print_reading(reading: Dict, gemini_api: GeminiAPI = None, extensive: bool = False, italian: bool = False):
    """Print a formatted tarot reading"""
    print("=" * 60)
    
    # Translate spread names if Italian mode
    if italian:
        italian_spread_names = {
            "Single Card Draw": "Estrazione Carta Singola",
            "Three Card Spread - Past, Present, Future": "Stesa di Tre Carte - Passato, Presente, Futuro",
            "Celtic Cross Spread": "Croce Celtica",
            "Relationship Spread": "Stesa delle Relazioni",
            "Yes/No Spread": "Stesa Sì/No"
        }
        name = italian_spread_names.get(reading['name'], reading['name'])
        question_label = "Domanda"
        answer_label = "Risposta"
        cards_drawn_label = "Carte estratte"
        
        # Translate position names
        italian_positions = {
            "Past": "Passato",
            "Present": "Presente", 
            "Future": "Futuro",
            "Your Card": "La Tua Carta",
            "Present Situation": "Situazione Presente",
            "Challenge/Cross": "Sfida/Croce",
            "Distant Past/Foundation": "Passato Lontano/Fondazione",
            "Recent Past": "Passato Recente",
            "Possible Outcome": "Risultato Possibile",
            "Near Future": "Futuro Prossimo",
            "Your Approach": "Il Tuo Approccio",
            "External Influences": "Influenze Esterne",
            "Hopes and Fears": "Speranze e Paure",
            "Final Outcome": "Risultato Finale",
            "You": "Tu",
            "Your Partner": "Il Tuo Partner",
            "The Relationship": "La Relazione",
            "Challenges": "Sfide",
            "Potential/Outcome": "Potenziale/Risultato",
            "Card 1": "Carta 1",
            "Card 2": "Carta 2",
            "Card 3": "Carta 3"
        }
    else:
        name = reading['name']
        question_label = "Question"
        answer_label = "Answer"
        cards_drawn_label = "Cards drawn"
        italian_positions = {}
    
    print(f"🔮 {name}")
    print("=" * 60)
    print(f"{question_label}: {reading['question']}")
    
    if 'answer' in reading:
        # Translate Yes/No answers if in Italian
        if italian:
            answer = reading['answer']
            answer = answer.replace('Yes', 'Sì').replace('No', 'No')
            answer = answer.replace('Strong', 'Forte').replace('Moderate', 'Moderata')
            answer = answer.replace('indication', 'indicazione')
        else:
            answer = reading['answer']
        print(f"\n{answer_label}: {answer}")
    
    print(f"\n{cards_drawn_label}:")
    print("-" * 40)
    
    for position, card in reading['cards'].items():
        translated_position = italian_positions.get(position, position) if italian else position
        print(f"\n📍 {translated_position}:")
        print(f"   🃏 {card.__str__(italian)}")
        print(f"   💭 {card.get_meaning(italian)}")
    
    print("\n" + "=" * 60)
    
    # Generate extensive reading if requested and API is available
    if extensive and gemini_api:
        loading_msg = "🤖 Generazione lettura estesa con IA..." if italian else "🤖 Generating extensive reading with AI..."
        header_msg = "📖 LETTURA ESTESA" if italian else "📖 EXTENSIVE READING"
        print(f"\n{loading_msg}")
        extensive_reading = gemini_api.generate_extensive_reading(reading, italian)
        print("\n" + "=" * 60)
        print(header_msg)
        print("=" * 60)
        print(extensive_reading)
        print("\n" + "=" * 60)

def interactive_reading(gemini_api: GeminiAPI = None, italian: bool = False):
    """Interactive tarot reading session"""
    reader = TarotReading(gemini_api)
    
    if italian:
        print("🔮 Benvenuto al Simulatore di Lettura dei Tarocchi! 🔮")
        if gemini_api and gemini_api.api_key:
            print("✨ Letture estese potenziate dall'IA disponibili!")
        print("\nStese disponibili:")
        print("1. Estrazione Carta Singola")
        print("2. Stesa di Tre Carte (Passato, Presente, Futuro)")
        print("3. Croce Celtica (10 carte)")
        print("4. Stesa delle Relazioni (5 carte)")
        print("5. Stesa Sì/No (3 carte)")
        
        spread_choice_prompt = "\nScegli una stesa (1-5) o 'q' per uscire: "
        question_prompt = "Inserisci la tua domanda (o premi Invio per una guida generale): "
        extensive_prompt = "Vorresti una lettura estesa alimentata dall'IA? (s/n): "
        shuffling_msg = "\n🃏 Mescolando le carte..."
        invalid_msg = "Scelta non valida. Seleziona 1-5."
        another_prompt = "\nVorresti un'altra lettura? (s/n): "
        goodbye_msg = "Grazie per aver usato il Simulatore di Lettura dei Tarocchi! 🌟"
        error_msg = "Si è verificato un errore: {}"
        extensive_yes = 's'
        another_yes = 's'
        quit_key = 'q'
    else:
        print("🔮 Welcome to the Tarot Reading Simulator! 🔮")
        if gemini_api and gemini_api.api_key:
            print("✨ AI-powered extensive readings available!")
        print("\nAvailable spreads:")
        print("1. Single Card Draw")
        print("2. Three Card Spread (Past, Present, Future)")
        print("3. Celtic Cross (10 cards)")
        print("4. Relationship Spread (5 cards)")
        print("5. Yes/No Spread (3 cards)")
        
        spread_choice_prompt = "\nChoose a spread (1-5) or 'q' to quit: "
        question_prompt = "Enter your question (or press Enter for general guidance): "
        extensive_prompt = "Would you like an extensive AI-powered reading? (y/n): "
        shuffling_msg = "\n🃏 Shuffling the cards..."
        invalid_msg = "Invalid choice. Please select 1-5."
        another_prompt = "\nWould you like another reading? (y/n): "
        goodbye_msg = "Thank you for using the Tarot Reading Simulator! 🌟"
        error_msg = "An error occurred: {}"
        extensive_yes = 'y'
        another_yes = 'y'
        quit_key = 'q'
    
    while True:
        try:
            choice = input(spread_choice_prompt).strip().lower()
            
            if choice == quit_key:
                print(goodbye_msg)
                break
            
            question = input(question_prompt).strip()
            if not question:
                question = None
            
            # Ask about extensive reading if Gemini API is available
            extensive = False
            if gemini_api and gemini_api.api_key:
                extensive_choice = input(extensive_prompt).strip().lower()
                extensive = extensive_choice == extensive_yes
            
            print(shuffling_msg)
            
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
                print(invalid_msg)
                continue
            
            print_reading(reading, gemini_api, extensive, italian)
            
            another = input(another_prompt).strip().lower()
            if another != another_yes:
                print(goodbye_msg)
                break
                
        except KeyboardInterrupt:
            print(f"\n\n{goodbye_msg}")
            break
        except Exception as e:
            print(error_msg.format(e))

def main():
    parser = argparse.ArgumentParser(description="Tarot Card Reading Simulator")
    parser.add_argument("--spread", "-s", choices=["single", "three", "celtic", "relationship", "yesno"], 
                       help="Type of spread to perform")
    parser.add_argument("--question", "-q", type=str, help="Question for the reading")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--italian", "-it", action="store_true",
                       help="Display cards and meanings in Italian")
    parser.add_argument("--api-key", type=str, help="Google Gemini API key for extensive readings")
    parser.add_argument("--extensive", "-e", action="store_true", 
                       help="Generate extensive AI-powered reading")
    
    args = parser.parse_args()
    
    # Initialize Gemini API
    gemini_api = GeminiAPI(args.api_key)
    
    if args.interactive or not args.spread:
        interactive_reading(gemini_api, args.italian)
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
    
    print_reading(reading, gemini_api, args.extensive, args.italian)

if __name__ == "__main__":
    main()
