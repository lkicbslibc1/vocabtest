from flask import Flask, request, abort, jsonify, session
import json
import requests
import random
from project.Config import Channel_access_token

app = Flask(__name__)

vocab = {
    "consider": "deem to be", 
    "concern" : "something that interests you because it is important",
    "intend": "have in mind as a purpose",
    "minute": "infinitely or immeasurably small",
    "commit": "perform an act, usually with a negative connotation",
    "issue": "some situation or event that is thought about",
    "accord": "concurrence of opinion",
    "approach": "move towards",
    "establish": "set up or found",
    "evident": "clearly revealed to the mind or the senses or judgment",
    "constitute": "to make up or form something",
    "attribute": "a quality or characteristic of someone or something",
    "evaluate": "to assess or judge the value or quality of something",
    "comprehend": "to understand or grasp the meaning of something",
    "illustrate": "to provide examples or clarify with visuals",
    "perceive": "to become aware of or notice through the senses",
    "emphasize": "to give special importance or attention to something",
    "interpret": "to explain or understand the meaning of something",
    "analyze": "to examine in detail for a better understanding",
    "determine": "to decide or ascertain a fact or outcome",
    "resemble": "to be similar or have a likeness to",
    "implement": "to put into action or use",
    "sustain": "to support or maintain",
    "contemplate": "to think deeply or consider",
    "synthesize": "to combine various elements to form a whole",
    "perpetuate": "to make something continue indefinitely",
    "deduce": "to infer or derive as a conclusion from facts or premises",
    "advocate": "to support or recommend a particular cause or policy",
    "elaborate": "involving many careful details; thorough and exhaustive",
    "ascertain": "to find out for certain; make sure of",
    "interpretation": "an explanation or way of explaining",
    "discern": "to perceive or recognize something",
    "pertain": "to be relevant to or connected with",
    "scrutinize": "to examine or inspect closely and thoroughly",
    "elucidate": "to make something clear and understandable",
    "annotate": "to add explanatory notes to a text or diagram",
    "expound": "to present and explain a theory or idea in detail",
    "inquire": "to ask for information or seek an answer",
    "derive": "to obtain something from a source or origin",
    "validate": "to confirm the accuracy or soundness of something",
    "postulate": "to suggest or assume the existence or truth of something",
    "explore": "to investigate or travel through in order to learn more",
    "corroborate": "to confirm or support with evidence or authority",
    "refute": "to prove something to be false or incorrect",
    "critique": "a detailed analysis and assessment of something",
    "emulate": "to imitate or match the achievement of another",
    "propagate": "to spread or promote widely",
    "deduct": "to subtract or take away from a total",
    "instigate": "to initiate or provoke something, often negative",
    "assess": "to evaluate or estimate the nature, ability, or quality of",
    "integrate": "to combine or coordinate different elements into a unified whole",
    "extrapolate": "to extend or project known information or data into an unknown area",
    "mitigate": "to make less severe or painful",
    "decipher": "to convert code or symbols into ordinary language",
    "proclaim": "to announce or declare publicly or officially",
    "dedicate": "to devote time, effort, or resources to a particular task or purpose",
    "construe": "to interpret or understand the meaning of something",
    "speculate": "to form a theory or conjecture without firm evidence",
    "authenticate": "to prove the genuineness or validity of something",
    "enumerate": "to list or mention a number of items one by one",
    "ratify": "to give formal approval or consent to an agreement, decision, or action","Hypothesize": "To propose a tentative explanation or theory based on limited evidence.",
    "Depict": "To represent or show something in a picture, story, or other form.",
    "Convey": "To communicate or express a message or feeling.",
    "Exemplify": "To serve as a typical example of something.",
    "Persevere": "To continue with an effort, despite obstacles or challenges.",
    "Fabricate": "To invent or create something, typically with deceitful intent.",
    "Elude": "To escape or avoid something, typically by being elusive or tricky.",
    "Repudiate": "To reject, deny, or disown something or someone.",
    "Cognizant": "To be aware or informed about something.",
    "Prudent": "Showing good judgment and careful thought.",
    "Alleviate": "To make a problem or suffering less severe.",
    "Inquire": "To seek information or ask for details.",
    "Mitigate": "To make less severe, harsh, or painful.",
    "Elicit": "To draw out or evoke a response, answer, or reaction.",
    "Meticulous": "Showing great attention to detail and precision.",
    "Unveil": "To reveal or disclose something that was previously hidden.",
    "Delineate": "To describe or outline something precisely.",
    "Concur": "To agree or be of the same opinion.",
    "Relinquish": "To give up or let go of something, typically a responsibility.",
    "Pragmatic": "Dealing with things sensibly and realistically.",
    "Scrutinize": "To examine or inspect closely and thoroughly.",
    "Expedite": "To make a process or action happen more quickly.",
    "Bolster": "To support or strengthen something.",
    "Corroborate": "To confirm or support with evidence or authority.",
    "Endorse": "To approve, support, or give one's public approval.",
    "Fathom": "To understand or comprehend a complex issue or idea.",
    "Reiterate": "To say or do something again, often for emphasis or clarity.",
    "Diminish": "To make or become less or smaller in size, degree, or importance.",
    "Culminate": "To reach the highest or climactic point.",
    "Negate": "To nullify or deny the truth or existence of something.",
    "Exacerbate": "To make a problem or situation worse.",
    "Illuminate": "To light up or provide clarity on a subject or topic.",
    "Resilient": "Capable of withstanding adversity and quickly recovering from difficulties.",
    "Vindicate": "To clear from blame or suspicion, typically after evidence or proof.","Austere": "Severe or strict in manner, attitude, or appearance.",
    "Benevolence": "The quality of being well-meaning, kindness, and goodwill.",
    "Cacophony": "A harsh, discordant mixture of sounds.",
    "Debilitate": "To make someone weak and infirm; to impair the strength of.",
    "Equivocate": "To use ambiguous language to conceal the truth or avoid making a direct statement.",
    "Facetious": "Treating serious issues with inappropriate humor; flippant.",
    "Garrulous": "Excessively talkative, especially on trivial matters.",
    "Hapless": "Unfortunate or unlucky; marked by a lack of success.",
    "Ineffable": "Too great or extreme to be expressed or described in words.",
    "Juxtapose": "To place or deal with close together for contrasting effect.",
    "Kaleidoscope": "A constantly changing pattern or sequence of elements.",
    "Lethargic": "Affected by a great lack of energy; sluggish and apathetic.",
    "Mellifluous": "Sweetly or smoothly flowing; pleasing to the ear.",
    "Nefarious": "Wicked, villainous, or heinously infamous.",
    "Obfuscate": "To render obscure, unclear, or unintelligible; to bewilder.",
    "Pernicious": "Having a harmful effect, especially in a gradual or subtle way.",
    "Quixotic": "Exceedingly idealistic; unrealistic and impractical.",
    "Recalcitrant": "Having an obstinately uncooperative attitude toward authority or discipline.",
    "Sycophant": "A person who acts obsequiously towards someone important in order to gain advantage.",
    "Taciturn": "Reserved or uncommunicative in speech; saying little.",
    "Ubiquitous": "Present, appearing, or found everywhere.",
    "Voracious": "Wanting or devouring great quantities of food; having a very eager approach to an activity.",
    "Wily": "Skilled at gaining an advantage, especially through deceit or cleverness.",
    "Xenophobia": "Dislike or prejudice against people from other countries.",
    "Yielding": "Compliant or giving in to a request or demand; allowing someone to have their way.",
    "Zealot": "A person who is fanatical and uncompromising in pursuit of their religious, political, or other ideals.",
}

