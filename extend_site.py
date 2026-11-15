"""Build additional local-preview routes using the existing shared page layout."""
from urllib.parse import quote
from html import escape
import os
import re
from repair_steps import workflow
from build_pages import page, hero, link, ROOT, model_paths

drafts = [
 ('3d20','3Д20','Власник окремо назвав 3Д20 серед двигунів серії Д20. Для оцінки можливостей ремонту потрібні повний індекс і паспорт саме цього двигуна.', 'Не прирівнюйте 3Д20 до 1Д20 чи 5Д20 лише за схожим позначенням.'),
 ('u1d6','У1Д6','У1Д6 зазначено окремо в переліку замовника. Уточніть літерні та числові суфікси на табличці двигуна.', 'Позначення У1Д6 і 1Д6 не слід автоматично вважати взаємозамінними.'),
 ('u1d12','У1Д12','Для звернення щодо У1Д12 підготуйте повне заводське маркування та назву установки.', 'Комплектацію, обсяг ремонту і підбір деталей визначають за конкретним виконанням.'),
 ('5d20b-300','5Д20Б-300','5Д20Б-300 наведено як окреме виконання в переліку замовника. У заявці вкажіть індекс повністю.', 'Не припускайте, що деталі цього виконання підходять до 5Д20К-300 без перевірки.'),
 ('5d20k-300','5Д20К-300','5Д20К-300 наведено окремо від 5Д20Б-300. Для запиту потрібні табличка та повний індекс.', 'Додаткова літера в позначенні важлива: комплектацію і сумісність слід уточнювати за документами.'),
 ('utd-20','УТД-20','УТД-20 включений до наданого переліку. Для звернення підготуйте точну модифікацію й заводське маркування.', 'Спільні або схожі позначення не підтверджують сумісності деталей з іншими двигунами.'),
 ('v-55','В-55','Для двигуна В-55 вкажіть повне заводське позначення та модифікацію, якщо вона відома.', 'Можливість робіт та підбору ущільнень оцінюють окремо для конкретного агрегату.'),
 ('v-59','В-59','Позначення В-59 потребує уточнення виконання або суфікса за табличкою чи паспортом.', 'Фото маркування допоможе відрізнити потрібне виконання від близьких позначень.'),
 ('v-84','В-84','Для запиту щодо В-84 вкажіть повний індекс і виконання двигуна.', 'Технічні дані й можливість ремонту необхідно підтверджувати для конкретної модифікації.'),
 ('v-92','В-92','Для В-92 потрібно уточнити точне виконання за маркуванням двигуна.', 'Наявність певної назви у списку не визначає автоматично його комплектацію або сумісність деталей.'),
 ('kamaz','Двигуни КамАЗ','КамАЗ у цьому переліку означає техніку або виробника, а не один конкретний двигун.', 'Знайдіть індекс двигуна та назву модифікації автомобіля: саме вони потрібні для підбору деталей.'),
 ('ural','Двигуни Урал','Урал у переліку позначає техніку, а не однозначну модель двигуна.', 'Для оцінки робіт повідомте модель двигуна, його маркування та виконання автомобіля.'),
 ('kraz','Двигуни КрАЗ','Назва КрАЗ визначає техніку, а не точну модифікацію встановленого двигуна.', 'Повідомте повний індекс з таблички агрегату: двигун не можна визначити лише за назвою машини.'),
 ('cummins-isle-350','Cummins ISLE-350','Для Cummins ISLE-350 важливо звірити повне паспортне позначення й серійний номер двигуна.', 'За наявності повідомте ESN і CPL з таблички: це допомагає уточнити комплектацію та підбір деталей.'),
 ('cummins-vta-903t','Cummins VTA-903T','Для Cummins VTA-903T потрібно звірити повний індекс та серійний номер конкретного виконання.', 'За наявності передайте дані таблички, зокрема ESN і CPL; не переносіть характеристики з інших версій.'),
 ('detroit-diesel','Detroit Diesel','Detroit Diesel — назва виробника, яка охоплює різні серії двигунів.', 'Для звернення уточніть серію, модель і серійний номер з таблички двигуна.'),
]
for slug, label, identity, note in drafts:
    query = quote(label)
    page('dvyhuny/'+slug, label + ': запит щодо ремонту', 'Інформація для звернення щодо ' + label + '.',
      hero('Двигуни / '+label, label+': уточнити ремонт.', 'Повне маркування й опис завдання допоможуть визначити наступний крок.', '../../') +
      f'''<section class="section inner-content"><div><h2>Як визначити виконання</h2><p>{identity}</p><p>{note}</p></div><div><h2>Що підготувати для звернення</h2><p>Маркування двигуна, назву техніки або установки, короткий опис несправності, фото таблички та історію попереднього ремонту, якщо вони є.</p><p>Вартість, строк, випробування та доступність деталей узгоджуються після уточнення конкретного завдання.</p>{link('../../ushchilnennia/', 'Підбір ущільнень')}</div></section><section class="section soft-section"><h2>Підготуйте запит.</h2><p class="measure">Для деталі вкажіть вузол, кількість та артикул або фото, якщо вони відомі.</p>{link('../../kontakty/?engine='+query, 'Підготувати звернення')}</section>''')

