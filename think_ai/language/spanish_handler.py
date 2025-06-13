"""Spanish language handler for Think AI
Maneja español latinoamericano perfectamente con contexto inteligente.
"""

import re
import time


class SpanishHandler:
    def __init__(self) -> None:
        # Memoria de conversación para contexto
        self.conversation_memory = []
        self.last_language_detected = None
        self.conversation_start_time = time.time()

        # Patrones de español más inteligentes
        self.spanish_patterns = [
            r"\b(hola|qué tal|que tal|cómo estás|como estas|buenos días|buenas tardes|buenas noches)\b",
            r"\b(hablas español|habla español|español|castellano)\b",
            r"\b(qué|que|cómo|como|cuándo|cuando|dónde|donde|por qué|porque|quién|quien)\b",
            r"\b(gracias|por favor|perdón|perdon|disculpa|disculpe)\b",
            r"\b(sí|si|no|tal vez|talvez|quizás|quizas)\b",
            r"\¿.*\?",  # Preguntas con signos de interrogación españoles
            r"\b(ayuda|ayudar|necesito|quiero|puedes|puede)\b",
            r"\b(bien|muy bien|mal|regular|más o menos|excelente)\b",
            r"\b(claro|obvio|por supuesto|desde luego|seguro)\b",
            r"\b(perfecto|genial|fantástico|increíble|maravilloso)\b",
        ]

        # Palabras muy comunes en español (alta confianza)
        self.high_confidence_spanish = [
            "hola",
            "ola",
            "gracias",
            "por favor",
            "perdón",
            "disculpa",
            "adiós",
            "hasta luego",
            "buenos días",
            "buenas tardes",
            "buenas noches",
            "cómo estás",
            "como estas",
            "qué tal",
            "que tal",
            "muy bien",
            "bien",
            "español",
            "castellano",
            "continua",
            "continúa",
            "explicame",
            "explícame",
            "ayudame",
            "ayúdame",
        ]

        # Palabras medianamente comunes (confianza media)
        self.medium_confidence_spanish = [
            "el",
            "la",
            "de",
            "que",
            "y",
            "a",
            "en",
            "un",
            "es",
            "para",
            "una",
            "del",
            "con",
            "por",
            "se",
            "su",
            "lo",
            "te",
            "me",
            "mi",
            "tu",
            "muy",
            "todo",
            "nada",
            "algo",
            "estar",
            "ser",
            "tener",
            "hacer",
            "ir",
            "ver",
            "dar",
            "saber",
            "querer",
            "decir",
            "poder",
            "donde",
            "cuando",
            "quien",
            "porque",
        ]

        # Palabras de contenido español (alta confianza para temas específicos)
        self.content_spanish_words = [
            "amor",
            "cancion",
            "canción",
            "música",
            "musica",
            "vida",
            "tiempo",
            "día",
            "casa",
            "agua",
            "trabajo",
            "familia",
            "amigo",
            "amiga",
            "corazón",
            "corazon",
            "feliz",
            "triste",
            "alegre",
            "bonito",
            "hermoso",
            "grande",
            "pequeño",
            "blanco",
            "negro",
            "rojo",
            "azul",
            "verde",
            "amarillo",
            "lunes",
            "martes",
            "miércoles",
            "jueves",
            "viernes",
            "sábado",
            "domingo",
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]

        # Respuestas por región
        self.greetings = {
            "general": "¡Hola! ¡Claro que hablo español! ¿Cómo estás? ¿En qué puedo ayudarte?",
            "mexico": "¡Órale! ¡Qué onda! Claro que hablo español, güey. ¿En qué te puedo echar la mano?",
            "argentina": "¡Hola che! ¡Por supuesto que hablo español! ¿Cómo andás? ¿En qué te puedo ayudar?",
            "colombia": "¡Hola parce! ¡Claro que sí! Hablo español perfectamente. ¿Qué más? ¿En qué te colaboro?",
            "chile": "¡Hola! ¡Obvio que hablo español po! ¿Cachai? ¿En qué te puedo ayudar?",
        }

        # Frases útiles
        self.useful_phrases = {
            "agreement": [
                "¡Dale!",
                "¡Claro!",
                "¡Por supuesto!",
                "¡Obvio!",
                "¡Sí, señor!",
            ],
            "thinking": [
                "A ver...",
                "Déjame pensar...",
                "Mira...",
                "Bueno..."],
            "enthusiasm": [
                "¡Qué chévere!",
                "¡Qué padre!",
                "¡Genial!",
                "¡Bacano!",
                "¡Qué buena onda!",
            ],
        }

    def add_to_conversation_memory(self, text: str, language: str) -> None:
        """Añade texto a la memoria de conversación."""
        self.conversation_memory.append(
            {
                "text": text,
                "language": language,
                "timestamp": time.time(),
            }
        )

        # Mantener solo las últimas 10 interacciones
        if len(self.conversation_memory) > 10:
            self.conversation_memory = self.conversation_memory[-10:]

    def get_conversation_context(self) -> str:
        """Obtiene el contexto de idioma de la conversación."""
        if not self.conversation_memory:
            return "unknown"

        # Contar idiomas en las últimas interacciones
        recent_languages = [item["language"]
                            for item in self.conversation_memory[-5:]]
        spanish_count = recent_languages.count("spanish")

        if spanish_count >= 2:  # Si 2+ de las últimas 5 fueron en español
            return "spanish_context"
        if spanish_count >= 1:
            return "mixed_context"
        return "english_context"

    def detect_spanish(self, text: str) -> bool:
        """Detecta si el texto está en español con contexto inteligente."""
        text_lower = text.lower().strip()
        words = text_lower.split()

        # 1. Verificar patrones explícitos de español
        for pattern in self.spanish_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        # 2. Verificar palabras de alta confianza
        for phrase in self.high_confidence_spanish:
            if phrase in text_lower:
                return True

        # 3. Análisis por peso de palabras
        high_conf_count = sum(
            1 for word in words if word in self.high_confidence_spanish
        )
        content_conf_count = sum(
            1 for word in words if word in self.content_spanish_words
        )
        medium_conf_count = sum(
            1 for word in words if word in self.medium_confidence_spanish
        )

        # Calcular puntuación de confianza
        confidence_score = ((high_conf_count * 4) +
                            (content_conf_count * 2) + (medium_conf_count * 1))
        total_words = len(words)

        if total_words == 0:
            return False

        # 4. Considerar contexto de conversación
        context = self.get_conversation_context()

        # Umbrales adaptativos según contexto
        if context == "spanish_context":
            # En contexto español, ser más permisivo
            threshold = 0.3
        elif context == "mixed_context":
            # En contexto mixto, umbral normal
            threshold = 0.8
        else:
            # En contexto inglés o desconocido, ser más estricto
            threshold = 1.2

        confidence_ratio = confidence_score / total_words

        # 5. Casos especiales para frases muy cortas
        if total_words <= 3:
            # Para frases cortas, ser más específico
            if high_conf_count > 0 or content_conf_count > 0:
                return True
            # Si estamos en contexto español y hay al menos una palabra
            # española
            if context == "spanish_context" and (
                medium_conf_count > 0 or content_conf_count > 0
            ):
                return True

        return confidence_ratio >= threshold

    def detect_region(self, text: str) -> str:
        """Detecta la región basándose en el vocabulario."""
        text_lower = text.lower()

        # Marcadores regionales
        if any(
            word in text_lower for word in [
                "güey",
                "órale",
                "chido",
                "neta",
                "morro"]):
            return "mexico"
        if any(
            word in text_lower for word in [
                "che",
                "boludo",
                "vos",
                "laburo",
                "pibe"]):
            return "argentina"
        if any(
            word in text_lower for word in [
                "parce",
                "bacano",
                "chimba",
                "parcero"]):
            return "colombia"
        if any(
            word in text_lower for word in [
                "weon",
                "cachai",
                "po",
                "fome",
                "pololo"]):
            return "chile"

        return "general"

    def is_harmful_request(self, query: str) -> bool:
        """Detecta solicitudes potencialmente dañinas."""
        harmful_keywords = [
            "pistola",
            "arma",
            "bomba",
            "explosivo",
            "veneno",
            "droga",
            "hackear",
            "hack",
            "robar",
            "matar",
            "violencia",
            "suicidio",
            "dañar",
            "lastimar",
            "herir",
            "weapon",
            "gun",
            "bomb",
            "poison",
            "drug",
            "kill",
            "harm",
            "violence",
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in harmful_keywords)

    def generate_spanish_response(
            self,
            query: str,
            context: dict | None = None) -> str:
        """Genera una respuesta en español apropiada."""
        query_lower = query.lower()
        region = self.detect_region(query)

        # Filtro de seguridad
        if self.is_harmful_request(query):
            safety_responses = {
                "general": "Lo siento, pero no puedo ayudarte con eso. ¿Hay algo más en lo que pueda asistirte de manera positiva?",
                "mexico": "Lo siento carnal, pero no puedo ayudarte con eso. ¿En qué más te puedo echar la mano?",
                "argentina": "Disculpá che, pero no puedo ayudarte con eso. ¿Hay algo más en lo que te pueda ayudar?",
                "colombia": "Perdón parce, pero no puedo ayudarte con eso. ¿En qué más te puedo colaborar?",
                "chile": "Perdón po, pero no puedo ayudarte con eso. ¿En qué más te puedo ayudar?",
            }
            return safety_responses.get(region, safety_responses["general"])

        # Respuestas a preguntas comunes
        if "hablas español" in query_lower or "habla español" in query_lower:
            return self.greetings[region]

        if any(
            greeting in query_lower
            for greeting in [
                "hola",
                "qué tal",
                "que tal",
                "buenos días",
                "buenas tardes",
                "buenas noches",
                "saludos",
            ]
        ):
            responses = {
                "general": "¡Hola! ¿Cómo estás? Soy Think AI y puedo ayudarte en español perfectamente. ¿Qué necesitas?",
                "mexico": "¡Qué onda! ¿Cómo estás, carnalito? Aquí andamos, echándole ganas. ¿En qué te ayudo?",
                "argentina": "¡Hola che! ¿Todo bien? ¿Cómo va eso? Dale, contame en qué te puedo ayudar.",
                "colombia": "¡Ey, qué más pues! ¿Bien o qué? Aquí estoy para lo que necesites, parce.",
                "chile": "¡Hola! ¿Cómo estái? Aquí andamos al firme. ¿En qué te puedo ayudar?",
            }
            return responses.get(region, responses["general"])

        if "cómo estás" in query_lower or "como estas" in query_lower:
            responses = {
                "general": "¡Muy bien, gracias por preguntar! Como IA, siempre estoy lista para ayudarte. ¿Y tú cómo estás?",
                "mexico": "¡De pelos, carnal! Aquí andamos al cien. ¿Y tú qué tal?",
                "argentina": "¡De diez, che! Siempre pilas para ayudarte. ¿Vos cómo andás?",
                "colombia": "¡Súper bien, parce! Full pilas para colaborarte. ¿Y vos qué tal?",
                "chile": "¡Pulento! Siempre ready para ayudarte. ¿Y tú cómo estái?",
            }
            return responses.get(region, responses["general"])

        if any(
            word in query_lower
            for word in ["bien", "muy bien", "excelente", "genial", "perfecto"]
        ):
            responses = {
                "general": "¡Qué bueno saber que estás bien! Me alegra mucho. ¿En qué puedo ayudarte hoy?",
                "mexico": "¡Qué padre, carnal! Me da mucho gusto. ¿En qué te puedo echar la mano?",
                "argentina": "¡Qué bueno che! Me alegra un montón. ¿En qué te puedo ayudar?",
                "colombia": "¡Qué bacano parce! Me alegra mucho saberlo. ¿En qué te colaboro?",
                "chile": "¡Qué buena po! Me alegra caleta. ¿En qué te puedo ayudar?",
            }
            return responses.get(region, responses["general"])

        if "y tu" in query_lower or "y tú" in query_lower:
            responses = {
                "general": "¡Muy bien también, gracias! Siempre lista para ayudarte. ¿Qué necesitas?",
                "mexico": "¡Al cien también, carnal! Siempre aquí para echarte la mano. ¿Qué ocupas?",
                "argentina": "¡Bárbaro también, che! Siempre acá para ayudarte. ¿Qué necesitás?",
                "colombia": "¡Súper bien también, parce! Siempre aquí para colaborarte. ¿Qué necesitás?",
                "chile": "¡Pulento también po! Siempre aquí para ayudarte. ¿Qué necesitái?",
            }
            return responses.get(region, responses["general"])

        if "gracias" in query_lower:
            responses = {
                "general": "¡De nada! Es un placer ayudarte. ¿Necesitas algo más?",
                "mexico": "¡No hay de qué, carnal! Pa' eso estamos. ¿Algo más en qué te pueda echar la mano?",
                "argentina": "¡No hay drama, che! Un gusto ayudarte. ¿Necesitás algo más?",
                "colombia": "¡Con mucho gusto, parce! Para eso estoy. ¿Algo más en qué te pueda colaborar?",
                "chile": "¡De nada po! Bacán poder ayudarte. ¿Necesitái algo más?",
            }
            return responses.get(region, responses["general"])

        # Respuestas específicas a temas comunes (antes del catch-all)
        if (
            "continua" in query_lower
            or "continúa" in query_lower
            or "sigue" in query_lower
        ):
            responses = {
                "general": "¡Por supuesto! Continúo con el tema. ¿Qué te gustaría que desarrolle más específicamente?",
                "mexico": "¡Órale, claro que sí! Sigo con el tema, carnal. ¿Qué quieres que te explique más a fondo?",
                "argentina": "¡Dale che! Sigo con lo que estábamos hablando. ¿Qué querés que profundice más?",
                "colombia": "¡Claro que sí parce! Continúo con el tema. ¿Qué querés que te explique mejor?",
                "chile": "¡Ya po! Sigo con el tema. ¿Qué querís que te explique más?",
            }
            return responses.get(region, responses["general"])

        if "amor" in query_lower:
            responses = {
                "general": "¡Qué tema tan hermoso! El amor es una de las emociones más poderosas. ¿Te gustaría que te ayude con algo específico sobre el amor?",
                "mexico": "¡Órale! El amor es lo más chido que hay, carnal. ¿En qué te puedo ayudar con eso?",
                "argentina": "¡Qué lindo che! El amor es todo. ¿Querés que te ayude con algo específico?",
                "colombia": "¡Bacano parce! El amor es lo más chimba. ¿En qué te puedo colaborar?",
                "chile": "¡Pulento! El amor es lo más lindo po. ¿En qué te ayudo?",
            }
            return responses.get(region, responses["general"])

        if (
            "cancion" in query_lower
            or "música" in query_lower
            or "musica" in query_lower
        ):
            responses = {
                "general": "¡Me encanta la música! ¿Te gustaría que te ayude a crear una canción, encontrar letras, o algo relacionado con música?",
                "mexico": "¡Qué padre la música, güey! ¿Quieres que te ayude con una rola o algo así?",
                "argentina": "¡La música es todo che! ¿Querés que te ayude con algún tema musical?",
                "colombia": "¡La música es muy bacana parce! ¿Te ayudo con algo musical?",
                "chile": "¡La música es muy buena po! ¿En qué te puedo ayudar con eso?",
            }
            return responses.get(region, responses["general"])

        # Para otras preguntas en español (catch-all)
        if self.detect_spanish(query):
            return self._generate_contextual_response(query, region, context)

        return None  # No es español o no tenemos respuesta específica

    def _generate_contextual_response(
        self, query: str, region: str, context: dict | None = None
    ) -> str:
        """Genera respuestas contextuales en español."""
        # Agregar marcadores regionales
        regional_markers = {
            "mexico": " güey",
            "argentina": " che",
            "colombia": " parce",
            "chile": " po",
            "general": "",
        }

        marker = regional_markers.get(region, "")

        # Base response
        response = f"Entiendo tu pregunta{marker}. "

        # Add contextual information if available
        if context and "topic" in context:
            response += f"Sobre {context['topic']}, "

        response += "Déjame ayudarte con eso. "

        # Add regional flavor
        if region == "mexico":
            response += "La neta es que puedo explicarte todo con detalle."
        elif region == "argentina":
            response += "Te voy a explicar todo de una, sin vueltas."
        elif region == "colombia":
            response += "Te voy a explicar todo bien bacano."
        elif region == "chile":
            response += "Te voy a explicar todo clarito."
        else:
            response += "Te voy a explicar todo claramente."

        return response

    def detect_language(self, text: str) -> str:
        """Detect the language of the text."""
        text_lower = text.lower().strip()

        # Spanish detection (existing)
        if self.detect_spanish(text):
            return "spanish"

        # French detection
        french_words = [
            "bonjour",
            "salut",
            "comment",
            "merci",
            "oui",
            "non",
            "ça va",
            "bonsoir",
        ]
        if any(word in text_lower for word in french_words):
            return "french"

        # German detection
        german_words = [
            "hallo",
            "guten tag",
            "wie geht",
            "danke",
            "ja",
            "nein",
            "auf wiedersehen",
        ]
        if any(word in text_lower for word in german_words):
            return "german"

        # Japanese detection (basic hiragana/katakana/kanji)
        if any(
            "\u3040" <= char <= "\u309f"
            or "\u30a0" <= char <= "\u30ff"
            or "\u4e00" <= char <= "\u9faf"
            for char in text
        ):
            return "japanese"

        # Portuguese detection
        portuguese_words = [
            "olá",
            "oi",
            "como está",
            "obrigado",
            "sim",
            "não",
            "tchau"]
        if any(word in text_lower for word in portuguese_words):
            return "portuguese"

        return "english"

    def should_respond_in_spanish(self, query: str) -> bool:
        """Determina si debemos responder en español."""
        return self.detect_spanish(query)

    def generate_multilingual_response(self, query: str, language: str) -> str:
        """Generate response in detected language."""
        if language == "spanish":
            return self.generate_spanish_response(query)
        if language == "french":
            return "Bonjour! Je suis Think AI et je peux vous aider en français. Comment puis-je vous aider?"
        if language == "german":
            return "Hallo! Ich bin Think AI und kann Ihnen auf Deutsch helfen. Wie kann ich Ihnen helfen?"
        if language == "japanese":
            return "こんにちは！私はThink AIです。日本語でお手伝いできます。どのようにお手伝いしましょうか？"
        if language == "portuguese":
            return (
                "Olá! Eu sou Think AI e posso ajudá-lo em português. Como posso ajudar?"
            )
        return None

    def translate_response(
            self,
            english_response: str,
            region: str = "general") -> str:
        """Traduce una respuesta del inglés al español con sabor regional."""
        # This is a simplified translation - in production you'd use a proper translation service
        # For now, we'll provide some common translations

        translations = {
            "I understand": "Entiendo",
            "Let me help you": "Déjame ayudarte",
            "Based on my understanding": "Basándome en mi comprensión",
            "I can tell you": "Te puedo decir",
            "Great question": "Excelente pregunta",
        }

        response = english_response
        for eng, esp in translations.items():
            response = response.replace(eng, esp)

        # Add regional flavor
        if region == "mexico":
            response = response.replace("Entiendo", "Ya entendí, carnal")
        elif region == "argentina":
            response = response.replace("Entiendo", "Ya entendí, che")
        elif region == "colombia":
            response = response.replace("Entiendo", "Ya pillé, parce")

        return response


# Singleton instance
spanish_handler = SpanishHandler()