example = {
    "consider": "She refused to consider my request.",
    "concern": "This issue is of great concern to our community.",
    "intend": "I intend to pursue a career in medicine.",
    "minute": "The details are so minute that they can easily be overlooked.",
    "commit": "He committed a serious crime and faced legal consequences.",
    "issue": "The latest issue of the journal is now available.",
    "accord": "There is a general accord among the members regarding the new policy.",
    "approach": "We need to carefully consider our approach to solving this problem.",
    "establish": "The company plans to establish a new branch in the city.",
    "evident": "The impact of climate change is evident in the increasing temperatures.",
    "constitute": "These small towns constitute the greater metropolitan area.",
    "attribute": "Her leadership skills are a remarkable attribute.",
    "evaluate": "The professor will evaluate the students' research projects.",
    "comprehend": "It may take some time to fully comprehend the complexity of this issue.",
    "illustrate": "He used charts and graphs to illustrate his findings.",
    "perceive": "Some people perceive this artwork as a symbol of hope.",
    "emphasize": "The speaker will emphasize the importance of education.",
    "interpret": "It is challenging to interpret this ancient text accurately.",
    "analyze": "Scientists analyze data to draw meaningful conclusions.",
    "determine": "The jury will determine the defendant's guilt or innocence.",
    "resemble": "The two siblings closely resemble each other.",
    "implement": "The government plans to implement new policies next year.",
    "sustain": "Efforts to sustain the local ecosystem are critical.",
    "contemplate": "She would often contemplate the mysteries of the universe.",
    "synthesize": "Scientists aim to synthesize a new, more efficient material.",
    "perpetuate": "His generous donation will help perpetuate the arts in our community.",
    "deduce": "From the evidence presented, we can deduce that he was not at the scene of the crime.",
    "advocate": "She passionately advocates for equal rights for all citizens.",
    "elaborate": "The research paper provides an elaborate analysis of the topic.",
    "ascertain": "The investigation aims to ascertain the truth of the matter.",
    "interpretation": "Different scholars may offer varying interpretations of this historical event.",
    "discern": "It is difficult to discern the truth amidst all the rumors.",
    "pertain": "The rules and regulations pertain to all employees.",
    "scrutinize": "The committee will scrutinize the proposed budget carefully.",
    "elucidate": "The professor will elucidate the key concepts in the lecture.",
    "annotate": "Students are encouraged to annotate the assigned texts.",
    "expound": "The expert will expound on the implications of the research findings.",
    "inquire": "Feel free to inquire if you have any questions about the project.",
    "derive": "The company will derive significant benefits from this partnership.",
    "validate": "Extensive testing is required to validate the safety of this product.",
    "postulate": "The scientist will postulate a new theory based on the experimental results.",
    "explore": "Researchers continue to explore the mysteries of the ocean.",
    "corroborate": "We need more evidence to corroborate this theory.",
    "refute": "The speaker will refute the opposing arguments in the debate.",
    "critique": "She received a critique of her artwork from a renowned art critic.",
    "emulate": "Aspiring writers often seek to emulate the styles of their favorite authors.",
    "propagate": "The organization's mission is to propagate awareness of environmental issues.",
    "deduct": "You can deduct the cost of business expenses from your taxes.",
    "instigate": "His inflammatory remarks can instigate unrest among the crowd.",
    "assess": "The teacher will assess the students' performance throughout the semester.",
    "integrate": "The software is designed to integrate seamlessly with other applications.",
    "extrapolate": "Economists often extrapolate future trends based on historical data.",
    "mitigate": "Efforts are in place to mitigate the effects of climate change.",
    "decipher": "Archaeologists work diligently to decipher ancient inscriptions.",
    "proclaim": "The president will proclaim a new national holiday.",
    "dedicate": "He chose to dedicate his life to helping those in need.",
    "construe": "The court will construe the language of the contract to determine its validity.",
    "speculate": "Economists speculate about the potential impacts of new trade policies.",
    "authenticate": "The expert will authenticate the historical documents.",
    "enumerate": "She will enumerate the key points in her presentation.",
    "ratify": "The United Nations will ratify the international treaty to promote peace.",
    "Hypothesize": "Scientists hypothesize that a cure for the disease may be found in the near future.",
    "Depict": "The painting beautifully depicts a serene countryside scene.",
    "Convey": "Effective communication skills are essential to convey ideas clearly.",    "Exemplify": "This success story exemplifies the principles of hard work and determination.",
    "Persevere": "Despite facing numerous challenges, she continued to persevere and achieved her goals.",
    "Fabricate": "The journalist was found to fabricate stories for sensationalism.",
    "Elude": "The criminal managed to elude the police for weeks.",
    "Repudiate": "He had to repudiate the rumors and set the record straight.",
    "Cognizant": "They were cognizant of the potential risks involved in the project.",
    "Prudent": "Making prudent financial decisions is essential for a secure future.",
    "Alleviate": "The medicine helped alleviate her pain and discomfort.",
    "Inquire": "Feel free to inquire if you have any questions about the project.",
    "Mitigate": "Efforts to mitigate the impact of the natural disaster were successful.",
    "Elicit": "The teacher used thought-provoking questions to elicit insightful responses from the students.",
    "Meticulous": "The artist's meticulous attention to detail is evident in every brushstroke.",
    "Unveil": "The company will unveil its latest product at the upcoming conference.",
    "Delineate": "He used a marker to delineate the boundaries of the property.",
    "Concur": "The team members concurred on the best approach to the problem.",
    "Relinquish": "She decided to relinquish her role as the team captain.",
    "Pragmatic": "In challenging situations, taking a pragmatic approach is often the best course of action.",
    "Scrutinize": "Auditors will scrutinize the company's financial records.",
    "Expedite": "The new software is designed to expedite the document review process.",
    "Bolster": "The support of her friends and family helped bolster her confidence.",
    "Corroborate": "Multiple witnesses corroborated the victim's account of the incident.",
    "Endorse": "The celebrity's endorsement of the product led to increased sales.",
    "Fathom": "The complexity of the legal case was difficult to fathom.",
    "Reiterate": "I would like to reiterate the importance of punctuality in our workplace.",
    "Diminish": "Over time, the impact of the economic crisis began to diminish.",
    "Culminate": "The awards ceremony will culminate in the presentation of the Lifetime Achievement Award.",
    "Negate": "Her apology was sincere and served to negate any ill feelings.",
    "Exacerbate": "The lack of rain will exacerbate the drought conditions in the region.",
    "Illuminate": "The scientific discovery will illuminate our understanding of the universe.",
    "Resilient": "Despite the setbacks, the community proved to be resilient and quickly recovered.",
    "Vindicate": "The newly discovered evidence will vindicate the wrongfully accused person.",
    "Austere": "The austere design of the building reflects the architect's minimalist style.",
    "Benevolence": "His benevolence extended to all, as he donated generously to various charities.",
    "Cacophony": "The city streets were filled with the cacophony of honking horns and chatter.",
    "Debilitate": "The illness left him debilitated and unable to carry out his daily activities.",
    "Equivocate": "She would often equivocate when asked direct questions about her actions.",
    "Facetious": "His facetious remarks lightened the mood during the tense meeting.",
    "Garrulous": "The garrulous neighbor would talk for hours about various topics.",
    "Hapless": "Despite his efforts, he remained a hapless victim of unfortunate circumstances.",
    "Ineffable": "The beauty of the natural landscape was ineffable, beyond words.",
    "Juxtapose": "The artist chose to juxtapose light and dark elements in the painting.",
    "Kaleidoscope": "The vibrant market was a kaleidoscope of colors, sounds, and flavors.",
    "Lethargic": "The heat made everyone feel lethargic and less energetic.",
    "Mellifluous": "The singer's mellifluous voice captured the hearts of the audience.",
    "Nefarious": "The nefarious activities of the criminal organization were finally exposed.",
    "Obfuscate": "His attempts to obfuscate the truth only made the situation more complicated.",
    "Pernicious": "The pernicious effects of the addiction took a toll on his health.",
    "Quixotic": "His quixotic dreams of world peace were considered unrealistic by many.",
    "Recalcitrant": "The recalcitrant student refused to follow the classroom rules.",
    "Sycophant": "He was known to be a sycophant who constantly sought the boss's approval.",
    "Taciturn": "His taciturn nature made it difficult to know what he was thinking.",
    "Ubiquitous": "In the modern world, smartphones have become ubiquitous.",
    "Voracious": "She had a voracious appetite for knowledge and constantly sought to learn.",
    "Wily": "The wily fox used its cunning to outsmart the hunters.",
    "Xenophobia": "Xenophobia can lead to discrimination against people from other countries.",
    "Yielding": "She was known for her yielding nature, always putting others' needs before her own.",
    "Zealot": "He was a religious zealot who was devoted to his faith."
}