page('mahazyn','Магазин запчастин','Підбір прокладок, гумових кілець та ремкомплектів за запитом.',
 hero('Магазин','Деталі для вашого двигуна.','Прокладки, гумові ущільнювальні кільця та ремкомплекти: підбір за моделлю, модифікацією і вузлом.') + '''<section class="section"><div class="shop-intro"><div><h2>Підбір починається з точних даних.</h2><p>Вкажіть маркування двигуна та потрібний вузол. Артикул, сумісність, ціна й наявність уточнюються за запитом.</p></div><figure><img src="../parts-illustration.png" alt="Ілюстрація гумових кілець і прокладок" loading="lazy"><figcaption>Ілюстративне зображення, створене за допомогою ШІ</figcaption></figure></div><div class="service-list"><article><span class="service-index">01</span><div><h3>Гумові ущільнювальні кільця</h3><p>Підбір за двигуном, вузлом та характеристиками деталі.</p>''' + link('kiltsia/', 'Переглянути категорію') + '''</div></article><article><span class="service-index">02</span><div><h3>Прокладки</h3><p>Прокладки для двигунів; частину виробів підприємство виготовляє самостійно.</p>''' + link('prokladky/', 'Переглянути категорію') + '''</div></article><article><span class="service-index">03</span><div><h3>Ремкомплекти</h3><p>Склад і сумісність комплекту уточнюються за запитом.</p>''' + link('remkomplekty/', 'Переглянути категорію') + '''</div></article></div><p class="section-note">Приклади карток наведені для демонстрації структури магазину. Реальні артикулі, ціни, залишки та сумісність ще не надані.</p></section>''')

categories = [('kiltsia','Гумові ущільнювальні кільця','kilce-pryklad','Гумове ущільнювальне кільце'),('prokladky','Прокладки','prokladka-pryklad','Прокладка двигуна'),('remkomplekty','Ремкомплекти',None,None)]
for slug,title,example,example_title in categories:
    body = hero('Магазин / '+title,title+'.','Уточніть модель двигуна та вузол, щоб підібрати необхідну деталь.', '../../')
    body += '<section class="section"><h2>Підбір за запитом</h2><p class="measure">Вкажіть повне маркування двигуна, місце встановлення, кількість і артикул або фото, якщо вони є. Сумісність, ціна й наявність уточнюються окремо.</p>'
    if example:
        body += f'<div class="product-example"><p class="example-label">ПРИКЛАД КАРТКИ</p><h3>{example_title}</h3><p>Демонстраційна картка без артикула, ціни та підтвердженої сумісності.</p>{link(example+"/", "Переглянути приклад")}</div>'
    else: body += '<p>Перелік комплектів та їх склад буде додано після отримання каталогу.</p>'
    body += '</section>'
    page('mahazyn/'+slug,title,'Підбір '+title.lower()+' за запитом.',body)
    if example:
        query=quote(example_title)
        page('mahazyn/'+slug+'/'+example,example_title+' — приклад','Демонстраційна картка для підбору запчастини.',
          hero('Магазин / '+title+' / Приклад',example_title+'.','Приклад оформлення картки: параметри, сумісність і ціна потребують підтвердження.', '../../../') +
          f'''<section class="section product-layout"><div><img src="../../../parts-illustration.png" alt="Ілюстрація ущільнень, не фото конкретного товару"><p class="section-note">Ілюстрація не зображує конкретний товар.</p></div><div><h2>Дані для підбору</h2><p>Модель і модифікація двигуна, вузол, кількість, артикул або креслення за наявності.</p><dl><dt>Артикул</dt><dd>Потребує уточнення</dd><dt>Сумісність</dt><dd>Перевіряється за запитом</dd><dt>Ціна і наявність</dt><dd>Потребують уточнення</dd></dl>{link('../../../kontakty/?type=parts&item='+query, 'Підготувати запит')}</div></section>''')

page('yak-my-pratsiuiemo','Як ми працюємо','Етапи звернення і ремонту двигунів.',
 hero('Як ми працюємо','Від запиту до погодженого ремонту.','Кожен двигун має власну історію. Обсяг і умови роботи визначаються індивідуально.') + '''<section class="section process"><div><h2>Послідовність роботи</h2><p>Для певних двигунів випробування проводять профільні підрядники. Деталі узгоджуються за конкретним замовленням.</p></div><ol><li><strong>Звернення</strong><span>Маркування, опис проблеми та фото за можливості.</span></li><li><strong>Оцінювання і дефектація</strong><span>Стан, можливі роботи та умови діагностики уточнюються окремо.</span></li><li><strong>Погодження</strong><span>Склад робіт, вартість, строк та деталі визначають за результатами оцінювання.</span></li><li><strong>Ремонт і перевірка</strong><span>Обсяг робіт і можливість випробувань залежать від двигуна.</span></li></ol></section>''')
