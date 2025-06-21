#! / usr / bin / env python3

"""Test deployment of Think AI v2.1.0 Contextual Multilingual Intelligence."""

import subprocess

from think_ai.language.spanish_handler import spanish_handler

# Test comprehensive language detection with all improvements
test_scenarios = [
("hola", "Spanish greeting"),
("bien y tu", "Spanish contextual response"),
("una cancion de amor", "Spanish content phrase"),
("puedes explicarme la teoria de cuerdas", "Complex Spanish technical question"),
("bonjour comment allez - vous", "French greeting"),
("guten tag wie geht es ihnen", "German greeting"),
("こんにちは元気ですか", "Japanese greeting"),
("olá como está", "Portuguese greeting"),
("hello how are you", "English baseline"),
]

for _i, (query, _description) in enumerate(test_scenarios, 1):
    detected = spanish_handler.detect_language(query)
    is_spanish = spanish_handler.detect_spanish(query)
    context = spanish_handler.get_conversation_context()

    if detected ! = "english":
        response = spanish_handler.generate_multilingual_response(query, detected)
        if response:
            pass
    else:
        pass

# Test API endpoints

    api_tests = [
    ("hola", "Spanish greeting"),
    ("una cancion de amor", "Spanish content"),
    ("bonjour", "French greeting"),
    ]

    for query, _desc in api_tests:
        try:
            result = subprocess.run([
            "curl", "-X", "POST", "http://localhost:8080 / api / v1 / think",
            "-H", "Content - Type: application / json",
            "-d", f"{{"query": "{query}", "enable_consciousness": true}}",
            ], check=False, capture_output=True, text=True, timeout=10)

            if result.returncode = = 0:
                pass
        else:
            pass
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass
