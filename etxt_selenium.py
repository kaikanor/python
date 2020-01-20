from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sqlite3
import time
conn = sqlite3.connect("db.db")
cursor_db = conn.cursor()
test = cursor_db.execute("""CREATE TABLE articles (name text, unik int, keys text, sale int, type text, lang text, cat text, len int, price int, type_article text, name_sale text, rating int, reviews_plus int, reviews_min int, date datetime, views int, moder text, quality int)""")

# from selenium.webdriver import Chrome
# browser = Chrome(r"C:\Users\serg\Downloads\operadriver_win32\operadriver_win32\operadriver.exe")
# browser.get('https://www.etxt.ru/users/signin/')
# 5.9

from selenium.webdriver import Chrome
browser = Chrome(r"C:\Users\serg\Downloads\chromedriver_win32\chromedriver.exe")
browser.get('https://www.etxt.ru/users/signin/')
# 6.61

login_area = browser.find_element_by_xpath("//input[@name='login']")
login_area.send_keys("slimper")
login_area = browser.find_element_by_xpath("//input[@name='password']")
login_area.send_keys("bjfdkgjd")
button = browser.find_element_by_xpath("//input[@name='submit']")
button.click()
time.sleep(3)
browser.find_element_by_link_text("Купить статью").click()
select = Select(browser.find_element_by_xpath("//select[@name='onPage']"))
select.select_by_value("100")
button = browser.find_element_by_xpath("//input[@type='submit']")
button.click()

