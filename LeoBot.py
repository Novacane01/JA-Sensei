# coding=utf-8
import sys
from random import randint
from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, PictureMessage, SuggestedResponseKeyboard, TextResponse, \
    StartChattingMessage, VideoMessage, IsTypingMessage, ScanDataMessage, StickerMessage, LinkMessage, \
    FriendPickerMessage
import requests
import json
from datetime import datetime
from pytz import timezone

kik = KikApi('jasensei', '1e02581f-bec7-461b-b64d-59aff09c4460')

# static_keyboard is the starting keyboard that will appear when they type the name of the bot
kik.set_configuration(Configuration(webhook='https://leobotkik.herokuapp.com/'))
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hmm():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)
    messages = messages_from_json(request.json["messages"])
    for message in messages:
        # with open("subscribers.txt", "r") as f:
        #     subscribers = f.read()
        # f.close()
        # if not (user_from in subscribers):
        #     with open("subscribers.txt", "a") as f:
        #         f.write(user_from)
        #     f.close()
        user = kik.get_user(message.from_user)
        user_from = message.from_user
        id_chat = message.chat_id
        if isinstance(message, (StartChattingMessage, ScanDataMessage)):
            msg_send(user_from, id_chat,
                     "Hi there! My name is Leo Sensei. I am here to assist with all your Japanese needs!"
                     "What can I help you with today?", ["Grammar", "Translations", "Examples", "Kana Charts", "Time", "Tips", "Facts", "Updates", "Exit"])
        elif isinstance(message, TextMessage):
            flow = ["Grammar", "Translations", "Examples", "Kana Charts", "Time", "Tips", "Facts", "Updates", "Exit"]
            greeting = ["hi","hello","hey","hola","yo","greetings"]
            mb = message.body.lower()
            if mb == "" and user_from == "bhoney_99":
                msg_send(user_from, id_chat, "Hi new here, I\'m new here")
            elif mb == "" or mb in greeting:
                msg_send(user_from, id_chat, "Hey {}! What can I help you with today?".format(user_from), flow)
            # elif mb.split()[0] in subscribers and user_from == "shadowblasts":
            #     kik.send_messages([TextMessage(
            #         to=mb.split()[0],
            #         body=mb.replace(mb.split()[0], "")
            #     )])
            elif mb == "updates":
                msg_send(user_from, id_chat, "Bug Fixes:\n-Fixed Leo Sensei's message spam\nPatch 1.5:\nAdded Intermediate Grammar Lessons\nPrevious Patches:\n"
            "-Can now translate from English to Japanese and vice versa!\n-Now able to send updates to subscribers\n-Increased number of tips given\n"
            "-Incorporated beginner level grammar lessons w/video\n-Hiragana Chart added\n-Katakana Chart added\nComing Soon:\n"
            "-Expert Grammar Lessons\n-Kana Learning Games\nWorking on a fix for certain people not being able to use Leo Bot")
            elif mb == "help":
                msg_send(user_from, id_chat, "What can I help you with today?", flow)
            elif mb == "particle":
                msg_send(user_from, id_chat, "Which particle would you like information on?", ["を(wo)","に(ni)","へ(he)","から(kara)/まで(made)","は(ha)","で(de)"])
            elif mb == "を(wo)" or mb == "particle wo" or mb == "particle を":
                msg_send(user_from,id_chat,"\'を\' is a \'対格\'. \'対\' meaning \'against\'.The way I remember \'を\' is, if YOU can do it then use \'を\'.\n"
        "\n\'べんとうを食べる\' - You can eat a bento.\n\n\'を\' usually comes before a verb. The \'を\' particle can't be "
        "used if the object isn't you or animate.\n\nボールを落とす - You drop the ball.\n"
        "\n\'ボールが落ちる\' - The ball falls.\n\n\'あのボールを落とす\' - I dropped that ball\n\n\'あのボールが落ちる\' - That ball dropped.\n"
        "\n\'キリンがボールを落とす\' - A giraffe dropped the ball\n\'キリン\' (giraffe).\n"
        "\nSee http://www.guidetojapanese.org/learn/grammar/verbparticles for more info",flow)
            elif mb == "に(ni)" or mb == "particle ni" or mb == "particle に":
                msg_send(user_from,id_chat,"\'に\' is \'処格/所格\'. \'所\' meaning place. As stated before you should think \'に\' as \'To\', but it can be \'At\' also.\n"
        "\n\'大阪に行く\'(\'I\' omitted) - I go to Osaka\n\n\'大阪に行った\' (this is in the past tense) - I went to Osaka.\n"
        "\n\'僕は大阪に着いた\' - I arrived at Osaka.\n\nThe only verbs that can used after \'に\' are verbs that are for travel\n"
        "\n\'大阪に歩く\' - I walk to Osaka (in this case it sounds unnatural because \'まで\' is more suitable for this.)\n"
        "\n\'に\' is used when there's destination. It can't be used for directions. "
        "\'東に行く\'<--- It would be correct if 東 was a destination, however, 東 is a direction. "
        "\'に\' is often placed between a destination and a verb such as \'行く\' (iku) which means go."
        "\nSee http://www.guidetojapanese.org/learn/grammar/verbparticles for more info",flow)
            elif mb == "へ(he)" or mb == "particle he" or mb == "particle へ":
                msg_send(user_from,id_chat,"\'へ\' is a \'方向格\'. \'方向\' means direction.\n"
        "\n\'へ\' has the same use as the second use of \n\'に\' (\'所格\' use of \'に\'), however instead of destinations, it\'s used for directions. "
        "\'へ\' can be \"to\" or \"towards\".\n\n\'僕は東へ歩く\' - I walk towards the east.\n\n\'右へ曲がる\' - Turn at the left.\n"
        "\n\'大阪に行く\' vs. \'大阪へ行く\'\nBoth are correct but there's a subtle difference:\n\n\'大阪に行く\' - Go to Osaka\n"
        "\n\'大阪へ行く\' - Go towards Osaka.\nBy using \'へ\' it doesn't necessarily mean that you're at Osaka, but "
        "you went in the general direction and you're around Osaka.\nFor vehicles such as trains and boats it gets a " 
        "little confusing.\n\n\'僕は電車で大阪へ行く\' - I go towards Osaka\n\'僕は電車で大阪駅に行く\' - I go to Osaka station" 
        "\n\n\'大阪駅\' is a specific destination, but in actuality both work and (especially when speaking). " 
        "Even if you switch them, it doesn't matter as much.\nSee http://www.guidetojapanese.org/learn/grammar/verbparticles for more info.",flow)
            elif mb == "から(kara)/まで(made)" or mb == "particle kara" or mb == "particle made" or mb == "particle まで" or mb == "particle から":
                msg_send(user_from,id_chat,"\'から\' is a \'出格\'. \'出る\' meaning \'exit\'. \'から\' is like \'from\'.\n\'まで\' is a \'到格\'. "
        "\'到\' meaning \'arrival\' or \'reach\'.\n\'まで\' is like until.\n\'から\' and \'まで\' are used as pairs, but there are some cases where you can "
        "omit \'まで\' or there are some cases don't need \'まで\'. Vice versa.\n\'大阪から東京まで何分ですか？\'"
        "\nHow many minutes is it from Osaka until Tokyo? For destinations you put it \'から\' and \'まで\' after "
        "the destinations.\n\n\'から\' and \'まで\' can also be used for numbers \'一から百億まで数えてください\'"
        "\nPlease count from one until 10000000000\n\n\'から\' and \'まで\' can be used for most things that can be measured."
        "\n\'あそこまで歩いてください\'\nPlease walk until there. \n\'ここから初めてください\'\nplease start here."
        "\'10まで数えます\'\nI'll count until 10\n\'0から数えてください\'\nPlease count from 0\n\'180cmまで伸びたら\'\nIf you grow until 180cm"
        "\nSee http://www.imabi.net/theparticlekara.htm for more info",flow)
            elif "で" in mb or "de" in mb:
                msg_send(user_from,id_chat,"\'で\' also has two uses. The first use is very similar to \'に\'. The first use of \'で\' is also a \'所格\'. "
        "Although \'で\' is similar to \'に\' it has a different use. \'で\' goes after a destination, however, you should only think of "
        "\'で\' as \'At\' \n\n\'大阪で会う\' (\'I\' omitted) - we met at Osaka \n\'大阪で見る\' - I saw at Osaka. \n\n\'大阪で行く\'<--- verbs "
        "that aren't for travel should go after \'で\'.\nThe second use of \'で\' is \'具格\'. \'で\' is like \'by\' or \'with\'\n\n\'車で行きます\'"
        "(\'I\' omitted) - I'll go by my car \n\'新幹線で大阪に行きます\' (\'へ\' is more suitable in this case but \'に\' also works) - "
        "Ill go to Osaka by bullet train. In this case a travel verb like 行く can be put after で.\n\nBefore で, a "
        "vehicle should be in front of \'で\'.\nAlso, with the \'具格\' use of \'で\', it can be used with tools. For example:"
        "\n\'ペンで書く\'(\'I\' omitted) - I write with a pen \'鎌で畑を刈る\' - I harvest the fields with a sickle.\n\nIf you "
        "imagine vehicles as tools then it will be easy to remember.\nSee http://www.guidetojapanese.org/learn/grammar/verbparticles for more info.",flow)
            elif mb == "は(ha)" or mb == "particle は" or mb == "particle ha":
                msg_send(user_from,id_chat,"\'は\' is similar to \'が\'. Both are \'主格\', \'主\' meaning \'master\' or \'subject\'.The only "
        "difference is that \'が\' is for a specific subject while \'は\' is for something general.\n\'は\' is used "
        "to indicate the topic of a sentence. The focus of the sentence is the statement behind the particle \'は\'.\n\n"
        "\'誰がやったの？\' - Who did it?\nWhy not \'は\'? You want a specific answer so it's \'が\' for this.\n\n"
        "Many foreigners make a mistake by putting \'は\' in:\n\'私はアメリカ人\' - I am an American\n\n\'私がアメリカ人\' - I am the American\n "
        "\'私はハンバーガーを食べた\' - I ate a hamburger\n\n\'私がハンバーガーを食べた\' - I ate a hamburger (with more emphasis on "
        "the \'I\' and \'Hamburger\')\n\'ハンバーガーが美味しかった\' - that hamburger was delicious (emphasis on \'That hamburger\')\n\'ハンバーガーは美味しい\' "
        "- hamburgers are delicious (just any hamburgers).\n\'は\' and \'が\' is like \'is\' and \'are\'. They have the same meaning and basically the same "
        "use but \'is\', is for one object, one specific object while \'are\' is used for multiple.\n"
        "See http://www.guidetojapanese.org/learn/grammar/particlesintro for more info",flow)
            # elif mb == "!translate":
            #     msg_send(user_from, id_chat, "Translation is currently being worked on. Sorry for any inconvenience!")
            # msg_send(user_from, id_chat, """To translate from Japanese to English, type in \"en\" followed by your text.
            # To translate from English to Japanese, type in \"ja\" followed by your text.""")
            # Code for giving examples
            elif mb == "examples":
                msg_send(user_from, id_chat, "Which example words would you like to review?", ["Animals", "Colors","Cancel"])
            elif mb == "colors":
                msg_send(user_from, id_chat, "明るい (あかるい) - light\n黒い (くろい) - black\n 茶色い (ちゃいろい) - brown\n白い (しろい) - white",flow)
            elif mb == "animals":
                msg_send(user_from, id_chat, "犬 (いぬ) - dog\n猫 (ねこ) - cat\n魚 (さかな) - fish",flow)
        #     elif mb == "disaster":
        #         msg_send(user_from,id_chat,"災害 (saigai) disasters\n地震 (jishin) earthquake \n津波 (tsunami) tsunami \n台風 (taifuu) typhoon\n"
        # "洪水 (kouzui) flooding \n土砂崩れ (doshakuzure) landslides\n噴火 (funka) eruptions\n火災 (kasai) fire\n旱魃 (kanbatsu) drought\n"
        # "大雨 (おおあめ) heavy rain\n洪水 (こうずい) flooding\n暴風 (ぼうふう) windstorm\n波浪 (はろう) violent waves")
        #     elif mb == "danger":
        #         msg_send(user_from,id_chat,"拉致 (rachi) abduction\n誘拐 (yuukai) kidnapping\n事件 (jiken) case, incident, crime")
        #     elif mb == "government":
        #         msg_send(user_from,id_chat,"政治 (せいじ) - politics\n政治家 (せいじか) - politician\n国政(こくせい) - state politics/ state government\n"
        # "地方自治(ちほうじち) - local autonomy\n政体(せいたい) - form of government\n政府(せいふ) - government/administration\n"
        # "地方自治体(ちほうじちたい) - local government/ local autonomy\n国(くに) - county \n国家(こっか) - state \n行政区分(ぎょうせいくぶん) - governmental division\n"
        # "国民(こくみん) - national citizens \n人民(じんみん) - people/public\n市民(しみん) - citizen\n国際法(こくさいほう) - international laws\n"
        # "国内法(こくないほう) - domestic laws\n憲法(けんぽう) - constitution\n条約(じょうやく) - a treaty\n法律(ほうりつ) - law")
            # elif mb == "more--":
            #     msg_send(user_from, id_chat, "政令(せいれい) - government ordinance\n省令(しょうれい) - ministerial ordinance\n"
            # "条例(じょうれい) - regulation, ordinance\n政治体制(せいじたいせい) - political system\n直接民主制 (ちょくせつみんしゅせい) - direct democracy\n"
            # "間接民主制 (かんせつみんしゅせい) - indirect democracy\n君主制 (くんしゅせい) - monarchy\n貴族制 (きぞくせい) - aristocracy\n"
            # "共和制 (きょうわせい) - republic\n僭主制 (せんしゅせい) - tyranny\n寡頭制 (かとうせい) - oligarchy\n民主主義 (みんしゅしゅぎ) - democracy\n"
            # "衆愚制 (しゅうぐせい) - ochlocracy ")
            #     x = 0
            # Gives Japanese studying tips
            elif mb == "translations":
                msg_send(user_from, id_chat, "To start translating, say \'Translate\' followed by the word or phrase you want translated.")
            elif mb == "tips":
                tips = randint(1, 7)
                if tips == 3:
                    v = ("1. Practicing Japanese"
            "\nHere's my advice for practicing Japanese: if you find yourself trying to figure out how to say an "
            "English thought in Japanese, save yourself the trouble and stop because you won't get it right most of the time."
            "You should always keep in mind that if you don't know how to say it already, then you don't know how to say it. "
            "Instead, if you can, ask someone how to say it in Japanese including a full explanation of the answer and start practicing from Japanese. "
            "Language is not a math problem; you don't have to figure out the answer. If you practice from the answer, you will "
            "develop good habits that will help you formulate correct and natural Japanese sentences.")
                elif tips == 2:
                    v = ("2. Japanese Speaking"
            "\nTo improve Japanese speaking proficiency, Leo bot recommends listening to 「すかいぷちゃんねる」with one quick search on "
            "YouTube thousands of videos come up of people talking about random things")
                elif tips == 1:
                    v = ("3. Mastering Japanese"
            "\nExamples and experience will be your main tools in mastering Japanese. Therefore, even if you don't "
            "understand something completely the first time, just move on and keep referring back as you see more examples.")
                elif tips == 4:
                    v = ("4. Relax in Japanese"
            "\nOnce you’ve finished the last season of Breaking Bad, start getting your daily TV fix with Japanese dramas. "
            "If you’ve been studying with text books, this approach will give you some valuable exposure to less formal, everyday language. "
            "Gooddrama.net is your one-stop-shop.")
                elif tips == 5:
                    v = ("5. Avoid burn-out"
            "\nJapanese can fry your brain. If you’re having an off day or if your brain is already tired of studying, see if you might "
            "be able to watch Japanese videos, for example your favourite anime. This is a way to keep Japanese active in your brain "
            "without the strain of studying a textbook or doing Anki. Some recommended video resources: "
            "For absolute beginners: Let’s Learn Japanese.\nFor upper beginners: Erin’s Challenge.\nFor everyone: Understand Your Favourite TV Series in 30 days.")
                elif tips == 6:
                    v = ("6. Don’t learn from (some) anime"
            "\nA lot of Japanese learners get quite shockingly embarrassed when they find out that the line they just repeated from "
            "Dragonball Z in the middle of the civilised dinner is the equivalent of shouting out “you motherf*****”. "
            "Some popular anime (popular in America at least, and mostly reserved for little boys in Japan) uses the kind of language "
            "which is in the real world almost exclusively reserved for Yakuza. Using that in polite company will make you look like a big foreign jerk.")
                elif tips == 7:
                    v = ("7. Improve your reading speed with songs"
            "\nFollowing lyrics will help you recognize kana and kanji, increase your reading speeds and, of course, teach you how "
            "Japanese should really sound")
                msg_send(user_from, id_chat, v,flow)
            elif mb == "grammar":
                msg_send(user_from,id_chat,"Please select a level", ["Grammar Beginner", "Grammar Intermediate", "Grammar Expert", "Cancel"])
            elif mb == "grammar beginner":
                msg_send(user_from,id_chat,"Please select a lesson", ["Grammar Lesson 1","Grammar Lesson 2",
                                                                      "Family Member References","Omiyage Use",
                                                                      "Genki vs Ogenki","Oneigai-shimasu vs Kudasai",
                                                                      "Mina-san vs Minna","Cancel"])
            elif mb == "grammar intermediate":
                msg_send(user_from,id_chat,"Please select a lesson",["Spring Activities","Difficult Katakana Words",
                                                                     "Condition Onomatopoeia","Tongue Twisters","Slang Verbs",
                                                                     "Slang Adjectives","Slang Nouns","Going Through Customs","Cancel"])
            elif mb == "grammar expert":
                msg_send(user_from, id_chat, "Please select a lesson", ["WIP", "Cancel"])
            elif mb == "grammar lesson 1":
                msg_send(user_from, id_chat, "Japanese consists of two scripts (referred to as kana) called Hiragana and Katakana. "
            "Hiragana and Katakana consist of a little less than 50 \"letters\", which are actually simplified Chinese characters adopted to form a phonetic script."
            "Chinese characters, called Kanji in Japanese, are also heavily used in the Japanese writing. Most of the words in the "
            "Japanese written language are written in Kanji (nouns, verbs, adjectives). There exists over 40,000 Kanji where about "
            "2,000 represent over 95% of characters actually used in written text. There are no spaces in Japanese so Kanji is necessary "
            "in distinguishing between separate words within a sentence.",flow)
            elif mb == "grammar lesson 2":
                msg_send(user_from,id_chat,"WIP")
            elif "family member references" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/ABQABH_L20_020916_jpod101_video.m4v",flow)
            elif "genki vs ogenki" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/ABQABH_L19_012616_jpod101_video.m4v",flow)
            elif "omiyage use" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/ABQABH_L18_011216_jpod101_video.m4v",flow)
            elif "mina-san vs minna" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/ABQABH_L17_122915_jpod101_video.m4v",flow)
            elif "onegai-shimasu vs kudasai" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/ABQABH_L15_120115_jpod101_video.m4v",flow)
            elif "spring activities" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L1_102614_jpod101_video.m4v",flow)
            elif "difficult katakana words" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L2_102614_jpod101_video.m4v",flow)
            elif "condition onomatopoeia" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L8_102614_jpod101_video.m4v",flow)
            elif "going through customs" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L15_102614_jpod101_video.m4v",flow)
            elif "slang verbs" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L20_102614_jpod101_video.m4v",flow)
            elif "slang adjectives" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L21_011315_jpod101_video.m4v",flow)
            elif "slang nouns" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L22_012715_jpod101_video.m4v",flow)
            elif "tongue twisters" == mb:
                vmsg_send(user_from, id_chat, "https://media.libsyn.com/media/japanesepod101/JWOTWWRFIL_L19_102614_jpod101_video.m4v",flow)
            elif mb == "kana charts":
                msg_send(user_from,id_chat, "Which chart would you like to see?", ["Hiragana Chart", "Katakana Chart", "Cancel"])
            elif mb == "hiragana chart":
                pmsg_send(user_from,id_chat,"https://preview.ibb.co/nxtv1a/Hiragana.jpg",flow)
            elif mb == "katakana chart":
                pmsg_send(user_from,id_chat,"https://preview.ibb.co/kaHYnF/katakana.jpg",flow)
            elif mb == "cancel":
                msg_send(user_from, id_chat, "Is there anything else I can help you with?",
                         ["Grammar", "Translations", "Examples", "Kana Charts", "Time", "Tips", "Facts", "Updates", "Exit"])
            elif mb == "exit":
                msg_send(user_from,id_chat,"Alrighty, またね!")
            elif mb == "time":
                japan = timezone("Asia/Tokyo")
                jpn_time = datetime.now(japan)
                msg_send(user_from, id_chat, "The time in Japan is: {}".format(jpn_time.strftime("%I:%M:%p")),flow)
            elif mb == "facts":
                fact = randint(1, 4)
                if fact == 1:
                    v = "There are 207,738 official traffic lights in Japan. That's 5 times England and 16 times America " \
                        "(density per square kilometre). "
                elif fact == 2:
                    v = "There are 47 provinces in Japan."
                elif fact == 3:
                    v = "Unlike most other countries, Japan has a prime minister, not a president\n Prime minister: " \
                        "総理大臣\nPresident: 大統領 "
                elif fact == 4:
                    v = "Japan consists of over 6,800 islands."
                msg_send(user_from, id_chat, v,flow)
            # Come back and fix this some time later
            # elif mb.split()[0] == "en" or mb.split()[0] == "ja" or mb.split()[0] == "ko" or mb.split()[0] == "de":
            #     client_secret = 'becf5c1efdad47a3bf822aaf0989a6bc'
            #     auth_client = AzureAuthClient(client_secret)
            #     bearer_token = 'Bearer ' + auth_client.get_access_token().decode("utf-8")
            #     headers = {"Authorization ": bearer_token}
            #     translate_url = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}".format(
            #         mb.replace(mb.split()[0], ""), mb.split()[0])
            #     translation_data = requests.get(translate_url, headers=headers)
            #     # parse xml return values
            #     translation = ElementTree.fromstring(translation_data.text.encode('utf-8'))
            #     kik.send_messages([TextMessage(
            #         to=user_from,
            #         chat_id=id_chat,
            #         body=str(translation.text)
            #     )])
            elif "translate" in mb:
                translate(mb, user_from, id_chat)
            else:
                msg_send(user_from, id_chat, "Sorry I couldn't understand you, say \"help\" for commands",flow)

            print(user_from+":"+mb)

        elif isinstance(message, (PictureMessage, VideoMessage, StickerMessage, LinkMessage, FriendPickerMessage)):
            msg_send(user_from, id_chat, "Sorry I couldn't understand you, say \"help\" for commands",flow)
        else:
            msg_send(user_from, id_chat, "Sorry I couldn't understand you, say \"help\" for commands",flow)

    return Response(status=200)


