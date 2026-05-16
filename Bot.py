import requests
import time
import random

# ================= CONFIG =================
BOT_TOKEN = "8466023093:AAGWaCQyzbhbZpdNzYmAr1HQtQEbohxI5JE"
# ==========================================

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0
active_questions = {}

# ================= QUESTION BANK =================
STATIC_BANK = [
    (
        "She ___ a teacher.",
        ["A am", "B is", "C are", "D be"],
        "B",
        "Use 'is' for singular third person (she/he/it)."
    ),

    (
        "They ___ in the park.",
        ["A am", "B is", "C are", "D be"],
        "C",
        "'Are' is used for plural subjects."
    ),

    (
        "I ___ happy today.",
        ["A am", "B is", "C are", "D be"],
        "A",
        "'Am' is only used with 'I'."
    ),

    (
        "He ___ to school every day.",
        ["A go", "B goes", "C going", "D gone"],
        "B",
        "For he/she/it in present simple, add s/es."
    ),

    (
        "Look! It ___ outside.",
        ["A rain", "B rains", "C raining", "D is raining"],
        "D",
        "Present continuous = am/is/are + verb-ing."
    ),

    (
        "She ___ a letter yesterday.",
        ["A write", "B wrote", "C written", "D writing"],
        "B",
        "Past simple of 'write' is 'wrote'."
    ),

    (
        "The cat is ___ the table.",
        ["A in", "B on", "C at", "D under"],
        "D",
        "'Under' means directly below."
    ),

    (
        "Happy most nearly means ___?",
        ["A sad", "B angry", "C joyful", "D tired"],
        "C",
        "'Joyful' means happy."
    ),
     # Verb to be
    ("She ___ a teacher.", ["A am", "B is", "C are", "D be"], "B",
     "Use 'is' for singular third person (she/he/it)."),
    ("They ___ in the park.", ["A am", "B is", "C are", "D be"], "C",
     "'Are' for plural subjects."),
    ("I ___ happy today.", ["A am", "B is", "C are", "D be"], "A",
     "'Am' only with 'I'."),
    # Present simple
    ("He ___ to school every day.", ["A go", "B goes", "C going", "D gone"], "B",
     "he/she/it + verb + s/es in present simple."),
    ("We ___ breakfast at 7 AM.", ["A eat", "B eats", "C eating", "D ate"], "A",
     "Plural subject uses base verb."),
    ("My sister ___ in a hospital.", ["A work", "B works", "C working", "D worked"], "B",
     "Third person singular → works."),
    ("They ___ television every evening.", ["A watch", "B watches", "C watching", "D watched"], "A",
     "Plural subject → base verb."),
    ("The sun ___ in the east.", ["A rise", "B rises", "C rising", "D rose"], "B",
     "General truth, third person singular → rises."),
    ("I ___ like coffee.", ["A don't", "B doesn't", "C not", "D am not"], "A",
     "Negative with 'I' uses don't."),
    ("She ___ have a car.", ["A don't", "B doesn't", "C not", "D isn't"], "B",
     "Third person negative → doesn't."),
    # Present continuous
    ("Look! It ___ outside.", ["A rain", "B rains", "C raining", "D is raining"], "D",
     "Present continuous: am/is/are + verb-ing."),
    ("We ___ our homework now.", ["A do", "B doing", "C are doing", "D does"], "C",
     "We + are + verb-ing."),
    ("I ___ a book at the moment.", ["A read", "B am reading", "C reading", "D reads"], "B",
     "I + am + verb-ing."),
    ("She ___ to music right now.", ["A listens", "B is listening", "C listened", "D listen"], "B",
     "Right now → present continuous."),
    # Past simple
    ("She ___ a letter yesterday.", ["A write", "B wrote", "C written", "D writing"], "B",
     "Past simple of 'write' is 'wrote'."),
    ("They ___ football last weekend.", ["A play", "B plays", "C played", "D playing"], "C",
     "Regular past simple → play + ed."),
    ("I ___ my keys this morning.", ["A lose", "B lost", "C losing", "D loses"], "B",
     "Past simple of 'lose' is 'lost'."),

("He ___ to Paris last year.", ["A go", "B goes", "C went", "D gone"], "C",
     "Past simple of 'go' → went."),
    ("We ___ a movie last night.", ["A see", "B saw", "C seen", "D seeing"], "B",
     "Past simple of 'see' → saw."),
    # Future tense
    ("I ___ visit my grandma tomorrow.", ["A will", "B am", "C do", "D have"], "A",
     "Future: will + base verb."),
    ("She ___ call you later.", ["A will", "B is", "C does", "D has"], "A",
     "Future with will."),
    ("They ___ arrive at 5 PM.", ["A will", "B are", "C do", "D have"], "A",
     "Will for future."),
    # Prepositions
    ("The cat is ___ the table.", ["A in", "B on", "C at", "D under"], "D",
     "Under = directly below."),
    ("We arrived ___ the station late.", ["A in", "B on", "C at", "D by"], "C",
     "Arrive at a place."),
    ("She is interested ___ music.", ["A on", "B in", "C at", "D with"], "B",
     "Interested in."),
    ("He is good ___ mathematics.", ["A at", "B in", "C on", "D with"], "A",
     "Good at."),
    ("I'm afraid ___ snakes.", ["A from", "B of", "C with", "D by"], "B",
     "Afraid of."),
    ("We went there ___ bus.", ["A by", "B on", "C in", "D with"], "A",
     "By bus (transport)."),
    # Articles

("She wants ___ apple.", ["A a", "B an", "C the", "D no article"], "B",
     "An before vowel sound."),
    ("___ sun rises in the east.", ["A A", "B An", "C The", "D No article"], "C",
     "The for unique things."),
    ("He is ___ best student in class.", ["A a", "B an", "C the", "D no article"], "C",
     "Superlative uses 'the'."),
    ("I have _ dog and _ cat.", ["A a, a", "B a, an", "C an, a", "D the, the"], "A",
     "A before consonant sounds."),
    ("She is ___ honest person.", ["A a", "B an", "C the", "D no article"], "B",
     "Honest starts with a vowel sound → an."),
    # Pronouns
    ("This is ___ book.", ["A I", "B me", "C my", "D mine"], "C",
     "My is a possessive adjective."),
    ("Give it to ___.", ["A I", "B me", "C my", "D mine"], "B",
     "Me is object pronoun."),
    ("___ are going to the park.", ["A He", "B Him", "C His", "D She"], "A",
     "He is subject pronoun."),
    ("The bag is ___.", ["A my", "B mine", "C me", "D I"], "B",
     "Mine is possessive pronoun."),
    ("We enjoyed ___ at the party.", ["A ourselves", "B us", "C our", "D we"], "A",
     "Reflexive pronoun ourselves."),
    # Comparatives / superlatives
    ("She is the ___ girl in the class.", ["A tall", "B taller", "C tallest", "D most tall"], "C",
     "Superlative: the + adjective + est."),
    ("This test is ___ than the last one.", ["A easy", "B easier", "C easiest", "D more easy"], "B",
     "Comparative: easy → easier."),
    ("My house is ___ than yours.", ["A big", "B bigger", "C biggest", "D more big"], "B",
     "Big → bigger."),
    ("She is the ___ beautiful in the family.", ["A more", "B most", "C much", "D very"], "B",
     "Long adjective → most beautiful."),
    ("He runs ___ than his brother.", ["A fast", "B faster", "C fastest", "D more fast"], "B",
     "Fast → faster."),
    # Vocabulary – synonyms
    ("Happy most nearly means ___?", ["A sad", "B angry", "C joyful", "D tired"], "C",
     "Joyful = happy."),
    ("Rapid means ___?", ["A slow", "B fast", "C heavy", "D light"], "B",
     "Rapid = fast."),
    ("Enormous means ___?", ["A tiny", "B huge", "C weak", "D thin"], "B",
     "Enormous = very big."),
    ("Commence means ___?", ["A stop", "B begin", "C finish", "D continue"], "B",
     "Commence = start."),
    ("Assist means ___?", ["A help", "B hinder", "C ignore", "D leave"], "A",
     "Assist = help."),
    # Vocabulary – antonyms
    ("The opposite of 'big' is ___?", ["A large", "B huge", "C small", "D tall"], "C",
     "Antonym of big → small."),
    ("Choose the antonym of 'beautiful':", ["A pretty", "B ugly", "C nice", "D lovely"], "B",

"Ugly = opposite of beautiful."),
    ("Antonym of 'brave' is ___?", ["A courageous", "B cowardly", "C bold", "D fearless"], "B",
     "Cowardly = not brave."),
    ("Opposite of 'cheap' is ___?", ["A inexpensive", "B costly", "C reasonable", "D low"], "B",
     "Costly = expensive."),
    ("Antonym of 'early' is ___?", ["A soon", "B late", "C quick", "D first"], "B",
     "Late = opposite of early."),
    # Verb forms
    ("He enjoys ___ football.", ["A play", "B plays", "C playing", "D to play"], "C",
     "enjoy + gerund (playing)."),
    ("She agreed ___ me.", ["A help", "B helping", "C to help", "D helps"], "C",
     "agree + to-infinitive."),
    ("I am looking forward to ___ you.", ["A see", "B seeing", "C seen", "D saw"], "B",
     "look forward to + gerund."),
    ("He stopped ___ because it was unhealthy.", ["A smoke", "B smoking", "C to smoke", "D smoked"], "B",
     "stop + gerund = quit an action."),
    ("She promised ___ on time.", ["A come", "B coming", "C to come", "D came"], "C",
     "promise + to-infinitive."),
    # Conditionals
    ("If it rains, we ___ at home.", ["A stay", "B will stay", "C stayed", "D staying"], "B",
     "First conditional: if + present, will + base."),

("If I ___ rich, I would travel the world.", ["A am", "B was", "C were", "D be"], "C",
     "Second conditional: if + past (were), would + base."),
    ("If she had studied, she ___ the exam.", ["A passed", "B would pass", "C would have passed", "D will pass"], "C",
     "Third conditional: if + past perfect, would have + past participle."),
    # Passive voice
    ("The book ___ by Mark Twain.", ["A wrote", "B was written", "C writes", "D writing"], "B",
     "Passive: be + past participle."),
    ("English ___ all over the world.", ["A speaks", "B is spoken", "C spoke", "D spoken"], "B",
     "Passive voice."),
    # Question tags
    ("You are coming, ___ you?", ["A are", "B aren't", "C do", "D don't"], "B",
     "Positive statement → negative tag."),
    ("She doesn't like coffee, ___ she?", ["A does", "B doesn't", "C is", "D isn't"], "A",
     "Negative statement → positive tag."),
    # Quantifiers
    ("There are ___ apples in the basket.", ["A a little", "B much", "C a few", "D any"], "C",
     "a few + countable plural."),
    ("I have ___ money left.", ["A a few", "B many", "C a little", "D few"], "C",
     "a little + uncountable."),
    ("How ___ students are there?", ["A much", "B many", "C a lot", "D little"], "B",
     "How many + countable."),
    # Conjunctions
    ("I wanted to go, ___ I was too tired.", ["A so", "B because", "C but", "D and"], "C",
     "But shows contrast."),
    ("She passed the exam ___ she studied hard.", ["A because", "B so", "C although", "D yet"], "A",
     "Because gives reason."),
    ("___ it was raining, we went out.", ["A Because", "B Although", "C So", "D Since"], "B",
     "Although shows contrast."),
    # Reported speech
    ("He said, 'I am happy.' → He said that he ___ happy.", ["A is", "B was", "C were", "D has been"], "B",
     "Reported speech: present → past."),
    ("She said, 'I will call you.' → She said she ___ call me.", ["A will", "B would", "C shall", "D can"], "B",
     "will → would."),
    # Modals
    ("You ___ smoke here. It's forbidden.", ["A can", "B must", "C mustn't", "D should"], "C",
     "mustn't = prohibition."),
    ("She ___ speak three languages.", ["A can", "B must", "C should", "D may"], "A",
     "can for ability."),
    ("You ___ see a doctor. You look ill.", ["A can", "B must", "C should", "D might"], "C",
     "should for advice."),
    # Miscellaneous
    ("There is ___ milk in the fridge.", ["A a", "B some", "C any", "D many"], "B",
     "some with uncountable in positive sentences."),
    ("We don't have ___ bread.", ["A some", "B any", "C a", "D little"], "B",

"any in negative sentences."),
    ("He is taller ___ his brother.", ["A as", "B than", "C then", "D that"], "B",
     "Comparative uses than."),
    ("She works as ___ teacher.", ["A a", "B an", "C the", "D no article"], "A",
     "as + a/an + job."),
    ("Let's go, ___ we?", ["A will", "B shall", "C do", "D don't"], "B",
     "Let's → shall we?"),
    ("I've been here ___ two hours.", ["A since", "B for", "C during", "D from"], "B",
     "for + duration."),
    ("She's lived here ___ 2010.", ["A since", "B for", "C from", "D in"], "A",
     "since + starting point."),
    ("This is the house ___ I grew up.", ["A which", "B where", "C who", "D when"], "B",
     "where for place."),
    ("The man ___ car was stolen is sad.", ["A who", "B which", "C whose", "D whom"], "C",
     "whose = possession."),
    ("I don't know ___ she is coming.", ["A if", "B that", "C which", "D what"], "A",
     "if/whether for indirect yes/no questions."),
    ("He is not only smart ___ also kind.", ["A and", "B but", "C so", "D or"], "B",
     "not only ... but also."),
    ("Either you ___ he is right.", ["A nor", "B or", "C and", "D but"], "B",
     "either ... or."),
    ("Neither the teacher ___ the students were in class.", ["A or", "B nor", "C and", "D but"], "B",

"neither ... nor."),
    ("I wish I ___ a bird.", ["A am", "B was", "C were", "D be"], "C",
     "wish + past subjunctive (were)."),
    ("It's time you ___ to bed.", ["A go", "B went", "C going", "D gone"], "B",
     "It's time + subject + past simple."),
    ("Hardly had we arrived ___ it started to rain.", ["A than", "B when", "C then", "D that"], "B",
     "Hardly ... when."),
    ("No sooner had he left ___ the phone rang.", ["A when", "B than", "C then", "D that"], "B",
     "No sooner ... than."),
    ("She is so kind ___ everyone likes her.", ["A that", "B as", "C than", "D so"], "A",
     "so ... that."),
    ("He ran fast ___ he could win.", ["A so that", "B such that", "C that", "D to"], "A",
     "so that = purpose."),
    ("I'd rather ___ at home tonight.", ["A stay", "B to stay", "C staying", "D stayed"], "A",
     "would rather + base verb."),
    ("You'd better ___ now.", ["A leave", "B to leave", "C leaving", "D left"], "A",
     "had better + base verb."),
    ("The more you practice, ___ you become.", ["A the best", "B the better", "C better", "D good"], "B",
     "the more ... the better.")

]