page('pytannia','Поширені запитання','Відповіді про звернення, ремонт і підбір деталей.',
 hero('Питання та відповіді','Відповіді перед зверненням.','Зібрали основні запитання про ремонт двигуна та підбір ущільнень.') + '''<section class="section faq"><details><summary>Коли можна визначити вартість ремонту?</summary><p>Вартість залежить від стану двигуна та потрібних робіт і деталей; її уточнюють після оцінювання і дефектації.</p></details><details><summary>Чи всі двигуни проходять випробування?</summary><p>Можливість випробувань залежить від двигуна і замовлення; частину випробувань проводять підрядники.</p></details><details><summary>Що потрібно для підбору прокладки?</summary><p>Модель і модифікація двигуна, вузол, кількість та артикул, фото або креслення за наявності.</p></details><details><summary>Як діє гарантія?</summary><p>Умови визначаються договором та особливостями конкретного замовлення.</p></details></section>''')
page('dostavka','Доставка та оплата','Узгодження доставки і оплати для деталей та двигунів.',
 hero('Доставка та оплата','Умови узгоджуємо для кожного запиту.','Порядок доставки, оплати та повернення буде додано після підтвердження компанією.') + '''<section class="section inner-content"><div><h2>Деталі та ремкомплекти</h2><p>Доступність, вартість і спосіб передачі деталей уточнюються під час оформлення запиту.</p></div><div><h2>Двигун на ремонт</h2><p>Приймання та можливість доставки агрегату погоджуються індивідуально з урахуванням конкретного завдання.</p>''' + link('../kontakty/', 'Підготувати звернення') + '</div></section>')

# Detailed process and terms from the client's questionnaire, kept at the
# service level; the precise scope depends on the individual engine.
page('yak-my-pratsiuiemo','Як ми працюємо','Як відбувається ремонт двигуна від звернення до випробувань.',
 hero('Як ми працюємо','Від звернення до перевірки двигуна.','Ремонт планують за результатами дефектації та погоджують для конкретного двигуна.') + '''<section class="section process"><div><h2>Етапи роботи</h2><p>Ремонт переважно виконують на території підприємства. Для деяких двигунів стендові випробування проводять залучені підрядники.</p></div><ol><li><strong>Звернення та ідентифікація</strong><span>Вкажіть модель, повне маркування, техніку та опишіть проблему.</span></li><li><strong>Розбирання й дефектація</strong><span>Очищення деталей та вимірювання допомагають визначити їхній стан і необхідні роботи.</span></li><li><strong>Узгодження умов</strong><span>Вартість і строк залежать від стану двигуна та необхідних запчастин; їх уточнюють після дефектації.</span></li><li><strong>Відновлення та складання</strong><span>Непридатні деталі замінюють, а придатні до ремонту відновлюють відповідно до завдання.</span></li><li><strong>Випробування</strong><span>Проводять стендові випробування з відеофіксацією та протоколом параметрів; спосіб перевірки узгоджують для конкретного двигуна.</span></li></ol></section><section class="section soft-section"><h2>Діагностика та гарантія</h2><p class="measure">Якщо очевидну причину можна встановити візуально, такий огляд може бути безкоштовним. Складніша діагностика платна; її умови уточнюються окремо. Гарантія визначається договором та характеристиками виробу, зокрема напрацюванням у мотогодинах.</p>''' + link('../kontakty/', 'Обговорити двигун') + '</section>')

page('pytannia','Поширені запитання','Відповіді про діагностику, гарантію, ремонт і підбір деталей.',
 hero('Питання та відповіді','Відповіді перед зверненням.','Умови залежать від двигуна, його стану та конкретного замовлення.') + '''<section class="section faq"><details><summary>Коли можна визначити вартість і строк ремонту?</summary><p>Після дефектації: вони залежать від стану двигуна, обсягу робіт і необхідних запчастин. За словами підприємства, ремонт може тривати від кількох днів до кількох тижнів; точний строк узгоджується окремо.</p></details><details><summary>Чи платна діагностика?</summary><p>Візуальне встановлення очевидної причини може бути безкоштовним. Складніша діагностика платна; її умови уточнюються відповідно до завдання.</p></details><details><summary>Як перевіряють двигун після ремонту?</summary><p>Проводять стендові випробування з відеофіксацією та протоколом. Деякі типи двигунів випробовують у підрядників; порядок для конкретного замовлення узгоджується окремо.</p></details><details><summary>Яка гарантія на ремонт?</summary><p>Умови гарантії визначаються договором і характеристиками конкретного виробу, зокрема напрацюванням у мотогодинах.</p></details><details><summary>Як підібрати прокладку чи кільце?</summary><p>Підготуйте модель і модифікацію двигуна, вузол, кількість, артикул, фото або креслення за наявності. Ціну і сумісність уточнюють за запитом.</p></details><details><summary>Чи працюєте з клієнтами з інших регіонів?</summary><p>Компанія приймає звернення з усіх регіонів України. Ремонт зазвичай виконують на виробництві; в окремих випадках можливий виїзд спеціалістів.</p></details></section>''')