quiz_in_progress = False
current_question = ""
correct_answer = ""

def quiz(vocab):
    word = random.choice(list(vocab.keys()))
    correct_meaning = vocab[word]
    options = [correct_meaning] + random.sample(list(vocab.values()), 3)
    random.shuffle(options)

    question = "What is the meaning of '{}'?\n".format(word)
    for i, option in enumerate(options, start=1):
        question += "{}. {}\n".format(chr(96 + i), option)

    correct_answer = chr(96 + options.index(correct_meaning) + 1)
    return question, correct_answer, word

def start_quiz():
    global current_question, correct_answer, quiz_in_progress
    quiz_in_progress = True
    current_question, correct_answer, word = quiz(vocab)

@app.route('/')
def hello():
    return 'Hello, World!', 200

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        global quiz_in_progress, current_question, correct_answer, word
        LongMessage = request.json
        events = LongMessage.get('events', [])

        if not events:
            return jsonify({})

        Reply_token = events[0]['replyToken']
        message = events[0]['message']

        if message['type'] != 'text':
            return jsonify({})

        message_text = message['text']

        if quiz_in_progress:
            user_answer = message_text.lower()
            correct_answer = correct_answer.lower()
            example_sentence = example[word]
            if user_answer == correct_answer:
                ReplyMessage(Reply_token, f"ปิ๊งป่องง ถูกครับ\nตัวอย่างประโยค: {example_sentence}", Channel_access_token)
            else:
                ReplyMessage(Reply_token, f"ว้าา คำตอบที่ถูกต้องคือ '{correct_answer}' ครับ\nตัวอย่างประโยค: {example_sentence}", Channel_access_token)
            quiz_in_progress = False
            return jsonify({"status": "success"})

        start_quiz()
        question, correct_answer, word = quiz(vocab)
        ReplyMessage(Reply_token, question, Channel_access_token)
        return jsonify({"status": "success"})
    
    elif request.method == 'GET':
        return 'This is method GET!!', 200
    else:
        abort(400)

def ReplyMessage(Reply_token, Text_Message, Channel_access_token):
    LINE_API = "https://api.line.me/v2/bot/message/reply"
    Authorization = "Bearer {}".format(Channel_access_token)
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": Authorization
    }
    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "text",
            "text": Text_Message
        }]
    }

    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200