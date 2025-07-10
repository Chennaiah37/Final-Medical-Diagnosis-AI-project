"""
🎉  Rule‑Based AI Medical Diagnosis – Minimal / Color‑Smart
===========================================================
• Detects if the output **really** supports ANSI colors.  
  → Colors on in most Unix‑style terminals.  
  → Plain text everywhere else (IDLE, basic Windows cmd, notebooks).
• **Interactive Mode** when run in a terminal; demo mode otherwise.
"""

import os
import sys
from typing import Dict, List, Set
def _supports_color() -> bool:
    if os.getenv("NO_COLOR", "0") == "1":  # user override
        return False
    if sys.platform.startswith("win") and os.getenv("ANSICON") is None:
        return False  # plain Windows cmd usually lacks ANSI
    if not sys.stdout.isatty():
        return False
    term = os.getenv("TERM", "")
    return term and term not in {"dumb", ""}

USE_COLOR = _supports_color()

RESET = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
DIM = "\033[2m" if USE_COLOR else ""
CYAN = "\033[36m" if USE_COLOR else ""
GREEN = "\033[32m" if USE_COLOR else ""
YELLOW = "\033[33m" if USE_COLOR else ""
MAGENTA = "\033[35m" if USE_COLOR else ""
RED = "\033[31m" if USE_COLOR else ""
BLUE = "\033[34m" if USE_COLOR else ""


def c(text: str, style: str) -> str:
    """Return colored or plain text based on USE_COLOR."""
    return f"{style}{text}{RESET}" if USE_COLOR else text
DISEASE_RULES: Dict[str, Set[str]] = {
    "flu": {"fever", "cough", "body_ache", "fatigue"},
    "common cold": {"cough", "sore_throat", "runny_nose"},
    "asthma": {"shortness_breath", "wheezing", "cough"},
    "covid-19": {"fever", "loss_smell", "cough", "sore_throat"},
    "pneumonia": {"fever", "cough", "shortness_breath", "chest_pain"},
    "migraine": {"headache", "blurred_vision", "nausea"},
    "diabetes": {"fatigue", "thirst", "frequent_urination", "blurred_vision"},
    "hypertension": {"headache", "dizziness", "blurred_vision"},
    "arthritis": {"joint_pain", "stiffness", "swelling"},
    "appendicitis": {"abdominal_pain", "vomiting", "loss_appetite", "fever"},
    "tuberculosis": {"chronic_cough", "weight_loss", "night_sweats", "chest_pain"},
    "depression": {"fatigue", "loss_interest", "sadness", "sleep_disturbance"},
    "conjunctivitis": {"red_eyes", "itchy_eyes", "eye_discharge"},
    "food_poisoning": {"vomiting", "diarrhea", "nausea", "abdominal_pain"},
}

DISEASE_TO_SPECIALIST: Dict[str, str] = {
    "flu": "General Physician",
    "common cold": "General Physician",
    "diabetes": "Endocrinologist",
    "hypertension": "Cardiologist",
    "asthma": "Pulmonologist",
    "pneumonia": "Pulmonologist",
    "migraine": "Neurologist",
    "arthritis": "Rheumatologist",
    "covid-19": "Infectious Disease Specialist",
    "appendicitis": "General Surgeon",
    "tuberculosis": "Pulmonologist",
    "depression": "Psychiatrist",
    "conjunctivitis": "Ophthalmologist",
    "food_poisoning": "Gastroenterologist",
}

ALL_SYMPTOMS = sorted({s for sset in DISEASE_RULES.values() for s in sset})

def banner():
    print(c("\nAI MEDICAL DIAGNOSIS", BOLD + BLUE))
    print(c("Rule‑based symptom checker\n", DIM + CYAN))


def diagnose(symptoms: List[str]):
    sset = {s.strip().lower().replace(" ", "_") for s in symptoms if s.strip()}
    if not sset:
        print(c("No symptoms entered.", YELLOW))
        return

    scores = [(len(sset & rules), dis) for dis, rules in DISEASE_RULES.items() if len(sset & rules) > 0]
    if not scores:
        print(c("No matching disease found.", RED))
        return

    top = sorted(scores, reverse=True)[:3]
    print(c("\nLikely diagnoses:", BOLD + MAGENTA))
    print(c("────────────────────────────────", DIM))
    for matches, disease in top:
        spec = DISEASE_TO_SPECIALIST.get(disease, "Consult specialist")
        disease_str = f"{disease.title():<20}"
        print(f"{c(disease_str, GREEN)} ({matches} match)  →  {spec}")

def interactive():
    banner()
    print(c("Enter symptoms separated by commas (type 'exit' to quit).\n", CYAN))
    while True:
        try:
            inp = input(c("Symptoms> ", BLUE))
        except EOFError:
            break
        if inp.lower() in {"exit", "quit", "q"}:
            break
        diagnose(inp.split(','))
    print(c("Goodbye!", DIM))


def demo():
    banner()
    tests = [
        ["fever", "cough"],
        ["headache", "blurred vision"],
        ["shortness breath", "wheezing"],
        ["abdominal pain", "vomiting"],
        ["loss_interest", "fatigue"],
        ["chronic cough", "weight loss"],
        ["red eyes", "itchy eyes"],
    ]
    for t in tests:
        print(c(f"\nDemo: {', '.join(t)}", BOLD))
        diagnose(t)

def main():
    print(c("Available symptoms:", BOLD + CYAN))
    print(", ".join(ALL_SYMPTOMS))
    if sys.stdin.isatty():
        interactive()
    else:
        demo()
    print("⚠️  This is an AI-based suggestion only.")
    print("📞 Please consult a certified doctor in real life.")
    print("🙏 Thank you for using the system. Stay healthy!\n")



if __name__ == "__main__":
    main()