print('Extended catalog, informational pages and 16 engine entries')

# Context-specific facts from manufacturer documentation; no extrapolation to
# unverified variants or claims about the workshop's model-specific operations.
technical_sections = {
 '1d20': '''<section class="section technical-facts"><h2>1Д20 у складі ДГМ-100</h2><p>Керівництво дизель-генератора ДГМ-100 описує установку з двигуном 1Д20. Наведені дані стосуються виконання в цьому керівництві; паспорт конкретного двигуна потрібно звірити окремо.</p><dl><div><dt>Циліндри</dt><dd>6, V-подібне розташування</dd></div><div><dt>Робочий цикл</dt><dd>Чотиритактний дизель</dd></div><div><dt>Охолодження</dt><dd>Рідинне</dd></div></dl><p class="section-note">Історичне технічне джерело не підтверджує перелік ремонтних операцій або сумісність деталей TIR Service.</p><a class="text-link" href="https://djvu.online/file/W1qnFMPDHTDwL">Джерело: керівництво ДГМ-100 ↗</a></section>''',
 '1d6': '''<section class="section technical-facts"><h2>Приклад виконання 1Д6-150С2-01</h2><p>Виробник описує це виконання як стаціонарний дизель для приводу генераторів та окремих рухомих машин. Наведені нижче значення стосуються саме 1Д6-150С2-01, а не всіх двигунів 1Д6 чи У1Д6.</p><dl><div><dt>Циліндри</dt><dd>6, рядне розташування</dd></div><div><dt>Номінальна потужність</dt><dd>150 к.с. при 1500 об/хв</dd></div><div><dt>Охолодження</dt><dd>Рідинне</dd></div></dl><p class="section-note">Дані за описом виробника; паспорт конкретного агрегату має пріоритет. Обсяг доступних ремонтних робіт для цього виконання уточнюється окремо.</p><a class="text-link" href="https://barnaultransmash.ru/1d6-150s2-01">Джерело: опис виробника ↗</a></section>''',
 'cummins-isle-350': '''<section class="section technical-facts"><h2>Сімейство Cummins ISLe</h2><p>У документації Cummins для автомобільного сімейства ISLe наведено шестициліндрову конфігурацію об'ємом 8,9 л. Брошура містить різні налаштування потужності та екологічні виконання, тому дані конкретного двигуна слід звірити за табличкою й серійним номером.</p><dl><div><dt>Сімейство в документації</dt><dd>ISLe</dd></div><div><dt>Кількість циліндрів</dt><dd>6</dd></div><div><dt>Робочий об'єм</dt><dd>8,9 л</dd></div></dl><p class="section-note">Це довідка про сімейство, а не підтвердження характеристик саме вашого ISLE-350. Умови ремонту й сумісність деталей уточнюються індивідуально.</p><a class="text-link" href="https://www.cummins.com/sites/default/files/4971324.pdf">Джерело: брошура Cummins ↗</a></section>''',
}
for slug, section in technical_sections.items():
    target = ROOT / 'dvyhuny' / slug / 'index.html'
    content = target.read_text(encoding='utf-8')
    visual = '''<figure class="generic-engine-image"><img src="../../generic-diesel-illustration.png" alt="Ілюстрація дизельного двигуна в майстерні" loading="lazy" width="1672" height="941"><figcaption>Ілюстрація, створена ШІ: не фотографія цієї моделі або майстерні</figcaption></figure>'''
    content = content.replace('</main>', section + visual + '</main>')
    target.write_text(content, encoding='utf-8')