# ================= TELEGRAM FUNCTIONS =================

def send_message(chat_id, text, reply_markup=None):

    payload = {
    "chat_id": chat_id,
    "text": text
}

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(
            BASE_URL + "/sendMessage",
            json=payload,
            timeout=10
        )

        data = response.json()

        if data.get("ok"):
            return data["result"]["message_id"]

        else:
            print("Send Error:", data)

    except Exception as e:
        print("Send Exception:", e)

    return None


def edit_message(chat_id, message_id, text, reply_markup=None):

    payload = {
    "chat_id": chat_id,
    "message_id": message_id,
    "text": text
}

    if reply_markup is not None:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(
            BASE_URL + "/editMessageText",
            json=payload,
            timeout=10
        )

        data = response.json()

        if not data.get("ok"):
            print("Edit Error:", data)

    except Exception as e:
        print("Edit Exception:", e)


def answer_callback(callback_id):

    try:
        requests.post(
            BASE_URL + "/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=10
        )

    except Exception as e:
        print("Callback Error:", e)


def get_updates():

    global last_update_id

    try:
        response = requests.get(
            BASE_URL + f"/getUpdates?offset={last_update_id + 1}",
            timeout=20
        )

        data = response.json()

if not data.get("ok"):
            print("API ERROR:", data)
            return []

        return data.get("result", [])

    except Exception as e:
        print("Network Error:", e)
        return []


