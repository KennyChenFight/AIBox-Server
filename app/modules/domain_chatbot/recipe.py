import os
import json
import pymongo
import app.modules.logger.logging as log
from app.modules.domain_chatbot.user import User
import datetime
import random
from config import BASE_DIR, LOG_DIR, MONGO_URI, client

class Recipe:
    # 讀取disease.json的模板並收集word
    def __init__(self, word_domain=None, flag=None):
        self.flag = flag
        self.word_domain = word_domain

        with open(os.path.join(BASE_DIR, 'domain_chatbot/template/recipe.json'), 'r', encoding='UTF-8') as input:
            self.template = json.load(input)

        self.collect_data()

    # 當處於回覆流程中，將word填入disease.json模板中
    def collect_data(self):
        if self.word_domain is not None and self.flag is not None:
            if self.flag == 'recipe_init':
                for data in self.word_domain:
                    if data['domain'] == '食譜類別':
                        self.template['類別'] = data['word']
            elif self.flag == 'recipe_type':
                for data in self.word_domain:
                    if data['domain'] == '食譜類別':
                        self.template['類別'] = data['word']
        with open(os.path.join(BASE_DIR, 'domain_chatbot/template/recipe.json'), 'w', encoding='UTF-8') as output:
            json.dump(self.template, output, indent=4, ensure_ascii=False)

    # 根據缺少的word，回覆相對應的response
    def response(self):

        content = {}
        if self.template['類別'] != '':
            content['flag'] = 'recipe_done'
            self.template['推薦回覆'] = self.get_data_form_database()
            content['response'] = self.template['推薦回覆']
            self.store_conversation(content['response'])
            self.clean_template()
        else:
            content['flag'] = 'recipe_type'
            content['response'] = self.template['類別回覆']
            self.store_conversation(content['response'])

        return json.dumps(content, ensure_ascii=False)

    # 從資料庫取得食譜知識
    def get_data_form_database(self):
        logger = log.Logging('recipe:get_data_form_database')
        logger.run(LOG_DIR)
        try:
            db = client['aiboxdb']
            if self.template['類別'] == '中式':
                collect = db['recipes_chinese']
            elif self.template['類別'] == '西式':
                collect = db['recipes_western']
            elif self.template['類別'] == '日式':
                collect = db['recipes_japanese']

            count = collect.count()
            recipe_collect = collect.find()[random.randrange(count)]
            print(recipe_collect['name'])
            ingredients_str = ''
            seasonings_str = '調味料為:'
            instructions_str = ''
            try:
                for str in recipe_collect['ingredients']:
                    ingredients_str += str + '、'
                for str in recipe_collect['seasonings']:
                    seasonings_str += str + '、'
                for str in recipe_collect['instructions']:
                    instructions_str += str
            except KeyError:
                for str in recipe_collect['instructions']:
                    instructions_str += str

            ingredients_str = ingredients_str[0:len(ingredients_str)-1]
            if seasonings_str != '調味料為:':
                seasonings_str = seasonings_str[0:len(seasonings_str)-1] + '。'
            else:
                seasonings_str = ''

            logger.debug_msg('successfully get data from database')
            return '推薦您這道菜:' + recipe_collect['name'] + '。' + '\n' + '原料為:' + ingredients_str + '。' + '\n' + seasonings_str  + '\n' + '烹煮方式為:' + instructions_str + '詳細資訊可至手機上查詢'

        except ConnectionError as err:
            logger.error_msg(err)

    # 清除recipe.json的欄位內容
    def clean_template(self):
        for key in dict(self.template).keys():
            if key != '類別回覆':
                self.template[key] = ''

        with open(os.path.join(BASE_DIR, 'domain_chatbot/template/recipe.json'), 'w', encoding='UTF-8') as output:
            json.dump(self.template, output, indent=4, ensure_ascii=False)

    # 上傳對話紀錄至資料庫
    def store_conversation(self, response):
        User.store_conversation(response)