# Explicitly requested, local-only review images; rights have not been cleared.
# A normal build does not include these. Keep the files out of version control.
preview_photos = {
 '5d20k-300': ('5d20k-300.png', 'Дизель 5Д20К-300 за описом товарного каталогу', 'Дизель 5Д20К-300 за назвою товарної картки; заводське маркування агрегату на зображенні незалежно не перевірено.', 'https://bmz.ru/postavljaem/postavka-dvigatelej/tip-utd-20/'),
 '3d20': ('3d20.jpg', 'Двигун 3Д20, сфотографований перед відправленням', 'Двигун 3Д20 за описом джерела; точне виконання та маркування на фото незалежно не перевірені.', 'https://spbdiesel.ru/news/439.html'),
 'v-6': ('v6.png', 'Двигун В-6Б за описом каталогу', 'В-6Б — приклад виконання двигуна В-6 за описом джерела; зображення не пов’язане з TIR Service.', 'https://bmz.ru/postavljaem/postavka-dvigatelej/tip-v-6/'),
 'v-84': ('v84.webp', 'Двигун В-84 до ремонту за описом джерела', 'Двигун В-84 до ремонту за описом джерела; це не робота TIR Service, маркування на знімку незалежно не перевірено.', 'https://kmz1.ru/uslugi/remont-diesel-dvigateley-b-46-b-84.html'),
 'v-92': ('v92.webp', 'Виставковий двигун В-92С2 за описом фотоальбому', 'В-92С2 — виконання В-92 за підписом автора фотоальбому SilverGhost; табличку агрегату незалежно не перевірено.', 'https://new.scalemodels.ru/albums/1869-tankovyi-dvigatel-v-92s2-dlia-t-90-russian-ex/'),
 '1d6': ('1d6.jpg', 'Дизельний двигун, названий у джерелі 1Д6-150', 'Дизель 1Д6-150 за описом джерела; маркування двигуна не перевірено.', 'https://zdk-nn.ru/articles/zapchasti-dlya-teplovozov-uzkoj-kolei'),
 '1d20': ('1d20.jpg', 'Фрагмент двигуна, названого в оголошенні 1Д20', 'Фрагмент двигуна 1Д20 за описом оголошення; маркування на фото не перевірено.', 'https://flagma.ua/uk/dizelny-dvigatel-1d20100kvt-v-odessa-nikolaev-dnepr-harkov-lvov-o15429139.html'),
 'u1d6': ('u1d6.jpg', 'Двигун, названий у джерелі У1Д6-250ТК', 'У1Д6-250ТК за описом оголошення; маркування двигуна не перевірено.', 'https://flagma.ua/dgu-u1d6-250tk-dizel-generatornaya-ustanovka-o14477860.html'),
 '5d20': ('5d20.jpg', 'Двигун, названий у джерелі 5Д20', 'Двигун 5Д20 за описом оголошення; точну модифікацію за фото не підтверджено.', 'https://flagma.ua/uk/dvigatel-5d20-v-odessa-zhitomir-lvov-dnepr-harkov-kiev-sumy-o15301979.html'),
 '5d20b-300': ('5d20b.jpg', 'Двигун, показаний у дописі про ремонт 5Д20Б-300', 'Двигун із допису про ремонт 5Д20Б-300; маркування на знімку незалежно не перевірено.', 'https://t.me/kmz1ru/1439'),
 'v-59': ('v59.webp', 'Двигун В-59УМС до ремонту за описом джерела', 'В-59УМС до ремонту за описом джерела; знімок зроблено не в TIR Service.', 'https://kmz1.ru/news/kapitalnyy-remont-v59ums.html'),
}
if os.environ.get('TIR_SHOW_UNCLEARED_PHOTOS') == '1':
    for slug, (filename, alt, caption, source) in preview_photos.items():
        target = ROOT / 'dvyhuny' / slug / 'index.html'
        content = target.read_text(encoding='utf-8')
        generic = '''<figure class="generic-engine-image"><img src="../../generic-diesel-illustration.png" alt="Ілюстрація дизельного двигуна в майстерні" loading="lazy" width="1672" height="941"><figcaption>Ілюстрація, створена ШІ: не фотографія цієї моделі або майстерні</figcaption></figure>'''
        content = content.replace(generic, '')
        figure = f'''<figure class="verified-photo"><img src="../../assets/preview-candidates/{filename}" alt="{escape(alt)}" loading="lazy"><figcaption>{escape(caption)} <a href="{escape(source, quote=True)}">Джерело фото</a>. Тимчасовий знімок для локального перегляду; права на публікацію не підтверджено.</figcaption></figure>'''
        target.write_text(content.replace('</main>', figure + '</main>'), encoding='utf-8')

# The client confirmed the supplied list as engines they service. Keep model
# labels separate and carry the selected label into the inquiry draft.
for model, relative in model_paths.items():
    target = ROOT / 'dvyhuny' / relative / 'index.html'
    content = target.read_text(encoding='utf-8')
    content = content.replace('уточнити ремонт.', 'ремонт та обслуговування.')
    content = content.replace('Можливість ремонту, випробувань та наявність деталей уточнюються для конкретної модифікації.', 'Обсяг ремонту, порядок випробувань та наявність деталей визначаються для конкретної модифікації.')
    content = content.replace('Можливість робіт та підбору ущільнень оцінюють окремо для конкретного агрегату.', 'Обсяг робіт та підбір ущільнень визначають окремо для конкретного агрегату.')
    content = content.replace('Власник окремо назвав 3Д20 серед двигунів серії Д20.', '3Д20 належить до переліку двигунів серії Д20, з якими ми працюємо.')
    content = content.replace('У дослідженні зустрічаються різні виконання 1Д6', 'Серед виконань 1Д6 зустрічаються різні позначення')
    content = content.replace('href="../../kontakty/"', 'href="../../kontakty/?engine=' + quote(model) + '"')
    safe_model = escape(model)
    info = f'''<section class="section inner-content engine-repair-detail"><div><h2>Як обговорити ремонт {safe_model}</h2><p>Повідомте точне маркування, назву техніки та що саме турбує. За можливості підготуйте фото таблички, відомості про напрацювання й попередні ремонти. Це допоможе визначити наступні кроки для вашого агрегату.</p><p>За описом підприємства, ремонт може включати розбирання, очищення, вимірювання деталей, відновлення або заміну несправних компонентів і складання. Склад робіт погоджується після оцінювання двигуна.</p></div><div><h2>Деталі та умови</h2><p>Для підбору прокладки, гумового кільця чи ремкомплекту потрібні модель і модифікація, вузол та, за наявності, артикул або фото. Сумісність і наявність перевіряються окремо.</p><p>Вартість і строк залежать від стану двигуна та потрібних деталей. Умови діагностики, випробувань і гарантії узгоджуються для конкретного замовлення.</p><a class="text-link" href="../../yak-my-pratsiuiemo/">Як проходить ремонт ↗</a></div></section>'''
    content = content.replace('</main>', info + '</main>')
    target.write_text(content, encoding='utf-8')

