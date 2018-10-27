from app.modules.domain_chatbot.user import User
from app.modules.domain_chatbot.emergency import Emergency
from app.modules.domain_chatbot.hospital import Hospital
from app.modules.domain_chatbot.disease import Disease
from app.modules.domain_chatbot.weather import Weather
from app.modules.domain_chatbot.wow import Wow
from app.modules.domain_chatbot.location import Location
from app.modules.domain_chatbot.reminder import Reminder
from app.modules.domain_chatbot.concern import Concern
from app.modules.domain_chatbot.special import Special
from app.modules.domain_chatbot.recipe import Recipe

class Chatbot:

    # 取domain不為'none'的，flag為'user_nickname'不需剔除
    def __init__(self, domain_score, flag=None, nickname=None):

        if flag == 'user_nickname':
            word_domain = []
            for domain in domain_score:
                dic = {}
                dic['word'] = domain['word']
                dic['domain'] = domain['domain']
                word_domain.append(dic)
        else:
            word_domain = []
            for domain in domain_score:
                # 280712, 不過濾none
                dic = {}
                dic['word'] = domain['word']
                dic['domain'] = domain['domain']
                word_domain.append(dic)
                '''這是原本代碼
                if domain['domain'] != 'none':
                    dic = {}
                    dic['word'] = domain['word']
                    dic['domain'] = domain['domain']
                    word_domain.append(dic)
                '''
        
        self.word_domain = word_domain
        self.flag = flag
        self.nickname = nickname

    # 根據flag及domain決定選擇哪個模組的覆流程
    # flag -> None or user_done or disease_done or location_done 表示完成該模組的回覆流程
    # flag -> user_xxx or disease_xxx or loaction_xxx 表處於哪個模組的回覆流程中
    def response_word(self):
        # TODO 新增 or concern_done
        if self.flag is None or self.flag == 'recipe_done' or self.flag=='special_done' or self.flag=='user_done' or self.flag=='emergency_done' or self.flag=='hospital_done' or self.flag=='disease_done' or self.flag=='weather_done' or self.flag=='wow_done' or self.flag=='wow_phone' or self.flag=='location_done' or self.flag=='reminder_done' or self.flag=='morning_concern_done' or self.flag=='noon_concern_done':
            domain = self.choose_domain()
            if domain == 'user':
                user = User()
                return user.response()
            # 決定為emergency的模組流程，可先收集word
            elif domain == 'emergency':
                emergency = Emergency(word_domain=self.word_domain, flag='emergency_init')
                return emergency.response()
            # 決定為hospital的模組流程，可先收集word
            elif domain == 'hospital':
                hospital = Hospital(word_domain=self.word_domain, flag='hospital_init')
                return hospital.response()
            # 決定為disease的模組流程，可先收集word
            elif domain == 'disease':
                disease = Disease(word_domain=self.word_domain, flag='disease_get')
                return disease.response()
            # 決定為weather的模組流程，可先收集word
            elif domain == 'weather':
                weather = Weather(word_domain=self.word_domain, flag='weather_init')
                return weather.response()
            # 決定為wow的模組流程，可先收集word
            elif domain == 'wow':
                wow = Wow(word_domain=self.word_domain, flag='wow_init')
                return wow.response()
            elif domain == 'recipe':
                recipe = Recipe(word_domain=self.word_domain, flag='recipe_init')
                return recipe.response()
            # 決定為location的模組流程，可先收集word
            elif domain == 'location':
                location = Location(word_domain=self.word_domain, flag='location_init')
                return location.response()
            # 決定為reminder的模組流程，可先收集word
            elif domain == 'reminder':
                reminder = Reminder(word_domain=self.word_domain, flag='reminder_init')
                return reminder.response()
            # 決定為morningconcern的模組流程
            elif domain == 'morningconcern':
                concern = Concern(word_domain=self.word_domain, flag='morning_init', nickname=self.nickname)
                return concern.response()
            # 決定為noonconcern的模組流程
            elif domain == 'noonconcern':
                concern = Concern(word_domain=self.word_domain, flag='noon_init')
                return concern.response()
            # 決定為nightconcern的模組流程
            elif domain == 'nightconcern':
                concern = Concern(word_domain=self.word_domain, flag='night_init')
                return concern.response()
            # 決定為special(domain=none)的流程
            else:
                special = Special()
                return special.response()
        else:
            if 'user' in self.flag:
                user = User(word_domain=self.word_domain, flag=self.flag)
                return user.response()
            elif 'emergency' in self.flag:
                emergency = Emergency(word_domain=self.word_domain, flag=self.flag)
                return emergency.response()
            elif 'hospital' in self.flag:
                hospital = Hospital(word_domain=self.word_domain, flag=self.flag)
                return hospital.response()
            elif 'disease' in self.flag:
                disease = Disease(word_domain=self.word_domain, flag=self.flag)
                return disease.response()
            elif 'weather' in self.flag:
                weather = Weather(word_domain=self.word_domain, flag=self.flag)
                return weather.response()
            elif 'wow' in self.flag:
                wow = Wow(word_domain=self.word_domain, flag=self.flag)
                return wow.response()
            elif 'recipe' in self.flag:
                recipe = Recipe(word_domain=self.word_domain, flag=self.flag)
                return recipe.response()
            elif 'location' in self.flag:
                location = Location(word_domain=self.word_domain, flag=self.flag)
                return location.response()
            elif 'reminder' in self.flag:
                reminder = Reminder(word_domain=self.word_domain, flag=self.flag)
                return reminder.response()
            elif 'morning' in self.flag:
                concern = Concern(word_domain=self.word_domain, flag=self.flag)
                return concern.response()
            elif 'noon' in self.flag:
                concern = Concern(word_domain=self.word_domain, flag=self.flag)
                return concern.response()
            elif 'night' in self.flag:
                concern = Concern(word_domain=self.word_domain, flag=self.flag)
                return concern.response()

    # 選擇哪個domain模組的回覆流程
    def choose_domain(self):
        isUser = False
        isEmergency = False
        isHospital = False
        isDisease = False
        isWow = False
        isRecipe = False
        isLocation = False
        isWeather = False
        isReminder = False
        isConcern = '' # 要分是早上、中午或晚上的關心

        magic_location = ['老人共餐', '友善餐廳', '長照中心', '餐廳', '旅館', '運動中心', '銀髮友好站', '美術館', '樂齡中心', '魔術地點']

        for data in self.word_domain:
            if data['domain'] == '個人化' or data['domain'] == '性別':
                isUser = True
            if data['domain'] == '緊急聯絡人':
                isEmergency = True
            if data['domain'] == '醫院':
                isHospital = True
            if data['domain'] == '感冒' or data['domain'] == '慢性病':
                isDisease = True
            if data['domain'] == '天氣':
                isWeather = True
            if data['domain'] == '食譜' or data['domain'] == '食譜類別':
                isRecipe = True
            if data['domain'] in magic_location:
                isWow = True
            if data['domain'] == '地點' or data['domain'] == '城市':
                isLocation = True
            if data['domain'] == '提醒':
                isReminder = True
            if data['domain'] == '關心':
                isConcern = data['word']

        if isUser:
            return 'user'
        elif isEmergency:
            return 'emergency'
        elif isHospital:
            return 'hospital'
        elif isDisease:
            return 'disease'
        elif isWeather:
            return 'weather'
        elif isRecipe:
            return 'recipe'
        elif isWow:
            return 'wow'
        elif isLocation:
            return 'location'
        elif isReminder:
            return 'reminder'
        elif isConcern:
            return isConcern
        # domain為none的情況
        else:
            return 'none'