def translate(string, user, chat_id):
    string = string.replace("translate", "")
    response = requests.get("http://jisho.org/api/v1/search/words?keyword={}".format(string))
    response = json.loads(response.content.decode('utf-8'))
    if len(response["data"]) == 0:
        msg_send(user, chat_id, "Word has no definition :(")
    elif len(response["data"][0]["japanese"]) != 0:
        try:
            msg_send(user, chat_id,
                     "is common: {0}\n\njapanese:\n\tword: {1}\t{4}\n\treading: {2}\n\ntranslation: {3}\n\n".format(
                         response["data"][0]["is_common"], response["data"][0]["japanese"][0]["word"],
                         response["data"][0]["japanese"][0]["reading"],
                         response["data"][0]["senses"][0]["english_definitions"],
                         response["data"][0]["senses"][0]["parts_of_speech"]))
        except KeyError:
            msg_send(user, chat_id, "japanese:\t{2}\n\treading: {0}\n\ntranslation: {1}\n\n".format(
                response["data"][0]["japanese"][0]["reading"],
                response["data"][0]["senses"][0]["english_definitions"],
                response["data"][0]["senses"][0]["parts_of_speech"]))


def msg_send(user, chat_id, body, keyboards=[]):
    message = TextMessage(to=user, chat_id=chat_id, body=body)
    if keyboards:
        message.keyboards.append(
            SuggestedResponseKeyboard(hidden=False,
                                      responses=[TextResponse(keyboard)
                                                 for keyboard in keyboards], ))
    kik.send_messages([message])


def vmsg_send(user, chat_id, url, keyboards=[]):
    message = VideoMessage(to=user, chat_id=chat_id, video_url=url)
    if keyboards:
        message.keyboards.append(
            SuggestedResponseKeyboard(hidden=False,
                                      responses=[TextResponse(keyboard)
                                                 for keyboard in keyboards], ))
    kik.send_messages([message])


def pmsg_send(user, chat_id, url, keyboards=[]):
    message = PictureMessage(to=user, chat_id=chat_id, pic_url=url)
    if keyboards:
        message.keyboards.append(
            SuggestedResponseKeyboard(hidden=False,
                                      responses=[TextResponse(keyboard)
                                                 for keyboard in keyboards], ))
    kik.send_messages([message])

if __name__ == "__main__":
    # use any port num you want
    app.run(port=int(sys.argv[1]), host='0.0.0.0', debug=True)