service_path = ROOT / 'posluhy' / 'remont-dyzelnykh-dvyhuniv' / 'index.html'
service = service_path.read_text(encoding='utf-8')
service = service.replace('</main>', '''<section class="section technical-facts"><h2>Діагностика, терміни та гарантія</h2><p>Якщо очевидну причину пошкодження можна визначити візуально, огляд може бути безкоштовним. Складніша діагностика платна; умови залежать від завдання. Після дефектації узгоджують обсяг, ціну й строк ремонту.</p><p>Гарантія визначається договором і характеристиками виробу, зокрема напрацюванням у мотогодинах. Для деяких типів двигунів стендові випробування проводять підрядники; їхні результати фіксують у протоколі та на відео.</p><a class="text-link" href="../../yak-my-pratsiuiemo/">Переглянути етапи роботи ↗</a></section></main>''')
service_path.write_text(service, encoding='utf-8')

# Photos are separate from workshop images: the Commons description supports
# the engine family or model stated in the caption, not a particular client unit.
photo_specs = {
 'u1d12': ('1d12-tu2.jpg', 'Двигун 1Д12 у моторному відсіку тепловоза ТУ2 в Іршаві', 'Для ознайомлення: двигун 1Д12 у тепловозі ТУ2 в Іршаві. Джерело не підтверджує, що це У1Д12; комплектація може відрізнятися.', 'Varga Attila', 'https://commons.wikimedia.org/wiki/File:TU2_Irshava_7.jpg', 'CC BY-SA 2.5', 'https://creativecommons.org/licenses/by-sa/2.5/'),
 'kraz': ('yamz-238.jpg', 'Дизельний двигун ЯМЗ-238 на музейній експозиції', 'ЯМЗ-238 — приклад сімейства двигунів, яке встановлювали на КрАЗ-255. На фото музейний експонат; його конкретне виконання не уточнене. Модель вашого двигуна слід перевірити за маркуванням.', 'Александр Сигачёв', 'https://commons.wikimedia.org/wiki/File:%D0%94%D0%B8%D0%B7%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_%D0%AF%D0%9C%D0%97_238.jpg', 'CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
 'ural': ('yamz-238.jpg', 'Дизельний двигун ЯМЗ-238 на музейній експозиції', 'ЯМЗ-238 — приклад сімейства двигунів, окремі виконання якого встановлюють на автомобілі Урал. Точне виконання експоната не уточнено.', 'Александр Сигачёв', 'https://commons.wikimedia.org/wiki/File:%D0%94%D0%B8%D0%B7%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_%D0%AF%D0%9C%D0%97_238.jpg', 'CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
 'cummins-vta-903t': ('cummins-vta-903t.jpg', 'Обслуговування двигуна Cummins VTA 903 T 525', 'Cummins VTA 903 T 525 під час обслуговування; конкретне виконання вашого двигуна може відрізнятися. Фото не пов’язане з майстернею TIR Service.', 'Martin Cuaron, U.S. Navy', 'https://commons.wikimedia.org/wiki/File:US_Navy_110406-N-QP268-157_Lance_Cpl._David_Ahrens_does_maintenance_on_an_amphibious_assault_vehicle_(AAV)_Cummins_VTA_903_T_525_diesel_engine_aboa.jpg', 'Public Domain Mark 1.0', 'https://creativecommons.org/publicdomain/mark/1.0/'),
 'v-55': ('v55.jpg', 'Фрагмент музейного двигуна В-55, вид зверху', 'Фрагмент двигуна В-55 на музейній експозиції; виконання вашого двигуна може відрізнятися.', 'Thomas Vogt', 'https://commons.wikimedia.org/wiki/File:Sowjetischer_Panzermotor_W-55,_Antrieb_des_T55_und_direkter_Nachfahre_des_W-2_im_T-34_(51437244758).jpg', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/'),
 'detroit-diesel': ('detroit-series60.jpg', 'Двигун Detroit Diesel Series 60 у моторному відсіку', 'Приклад двигуна Detroit Diesel Series 60; серію вашого двигуна та можливість ремонту потрібно уточнити.', 'Panoha (автор зазначений умовно у джерелі)', 'https://commons.wikimedia.org/wiki/File:Detroit_D60_diesel.jpg', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/'),
 'kamaz': ('kamaz-740.jpg', 'Дизельний двигун КамАЗ-740 на стенді', 'Приклад двигуна КамАЗ-740; для ремонту потрібне точне маркування вашого агрегату.', 'АЗПИ', 'https://commons.wikimedia.org/wiki/File:%D0%9F%D0%BE%D0%BB%D0%BD%D0%BE%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%9A%D0%90%D0%9C%D0%90%D0%97-740.jpg', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
 'v-46': ('v-46-6.jpg', 'Музейний експонат двигуна В-46-6, вигляд зверху', 'Музейний експонат двигуна В-46-6: приклад одного з виконань В-46.', 'Triple-green', 'https://commons.wikimedia.org/wiki/File:Russischer_Panzermotor_W-46-6_(38039041282).jpg', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/'),
 'utd-20': ('utd-20.jpg', 'Музейний експонат двигуна УТД-20 у розрізі', 'Музейний експонат УТД-20 у розрізі; комплектація двигуна може відрізнятися.', 'Triple-green', 'https://commons.wikimedia.org/wiki/File:UTD-20_Diesel_V6_des_BMP_(24383514397).jpg', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/'),
 'yamz-238': ('yamz-238.jpg', 'Дизельний двигун ЯМЗ-238 на музейній експозиції', 'ЯМЗ-238 на музейній експозиції; точне виконання на сторінці джерела не уточнено.', 'Александр Сигачёв', 'https://commons.wikimedia.org/wiki/File:%D0%94%D0%B8%D0%B7%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_%D0%AF%D0%9C%D0%97_238.jpg', 'CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
 'cummins-isle-350': ('cummins-isl.jpg', 'Двигун Cummins ISL із трансмісією ZF Ecolife', 'Двигун сімейства Cummins ISL із трансмісією ZF Ecolife; модифікацію ISLE-350 для цього фото не підтверджено.', 'Bouchecl', 'https://commons.wikimedia.org/wiki/File:Cummins_ISL_-_ZF_Ecolife.JPG', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
}
for slug, (filename, alt, caption, author, source, license_name, license_url) in photo_specs.items():
    target = ROOT / 'dvyhuny' / slug / 'index.html'
    content = target.read_text(encoding='utf-8')
    if slug == 'cummins-isle-350':
        generic = '''<figure class="generic-engine-image"><img src="../../generic-diesel-illustration.png" alt="Ілюстрація дизельного двигуна в майстерні" loading="lazy" width="1672" height="941"><figcaption>Ілюстрація, створена ШІ: не фотографія цієї моделі або майстерні</figcaption></figure>'''
        content = content.replace(generic, '')
    change_note = 'оригінальне зображення' if filename == '1d12-tu2.jpg' else 'зображення зменшено'
    figure = f'''<figure class="verified-photo"><img src="../../assets/verified/{filename}" alt="{escape(alt)}" loading="lazy"><figcaption>{escape(caption)} Фото: {escape(author)}, <a href="{source}">Wikimedia Commons</a>, <a href="{license_url}">{license_name}</a>; {change_note}.</figcaption></figure>'''
    content = content.replace('</main>', figure + '</main>')
    target.write_text(content, encoding='utf-8')

# Illustrative assets for pages without a clean, model-confirmed photograph.
engine_art = {'1d6':'1Д6', 'u1d6':'У1Д6', '1d20':'1Д20', '3d20':'3Д20', '5d20':'5Д20', '5d20b-300':'5Д20Б-300', '5d20k-300':'5Д20К-300', 'v-6':'В-6', 'v-59':'В-59', 'v-84':'В-84', 'v-92':'В-92'}
for slug, model in engine_art.items():
    target = ROOT / 'dvyhuny' / slug / 'index.html'
    content = target.read_text(encoding='utf-8')
    content = re.sub(r'<figure class="generic-engine-image">.*?</figure>', '', content, flags=re.S)
    picture = f'''<figure class="engine-art"><img src="../../assets/generated-engines/{slug}.jpg" alt="Ілюстрація дизельного двигуна для сторінки {escape(model)}" width="1536" height="1024" loading="lazy"><figcaption>Ілюстрація для ознайомлення; вигляд двигуна {escape(model)} може відрізнятися.</figcaption></figure>'''
    content = content.replace('</main>', picture + '</main>')
    target.write_text(content, encoding='utf-8')

# Keep the same client-approved workflow on the homepage and the detail page.
home_path = ROOT / 'index.html'
home = home_path.read_text(encoding='utf-8')
home = re.sub(r'<section class="section repair-workflow" id="repair-workflow">.*?</section>', workflow(), home, count=1, flags=re.S)
if 'id="repair-workflow"' not in home:
    home = re.sub(r'<section class="section inner-content"><div><h2>Як відбувається ремонт</h2>.*?</section>\s*<section class="section process">.*?</section>', workflow(), home, count=1, flags=re.S)
home = re.sub(r'(<div class="engine-grid" id="engine-list" aria-live="polite">).*?(</div>)', lambda m: m.group(1) + ''.join(f'<span><a href="dvyhuny/{relative}">{escape(model)}</a></span>' for model, relative in model_paths.items()) + m.group(2), home, count=1, flags=re.S)
home = home.replace('Усі двигуни та сторінка 1Д20 ↗', 'Усі двигуни ↗')
home_capabilities = '''<section class="section workshop-overview" id="workshop-overview"><div><h2>Обладнання для ремонту та контролю.</h2><p>На виробництві використовують вимірювальний інструмент, обладнання для механічної обробки, миття та фарбування, а також стенд для ремонту паливної апаратури.</p><a class="text-link" href="pro-kompaniiu/">Більше про виробництво <span aria-hidden="true">↗</span></a></div><div class="workshop-overview-detail"><h3>Контроль на кожному етапі</h3><p>За інформацією підприємства, спеціаліст контролює процес від приймання двигуна до видачі. Склад робіт і спосіб випробувань погоджують для конкретного замовлення.</p></div></section>'''
if 'id="workshop-overview"' in home:
    home = re.sub(r'<section class="section workshop-overview" id="workshop-overview">.*?</section>', lambda _: home_capabilities, home, count=1, flags=re.S)
else:
    home = home.replace('<section class="section repair-workflow"', home_capabilities + '<section class="section repair-workflow"', 1)
quick_form = '''<section class="section quick-feedback" id="quick-feedback"><div><h2>Потрібна консультація?</h2><p>Залиште ім’я та номер телефону, щоб підготувати запит щодо ремонту двигуна.</p></div><form class="quick-form" data-callback-form><label>Ваше ім’я<input name="name" type="text" autocomplete="name" maxlength="100" required placeholder="Як до вас звертатися"></label><label>Номер телефону<input name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="25" required placeholder="+380"></label><button class="button" type="submit">Підготувати звернення <span aria-hidden="true">↗</span></button><p class="callback-note">Локальний макет: заявка не надсилається. Текст можна скопіювати.</p><div class="callback-result" hidden><label>Текст звернення<textarea rows="3" readonly></textarea></label><button class="outline-button" type="button" data-copy-callback>Скопіювати текст</button><p role="status"></p></div></form></section>'''
if 'id="quick-feedback"' not in home:
    home = home.replace('</main><footer>', quick_form + '</main><footer>')
home_path.write_text(home, encoding='utf-8')
process_path = ROOT / 'yak-my-pratsiuiemo' / 'index.html'
process = process_path.read_text(encoding='utf-8')
process = re.sub(r'<section class="section process">.*?</section>', workflow('../'), process, count=1, flags=re.S)
process_path.write_text(process, encoding='utf-8')

# Capabilities transcribed from the client's handwritten answers. Do not infer
# that every engine can be tested on a company-owned stand.
about_path = ROOT / 'pro-kompaniiu' / 'index.html'
about = about_path.read_text(encoding='utf-8')
about_details = '''<section class="section workshop-details"><h2>Виробництво та обладнання.</h2><p class="workshop-lead">За інформацією підприємства, виробнича площа становить близько 300 м². Оснащення допомагає виконувати різні етапи ремонту та контролювати стан деталей.</p><div class="workshop-columns"><div><h3>Механічна обробка й підготовка</h3><p>Обладнання для розточування і шліфування, миття та фарбування, токарний верстат, ручний та електричний інструмент.</p></div><div><h3>Перевірка і переміщення</h3><p>Вимірювальні інструменти, стенд для ремонту паливного насоса високого тиску та підйомне обладнання для роботи з агрегатами.</p></div><div><h3>Контроль якості</h3><p>За повідомленням компанії, спеціаліст контролює процес від приймання двигуна в ремонт до його видачі. Порядок випробувань узгоджують для конкретного агрегату.</p></div></div><p class="workshop-note">Частину стендових випробувань двигунів проводять залучені підрядники; наявність потрібного обладнання та обсяг робіт уточнюються для конкретного замовлення.</p></section>'''
about_path.write_text(about.replace('</main>', about_details + '</main>'), encoding='utf-8')

# Keep the customer-facing presentation neutral while retaining provenance
# and exact-model limitations in research-input/РЕЄСТР-ФОТО-2026.md.
for html_path in ROOT.rglob('index.html'):
    html = html_path.read_text(encoding='utf-8')
    html = re.sub(r'<figcaption>Ілюстрація, створена ШІ: не фотографія цієї моделі або майстерні</figcaption>', '', html)
    html = re.sub(r'<figcaption>Ілюстративне зображення, створене за допомогою ШІ</figcaption>', '', html)
    html = re.sub(r'<figcaption>Ілюстрація для ознайомлення; вигляд двигуна [^<]+ може відрізнятися\.</figcaption>', '', html)
    html = html.replace('<figcaption>Ілюстрація для ознайомлення.</figcaption>', '')
    html = html.replace('<p class="section-note">Ілюстрація не зображує конкретний товар.</p>', '')
    html_path.write_text(html, encoding='utf-8')