# ================= BUTTONS =================

def build_options_keyboard(options):

    """
    Shows full option text on buttons.

    Example:
    A am
    B is
    C are
    D be

    But callback data remains:
    A / B / C / D
    """

    buttons = []

    for opt in options:

        letter = opt[0]

        buttons.append({
            "text": opt,
            "callback_data": letter
        })

    keyboard = [
        buttons[:2],
        buttons[2:]
    ]

    return {
        "inline_keyboard": keyboard
    }


def build_new_question_keyboard():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "🔄 New Question",
                    "callback_data": "/practice"
                }
            ]
        ]
    }


# ================= BOT START =================

print("Bot is running...")

while True:

    updates = get_updates()

    for update in updates:

        last_update_id = update["update_id"]

        # ================= NORMAL MESSAGE =================

        message = update.get("message")

        if message:

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            print(f"Message from {chat_id}: {text}")

            # ---------- /start ----------
            if text == "/start":

                send_message(
                    chat_id,
                    "👋 Welcome!\n\nUse /practice to start the quiz."
                )

            # ---------- /practice ----------
            elif text == "/practice":

                q, opts, correct, explanation = random.choice(STATIC_BANK)

                keyboard = build_options_keyboard(opts)

                message_id = send_message(
                    chat_id,
                    q,
                    reply_markup=keyboard
                )

                if message_id:

                    active_questions[(chat_id, message_id)] = {
                        "correct": correct,
                        "explanation": explanation
                    }

            # ---------- OTHER MESSAGE ----------
            else:

                send_message(
                    chat_id,
                    "Use /practice to start the quiz."
                )

        # ================= CALLBACK QUERY =================

        callback = update.get("callback_query")

        if callback:

            callback_id = callback["id"]
            user_choice = callback["data"]

            message = callback["message"]

            chat_id = message["chat"]["id"]
            message_id = message["message_id"]

            answer_callback(callback_id)

            # ---------- NEW QUESTION BUTTON ----------
            if user_choice == "/practice":

                q, opts, correct, explanation = random.choice(STATIC_BANK)

                keyboard = build_options_keyboard(opts)

                edit_message(
                    chat_id,
                    message_id,
                    q,
                    reply_markup=keyboard
                )

                active_questions[(chat_id, message_id)] = {
                    "correct": correct,
                    "explanation": explanation
                }

                continue

            # ---------- CHECK ANSWER ----------

            question_info = active_questions.pop(
                (chat_id, message_id),
                None
            )

            if not question_info:

                edit_message(
                    chat_id,
                    message_id,
                    "This question expired.\nUse /practice for a new question."
                )

                continue

            correct_letter = question_info["correct"]
            explanation = question_info["explanation"]

            # ---------- RESULT ----------
            if user_choice == correct_letter:

result = f"✅ Correct!\n\nAnswer: {correct_letter}"

            else:

                result = (
                    f"❌ Wrong!\n\n"
                    f"Your answer: {user_choice}\n"
                    f"Correct answer: {correct_letter}"
                )

            original_question = message.get("text", "")