link = browser.find_element_by_xpath("//a[@title='Перейти на последнюю страницу']")
for i in range(1,int(link.text) + 1):
    now = time.perf_counter()
    print("i = " + str(i), end = " ")
    url = "https://www.etxt.ru/admin.php?mod=articles&lib=main&act=show&page=" + str(i)
    browser.get(url)
    html = browser.page_source
    cursor = html.find('<div class="mod-item">')
    j = 0
    while (cursor != -1):
        j += 1
        html = html[cursor + len('<div class="mod-item">'):]
        cursor = html.find('<div class="mod-item">')
        html_for_parse = html[:cursor]

        cursor = html_for_parse.find('title="Скидка на статью">-') + len('title="Скидка на статью">-') # скидка
        cursor_end = html_for_parse.find("%</span>")
        sale_sql = int(html_for_parse[cursor:cursor_end])
        # print(sale_sql)
        html_for_parse = html_for_parse[cursor_end:]

        cursor = html_for_parse.find('<span class="mod-item-typetext">') + len('<span class="mod-item-typetext">') # тип текста
        cursor_end = html_for_parse[cursor:].find("</span>")
        type_sql = html_for_parse[cursor:cursor + cursor_end]
        # print(type_sql)
        html_for_parse = html_for_parse[cursor+cursor_end:]

        cursor = html_for_parse.find('<span class="mod-item-lang"><img src="/images/langs/') + len('<span class="mod-item-lang"><img src="/images/langs/') # язык
        cursor_end = html_for_parse[cursor:].find('.png" title="')
        lang_sql = html_for_parse[cursor:cursor + cursor_end]
        # print(lang_sql)
        html_for_parse = html_for_parse[cursor+cursor_end:]

        cursor = html_for_parse.find('<span class="mod-item-category">') + len('<span class="mod-item-category">') # Категория
        cursor_end = html_for_parse[cursor:].find('</span>')
        cat_sql = html_for_parse[cursor:cursor+cursor_end]
        # print(cat_sql)
        html_for_parse = html_for_parse[cursor+cursor_end:]

        cursor = html_for_parse.find('<div class="mod-item-size"><b>') + len('<div class="mod-item-size"><b>') # длина
        cursor_end = html_for_parse[cursor:].find('</b> символов')
        len_sql = int(html_for_parse[cursor:cursor + cursor_end])
        # print(len_sql)
        html_for_parse = html_for_parse[cursor+cursor_end:]

        cursor = html_for_parse.find('<b class="light">') + len('<b class="light">') # цена за 1000
        cursor_end = html_for_parse[cursor:].find('</b> <span class')
        price_sql = html_for_parse[cursor:cursor+cursor_end]
        # print(price_sql)
        html_for_parse = html_for_parse[cursor+cursor_end:]

        cursor = html_for_parse.find('Тип статьи: <b>') + len('Тип статьи: <b>') # тип статьи
        if cursor - len('Тип статьи: <b>') == -1:
            type_article_sql = 'Не опеределено'
        else:
            cursor_end = html_for_parse[cursor:].find('</b></div>')
            type_article_sql = html_for_parse[cursor:cursor + cursor_end]
            html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(type_article_sql)

        if (html_for_parse.find('<div class="mod-item-quality">') == -1):
            qual_orf = 2
            qual_pun = 2
            qual_rech = 2
        else:
            cursor = html_for_parse.find('images/moder_') + len('images/moder_') # Орфография
            qual_orf = int(html_for_parse[cursor:cursor + 1])
            html_for_parse = html_for_parse[cursor + 1:]
            cursor = html_for_parse.find('images/moder_') + len('images/moder_') # Пунктуация
            qual_pun = int(html_for_parse[cursor:cursor + 1])
            html_for_parse = html_for_parse[cursor + 1:]
            cursor = html_for_parse.find('images/moder_') + len('images/moder_') # Речь
            qual_rech = int(html_for_parse[cursor:cursor + 1])
            html_for_parse = html_for_parse[cursor + 1:]
        # print(qual_orf, qual_pun, qual_rech)

        cursor = html_for_parse.find('Открыть меню пользователя ') + len('Открыть меню пользователя ') # продавец
        cursor_end = html_for_parse[cursor:].find('">')
        name_sale_sql = html_for_parse[cursor:cursor + cursor_end]
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(name_sale_sql)

        cursor = html_for_parse.find('Рейтинг: <b>') + len('Рейтинг: <b>') # рейтинг
        cursor_end = html_for_parse[cursor:].find('</b>')
        rating_sql = int(html_for_parse[cursor:cursor + cursor_end])
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(rating_sql)

        cursor = html_for_parse.find('class="green-link">+ ') + len('class="green-link">+ ') # отзывы+
        cursor_end = html_for_parse[cursor:].find('</a>')
        reviews_plus_sql = int(html_for_parse[cursor:cursor + cursor_end])
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(reviews_plus_sql)

        cursor = html_for_parse.find('class="red-link">- ') + len('class="red-link">- ') # отзывы-
        cursor_end = html_for_parse[cursor:].find('</a>')
        reviews_min_sql = int(html_for_parse[cursor:cursor + cursor_end])
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(reviews_min_sql)

        cursor = html_for_parse.find('Размещено: <b>') + len('Размещено: <b>') # размещено 
        cursor_end = html_for_parse[cursor:].find('</b>')
        date_sql = html_for_parse[cursor:cursor + cursor_end]
        sdvig = 0
        day = date_sql[sdvig:sdvig + 2]
        sdvig += 3
        month = date_sql[sdvig:sdvig + 2]
        sdvig += 3
        year = date_sql[sdvig:sdvig + 4]
        sdvig += 6
        hour = date_sql[sdvig:sdvig + 2]
        sdvig += 3
        minutes = date_sql[sdvig:sdvig + 2]
        date_sql = year + "-" + month + "-" + day + " " + hour + ":" + minutes
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(date_sql)

        cursor = html_for_parse.find('Просмотров: <b>') + len('Просмотров: <b>') # просмотров
        cursor_end = html_for_parse[cursor:].find('</b></div>')
        views_sql = int(html_for_parse[cursor:cursor + cursor_end])
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(views_sql)

        cursor = html_for_parse.find('<font style="color: green;">') + len('<font style="color: green;">') # модерация
        cursor_end = html_for_parse[cursor:].find('</font></span>')
        moder_sql = html_for_parse[cursor:cursor + cursor_end]
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(moder_sql)

        cursor = html_for_parse.find('Постоянный адрес статьи" /> ') + len('Постоянный адрес статьи" /> ') # название
        cursor_end = html_for_parse[cursor:].find('</h4>')
        name_sql = html_for_parse[cursor:cursor + cursor_end]
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(name_sql)

        cursor = html_for_parse.find('<b>Ключевые слова:</b>') + len('<b>Ключевые слова:</b>') # ключевые слова
        cursor_end = html_for_parse[cursor:].find('</p>')
        keys_sql = html_for_parse[cursor:cursor + cursor_end]
        html_for_parse = html_for_parse[cursor + cursor_end:]
        # print(keys_sql)

        if ((html_for_parse.find('title="Текст не проверялся"') != -1) or (html_for_parse.find('title="Текст отправлен на проверку"') != -1)):
            unik_sql = 0
        else:
            cursor = html_for_parse.find('"Проверка на рерайтинг">') + len('"Проверка на рерайтинг">') # уникальность (проверка на рерайтинг)
            cursor_end = html_for_parse[cursor:].find('%</span>')
            unik_sql = int(html_for_parse[cursor:cursor + cursor_end])
            html_for_parse = html_for_parse[cursor + cursor_end:]
            # print(unik_sql)

        cursor = html.find('<div class="mod-item">')

        quality_sql = 1000 + qual_orf*100 + qual_pun*10 + qual_rech
        insert = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(name_sql).replace("'", "''"), str(unik_sql), str(keys_sql).replace("'", "''"), str(sale_sql), str(type_sql), str(lang_sql), str(cat_sql).replace("'", "''"), str(len_sql), str(price_sql), str(type_article_sql), str(name_sale_sql).replace("'", "''"), str(rating_sql), str(reviews_plus_sql), str(reviews_min_sql), str(date_sql), str(views_sql), str(moder_sql).replace("'", "''"), str(quality_sql))
        test = cursor_db.execute("INSERT INTO articles VALUES (" + insert + ")")
    test = conn.commit()

        # with open('text.txt', 'a') as f:
        #     f.write(str(sale_sql) + '   ')
        #     f.write(str(type_sql) + '   ')
        #     f.write(str(lang_sql) + '   ')
        #     f.write(str(cat_sql) + '   ')
        #     f.write(str(len_sql) + '   ') 
        #     f.write(str(price_sql) + '   ')
        #     f.write(str(type_article_sql) + '   ')
        #     f.write(str(qual_orf) + '   ')
        #     f.write(str(qual_pun) + '   ')
        #     f.write(str(qual_rech) + '   ')
        #     f.write(str(name_sale_sql) + '   ')
        #     f.write(str(rating_sql) + '   ')
        #     f.write(str(reviews_plus_sql) + '   ')
        #     f.write(str(reviews_min_sql) + '   ')
        #     f.write(str(date_sql) + '   ')
        #     f.write(str(views_sql) + '   ')
        #     f.write(str(moder_sql) + '   ')
        #     f.write(str(name_sql) + '   ')
        #     f.write(str(keys_sql) + '   ')
        #     f.write(str(unik_sql) + '   ')
        #     f.write('\n')

    print(time.perf_counter() - now)
browser.quit()
print("The end")
print(time.perf_counter())
input()