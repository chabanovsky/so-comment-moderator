# encoding:utf-8
from utils import process_text

'''
To get a list of words from a page on wiktionary use the following script than review to make it one–word–lenght each.
items = $(".mw-category-group li a")
txt = ""
for (var i = 0; i < items.length; i++) {
    txt += "'" + $(items[i]).text() + "', "
}
'''
class WiktionaryOrg:
    __props = None
    
    processed_obscene_word_list = None
    processed_abusive_word_list = None
    processed_rude_word_list    = None
    processed_irony_word_list   = None
    processed_contempt_word_list= None
    processed_neglect_word_list = None
    processed_humiliation_word_list = None

    # https://ru.wiktionary.org/wiki/Категория:Матерные_выражения/ru
    __obscene_words = ["архипиздрит","ахуй","ахулиард","пизды","бля","блядёшка","блядина","блядища","блядки","блядовать","блядовитый","блядство","блядствовать","блядун","блядь", "ахуе","ёбаный","пизду","взъёб","взъебать","взъёбка","взъёбывать","волоёб","вхерачить","въёб","въебать","въебаться","въебашить","въебенить","въёбка","въёбывать","выблядок","выебать","выебаться","выебнуть","выебнуться","выебон","выебсти","выёбывать","выёбываться","выеть","пиздой","ебака","пизды","допизды","дохуища","дохуя","довыёбываться","доебаться","долбоёб","долбоебизм","долбоёбище","долбоёбство","допиздеться","дохулион","дохуя","драпиздон","драпиздончик","дядеёб","ёб","ебак","ебака","ебало","ебальник", "ебальничек", "ебан","ебанатик","ёбанный","ебаноид","ебанутый","ебануть","ебануться","ебанушка","ебаный","ёбаный","ебарёк","ёбарь","ебать","ебаться","ебач","ебашить","ебашиться","ебенамать","ебёна","ебеный","ебёный","ебеня","ёбкий","еблан","ебланить","еблец","ебливый","ебля","ёбля","ёбнутый","ёбнуть","ёбнуться","ебота","еботе","еботня","ебошить","ебошиться","ёбс","переёбс","ебсти","ебун","ебур","ебут","ебучий","ебучка","ёбфренд","ёбши","ёбывать","ебырок","ёпт","ёпть","хуище","хуем","заблядовать","заёб","заёба","заебательский","заебато","заебатый","заебать","заебаться","заебенить","заебёшься","заебись","заебок","заебунеть","заёбушка","запиздеться","запиздючить","захуевертить","захуярить","захуячить","здрахуйте","злоебучий","нахуярить","испиздить","исхуярить","исхуячить","ебене","ебеней","хуя","коноёбить","коноёбиться","косоёбить","мозгоёб","мозгоебатель","мозгоебательство","хуёк","мудоёб","отъебись","впизду","пизду","хуище","хуй","нахуй","жопа","хую","нахуя","наебалово","наебать","наёбка","наебнуть","наебнуться","наёбщик","наёбщица","наёбывать", "напиздеть","напиздеться","напиздить","настоебать","настопиздеть","нах","нахуевертить""нахуй","нахуя","нахуяриться","невъебенный","нехуй","схуя","хуясебе","нихуясе","хуясе","объебать","объебаться","объебон","объебос","объёбывать","овцеёб","однохуйственно","одолбоёбиться","опездал","опиздюлиться","ослоёб","остоебенить","остопиздеть","остопиздить","остохуеть","отпиздить","отхуесосить","отхуярить","отхуячить","отъебать","отъебаться","отъебошить","отъёбываться","охуевать","охуевший","охуение","охуенно","охуенный","охуетительный","охуеть","охуительно","охуительный","переебать","перехуярить","пизда","пиздануть","пиздануться","пиздарики","пиздарики","пиздато","пиздатый","пиздёж","пиздёнка","пиздёночка","пиздёныш","пиздеть","пиздец","пиздий","пиздить","пиздища","пиздище","пиздливый","пиздоблядство","пиздобол","пиздоболить","пиздобратия","пиздовать","пиздодельный","пиздой","пиздолиз","пиздорванец","пиздорванка","пиздоремонтник","пиздоремонтничек","пиздос","пиздострадалец","пиздуй","пиздун","пиздушечка","пиздушка","пизды","пиздюк","пиздюлина","пиздюль","пиздюхать","пиздюшка","пиздятина","пиздятинка","пиздящий","повыёбываться","подзаебаться","подъебать","подъебаш","подъёбка","подъебнуть","подъебон","подъебончик","подъебушка","подъёбывать","поебать","поебаться","поебень","поеботина","поёбывать","попизде","похуист","попизделки","попиздеть","попиздовать","похуизм","похуист","похуистка","похуй","похую","припиздень","припиздить","проблядь","проёб","проебать","проебаться","проёбчик","проёбщик","проёбывать","пропиздеть","шестихуй","разъебай","разъебуха","распиздеть","распиздеться","распиздун","распиздяй","распиздяйка","распиздяйство","расхуяривать","расхуярить","расхуячить","снихуя","свиноёб","семихуй","смехуёчки","спиздеть","спиздить","спиздиться","страхопиздище","сцуко","съебать","съебаться","съёбывать","толстопиздый","уебан","уебать","уебаться","уёбище","уёбок","уёбский","уёбывать","упиздить","упиздовать","хитровыебанный","худоёбина","хуев","хуева","хуевастый","хуевато","хуеватый","хуёвина","хуёвничать","хуёво","хуевый","хуёвый","хуеглот","хуежопый","хуек","хуем","хуеньки","хуеплёт","хуеплётка","хуепутало","хуерыга","хуерык","хуесос","хуесосить","хуета","хуетень","хуеть","хуец","хуёчек","хуила","хуило","моржовый","хуильник","хуина","хуинушка","хуишко","хуище","хуй","нихуя","хуйнаны","перехуй","хуйкино","хуйло","хуйлыга","хуйнуть","хуйня","хуле","хули","хуль","хуля","перехуля","хуяк","хуяка","хуякать","хуякнуть","хуякс","хуярить","хуястый","хуячить","шароёбить","шароёбиться","ябать"]
    # https://ru.wiktionary.org/wiki/Категория:Бранные_выражения/ru
    __abusive_words = ['абаза', 'анафема', 'антихрист', 'аршинник', 'аспид', 'бандеровец', 'банный', 'баран', 'басурманин', 'безбожник', 'бесовка', 'бля', 'блядёшка', 'блядь', 'богомерзкий', 'ботало', 'бревно', 'быдло', 'варнак', 'вафлёр', 'вахлак', 'ведьма', 'вертячий', 'чёрт', 'википедик', 'википидор', 'вилюшка', 'вертячий', 'висельник', 'вошь', 'выблядок', 'выморозок', 'выхухоль', 'гад', 'гадёнок', 'гадёныш', 'гадина', 'гадюка', 'галимый', 'гамадрил', 'гандон', 'гнида', 'гнидный', 'гнилушка', 'говно', 'говноед', 'голоштанник', 'гондон', 'грымза', 'грязнуха', 'губошлёп', 'дебил', 'дебилоид', 'дегенерат', 'дерьмократ', 'дерьмократия', 'дешёвка', 'днище', 'долбоёб', 'дрянь', 'дубьё', 'дундук', 'дуролом', 'душегуб', 'дылда', 'дьявол', 'дядеёб', 'ёбаный', 'ебырок', 'жопа', 'жопошник', 'задрот', 'залупа', 'залупать', 'зверьё', 'зверюга', 'злодей', 'векша', 'идиотина', 'идиотка', 'идолёнок', 'имбецил', 'ирод', 'искариот', 'искариотка', 'ишак', 'к чёрту', 'кайло', 'калбит', 'каналья', 'кикимора', 'клуша', 'кобылий', 'козёл', 'козлина', 'колорад', 'колотовка', 'курва', 'курица', 'лайдак', 'лахудра', 'лежень', 'леший', 'лох', 'луганда', 'лягва', 'лярва', 'мазурик', 'манда', 'мерзавец', 'мерин', 'мокрохвостка', 'молофья', 'морда', 'мразь', 'мудак', 'мудачество', 'мудила', 'мудило', 'мудозвон', 'мымра', 'наволочь', 'негодяй', 'недоумок', 'нехристь', 'нечисть', 'нихрена', 'ниггер', 'овца', 'оглоед', 'одёр', 'олигофрен', 'опидореть', 'остолоп', 'отмудохать', 'отродье', 'охальник', 'охламон', 'павиан', 'падаль', 'падла', 'падло', 'паразит', 'пархатый', 'паршивец', 'паскуда', 'паскудница', 'паскудный', 'педрила', 'пердун', 'перечница', 'пехтерь', 'пидарас', 'пидор', 'пидорас', 'пидорасня', 'пиздобол', 'пиздорванец', 'пиздорванка', 'пиздюк', 'пиявица', 'пиявка', 'поганец', 'поганка', 'подлый', 'подлюга', 'подонок', 'подстилка', 'политическая', 'проститутка', 'попадья', 'потаскунья', 'поц', 'придурок', 'прихвостень', 'прожига', 'прохвост', 'прохвостка', 'прошмандовка', 'пьянь', 'развалина', 'раздолбай', 'разъебай', 'ракалия', 'ракалья', 'ржавчина', 'сапожник', 'свинья', 'сволота', 'скотина', 'скурвиться', 'собака', 'собачий', 'сопливец', 'спермохлёб', 'срань', 'срань', 'господня', 'срать', 'стерва', 'стервец', 'сука', 'сукин', 'сучара', 'сучок', 'сучонок', 'сцуко', 'тварь', 'толеразм', 'толераст', 'толерастия', 'толстопиздый', 'ублюдок', 'ублюдочный', 'уголёк', 'удод', 'укронацист', 'укронацистка', 'укроп', 'укрофашизм', 'укрофашист', 'укрофашистка', 'укурок', 'ушлёпок', 'фашист', 'хабальный', 'хайло', 'халда', 'хамка', 'хамов', 'хер', 'херь', 'холера', 'хохол', 'христопродавец', 'хрыч', 'хуежопый', 'хуеплёт', 'хуеплётка', 'хуесос', 'хуйло', 'хуйлыга', 'черножопый', 'чертовка', 'чурбак', 'чурбан', 'чучело', 'шайтан', 'шакал', 'шалава', 'шантрапа', 'швабра', 'шелупонь', 'шкода', 'шкура', 'шлюха', 'шпендик', 'шпендрик', 'штопаный', 'гондон', 'ярыжка']
    # https://ru.wiktionary.org/wiki/Категория:Грубые_выражения/ru
    __rude_words    = ['алкояд', 'анальчик', 'бельмо', 'бздёж', 'бздение', 'бздун', 'бздунья', 'бздюшка', 'блядь', 'болт', 'бред', 'кобылы', 'буркалы', 'быдлить', 'пьяный', 'вафлёрша', 'вдуть', 'взбзднуть', 'вправить', 'вразжопицу', 'выблядок', 'выжрать', 'высирать', 'высираться', 'гадюка', 'подколодная', 'глиста', 'говнина', 'говнистый', 'говниться', 'говно', 'говнозадый', 'говнокачка', 'говнососка', 'говнюк', 'голубизна', 'гоношила', 'дебилка', 'дерьмо', 'дерьмово', 'дерьмовость', 'дерьмовый', 'дожраться', 'долбанутый', 'дрисня', 'дристун', 'дрочила', 'дрючить', 'жопой', 'дура', 'дурак', 'жидовка', 'жлобский', 'жопа', 'жопень', 'жопиться', 'жопник', 'жопой', 'жополиз', 'жратва', 'жраться', 'жрачка', 'заблевать', 'загибаться', 'загнуться', 'задалбывать', 'задалбываться', 'задарма', 'задолбать', 'задрачиваться', 'зажопить', 'зажраться', 'заколебать', 'зарубить', 'засранец', 'зассать', 'зассыха', 'засушина', 'заткнуться', 'затыкаться', 'изговнять', 'изговняться', 'издохнуть', 'издыхать', 'катиться', 'кривожопый', 'кузькина', 'матка', 'мокрощёлка', 'мужлан', 'мурло', 'мутный', 'навернуть', 'надраться', 'нажираться', 'накось', 'напереть', 'насрать', 'начихать', 'золотуха', 'неуважаемый', 'носяра', 'обделаться', 'обожраться', 'обосрать', 'обосраться', 'обоссаться', 'околевать', 'околеть', 'остохренеть', 'отлезть', 'отпидорасить', 'отшить', 'охереть', 'охренительный', 'очкун', 'падла', 'паскудник', 'паскудничать', 'паскудство', 'пасть', 'педик', 'пердак', 'пердь', 'передохнуть', 'передыхать', 'пережрать', 'пидорюга', 'пиздюк', 'пистон', 'пихнуть', 'подонок', 'подохнуть', 'подстилка', 'подыхать', 'пожрать', 'понасрать', 'пороть', 'пороться', 'поссать', 'потаскуха', 'потаскушка', 'придрочиться', 'провафлить', 'прожирать', 'пустобрёх', 'пятак', 'раззявить', 'рыло', 'ряха', 'ряшка', 'сжирать', 'смердящий', 'сосалка', 'сосать', 'сраный', 'срань', 'срать', 'ссака', 'ссать', 'ссут', 'ссыкотно', 'ссыкун', 'стабилизец', 'стервец', 'стояк', 'хернёй', 'сука', 'сучоныш', 'сыкун', 'табло', 'толстомордый', 'трындеть', 'тупорылый', 'узкоглазый', 'упираться', 'употребить', 'урыльник', 'урюк', 'усратый', 'утырок', 'ушлёпок', 'фиговый', 'фукнуть', 'хавальник', 'хам', 'хамло', 'хамьё', 'харчок', 'хачик', 'хлебало', 'хлебальник', 'хмырь', 'хрена', 'хренов', 'хрюкало', 'хряпать', 'рыло', 'цунар', 'цунареф', 'черномазый', 'чёртов', 'четырёхглазый', 'чмо', 'чмошник', 'чмошница', 'чурбан', 'булками', 'шлюха']
    # https://ru.wiktionary.org/w/index.php?title=Категория:Ироничные_выражения/ru
    __irony_words   = ['маркиза', 'трусы', 'накрахмалил', 'авгур', 'автоджигит', 'авторица', 'адамовский', 'административный', 'зуд', 'аз', 'айболит', 'алгвазил', 'альгвазил', 'амбре', 'апофегей', 'арапа', 'ареопаг', 'армагеддец', 'артист', 'погорелого', 'театра', 'излишество', 'аутодафе', 'ахулиард', 'баба', 'бамбарбия', 'киргуду', 'банная', 'кочерга', 'банный', 'слоновой', 'ветрил', 'царя', 'белокепочник', 'пушистый', 'беременный', 'бич', 'блага', 'цивилизации', 'благоверный', 'благоглупость', 'покорно', 'благотворительность', 'божий', 'одуванчик', 'божок', 'крым','бомж', 'борзописание', 'борцуха', 'вдогонку', 'бремя', 'терпит', 'буржуй', 'жопе', 'жопу', 'муда', 'репертуаре', 'валенок', 'ванговать', 'Васька', 'ватник', 'вежливенький', 'вежливенько', 'велеречивость', 'великий', 'могучий', 'величаться', 'вече', 'вздыхатель', 'вздыхательница', 'взрывчик', 'витийствовать', 'влопаться', 'возопить', 'волапюк', 'вояжёр', 'вояжировать', 'вояка', 'планеты', 'впечатленьице', 'вручант', 'всезнайка', 'всезнающий', 'свежести', 'выраженьице', 'высоколобый', 'выспренность', 'выступальщик', 'вышесидящий', 'галантерейный', 'гееборец', 'гениальничать', 'геронтофилия', 'глаголить', 'гладкопись', 'говно', 'говноед', 'господчик', 'грамотей', 'грибоед', 'коммунизм', 'социализм', 'гурия', 'гусь', 'даладно', 'полусвета', 'угодник', 'датский', 'даун', 'двухминутка', 'ненависти', 'дедсад', 'колбаса', 'деловой', 'демиург', 'демократесса', 'депутан', 'диванные', 'войска', 'диванный', 'теоретик', 'дивный', 'дитятя', 'барабана', 'додик', 'домотканый', 'допотопный', 'допросец', 'досидент', 'дохулион', 'дражайший', 'драматургесса', 'драндулет', 'думалка', 'дуче', 'душевед', 'душераздирающий', 'душеспасительный', 'дщерь', 'дядя', 'Ёбург', 'евангелие', 'еврейское', 'еврореволюция', 'евростроитель', 'ерундиция', 'принца', 'яйцами', 'погоды', 'женская', 'женщина', 'труп', 'животное', 'жизнеучитель',  'жрец', 'Фемиды', 'киселя', 'загранвояж', 'заединщик', 'законотворец', 'заседательство', 'заумствовать', 'зацарствовать', 'защитничек', 'звездун', 'звездунья', 'звероящер', 'златоуст', 'зреть', 'зряплата', 'Сусанин', 'идефикс', 'изм', 'имать', 'индивидуй', 'кадавр', 'кадр', 'губернска', 'верста', 'камлание', 'Капитан', 'Очевидность', 'кэп', 'капреализм', 'капсоревнование', 'каптруд', 'кашевар', 'квартирант', 'кино', 'киноопус', 'китайская', 'грамота', 'козлетон', 'генерал', 'конспиролог', 'конь', 'пальто', 'корифей', 'король', 'кость', 'красавчик', 'партизан', 'кремледворец', 'критикесса', 'кузькина', 'культурка', 'слепота', 'либеральничать', 'лимонничать', 'литвождь', 'лицезреть', 'лобызать', 'лошадь', 'лукавый', 'царедворец', 'мавр', 'маман', 'мандавошка', 'мандатоносец', 'мартобрь', 'матушка', 'ментор', 'бисер', 'милость', 'многоглаголиво', 'многознайка', 'моветон', 'хуёк', 'мордодел', 'морлок', 'мудаком', 'мудилка', 'картонная', 'мудрила', 'мусьё', 'мыльнооперный', 'наголосовать', 'награждать', 'тулуп', 'дубовый', 'сосновый', 'барабан','нессы', 'компот', 'Гондурасом','небожитель', 'небыдло', 'негр', 'недоросль', 'немилость', 'неофит', 'неприкасаемый', 'непуганый', 'нетленка', 'неужели', 'ничтоже', 'сумняшеся', 'облагодетельствовать', 'облобызать', 'ОБС', 'общеньице', 'окольцеваться', 'окольцовываться', 'окрошка', 'олауреаченный', 'опровергатель', 'оскароносица', 'осчастливливание', 'отец', 'откопаться', 'отпрыск', 'паж', 'паноптикум', 'партайгеноссе', 'педераст', 'пейзанка', 'пенис', 'переезжать', 'переживашка', 'переучка', 'персонаж', 'песнь', 'пиздоремонтник', 'пиздюк', 'пиитический', 'пипл', 'хавает', 'пирамидостроитель', 'пирамидостроительница', 'писсоюз', 'барабану', 'милости', 'подвизаться', 'подходец', 'подъёбывать', 'позвоночник', 'поздравить', 'памперсов', 'покорно', 'покреативить', 'полировка', 'политес', 'политесса', 'полкан', 'половой', 'демократ',  'понятненько', 'портфеленосец', 'посадка', 'посконный', 'пособолезновать', 'пофигист',  'бозе', 'почтеннейший', 'губерния', 'правоверный', 'прекраснодушие', 'прекраснодушный', 'премудрость', 'преуспеяние', 'придворный', 'приказать', 'ислам', 'приснопамятный', 'прихватизация', 'прихватизировать', 'прихватизироваться', 'прихватить', 'прихватывать', 'прогулка', 'прогуляться', 'прожект', 'профбосс', 'профурсетка', 'прошмандовка', 'псалом', 'психиатор', 'раб', 'Божий', 'раскланяться', 'раскулачивание', 'распрекрасный', 'рассекать', 'рассуждизм', 'редиска', 'рекорд', 'родич', 'рожать', 'россиянец', 'Россияния', 'россиянский', 'рубака', 'рыцарь', 'Буратино', 'самопровозгласить', 'самопровозглашать', 'сателлит', 'свербёж', 'свергалка', 'сверхдемократ', 'светский', 'священнодействие', 'седалище', 'Полишинеля', 'семидесяхнутый', 'сепулька', 'сермяжная', 'валенок', 'скромница', 'словеса', 'слухмейкер', 'колокольни', 'собачий', 'совещаловка', 'совпис', 'соизволение', 'соизволить', 'соображалка', 'сосать', 'спикериада', 'среднепотолочный', 'старовер', 'старуха', 'страдивариус', 'строчить', 'строчкогон', 'строчкогонство', 'студентик', 'суверенизатор', 'супермен', 'суслик', 'сфабрикованный', 'сфабриковать', 'схлопатывать', 'схлопотать', 'телеса', 'тестенёк', 'титулоносец', 'сапой', 'неуместен', 'торжественно', 'торжественный', 'травоядный', 'триппер', 'трудоголик', 'трындычиха', 'турникмен', 'тушка', 'удобоваримый', 'удостоиться', 'уёбок', 'узкоплёночный', 'улицезреть', 'умник', 'упражняться', 'матчасть',  'финита', 'комедия', 'фюрер', 'халява', 'харч', 'хитрожопый', 'хуета', 'моржовый', 'цивилизатор', 'чадо', 'человейник', 'чтец', 'чучело', 'шагистика', 'петушок', 'штукатурить', 'шумахер', 'щеголять', 'юзверь', 'яйцеголовый', 'яство', 'ять']
    # https://ru.wiktionary.org/w/index.php?title=Категория:Презрительные_выражения/ru
    __contempt_words= ['австрияк', 'азик', 'айзер', 'алкашня', 'алтынник', 'алтынница', 'альфонс', 'аморальщина', 'анонимщик', 'апостат', 'армяшка', 'аэропортишко', 'белогвардейщина', 'белоподкладочник', 'бздых', 'бздышка', 'бизнесмент', 'бомжара', 'буржуин', 'буржуй', 'быдло', 'быдляк', 'ватник', 'видеопорнуха', 'википидор', 'винище', 'вкусовщина', 'власовщина', 'воришка', 'вороньё', 'ворюга', 'выродок', 'высер', 'вытиран', 'вяньгать', 'гадёныш', 'гайдарёнок', 'гайдучок', 'гауляйтер', 'гейропа', 'гетераст', 'гидра контрреволюции', 'гнилуха', 'гнилушка', 'гнильцо', 'говнина', 'говноед', 'голубизна', 'гопник', 'гринго', 'гэбня', 'давалка', 'двурушник', 'двурушничество', 'дебилизор', 'демокрад', 'демонократия', 'демофашизм', 'демофашист', 'демофашистский', 'демшиза', 'демшизоид', 'демшизоидный', 'депутан', 'депутатишко', 'джамшутка', 'джихад', 'диссидентщина', 'додик', 'дохлик', 'дрань', 'дурачьё', 'дурдом', 'ебарёк', 'ельциноид', 'ельцинщина', 'жадюга', 'живец', 'жириновщина', 'жлоб', 'завлаб', 'зажравшийся', 'зануда', 'западоид', 'казачок', 'зубрила', 'избабиться', 'интеллигентщина', 'истукан', 'карапетина', 'кацапка', 'керенка', 'китаёза', 'кляузнический', 'кляузничество', 'кляузный', 'колбасня', 'коммуноидный', 'коммунофашист', 'коммуняга', 'коммуняка', 'коммуняцкий', 'контра', 'копираст', 'кремлядь', 'крыса', 'крысы', 'кулачьё', 'лаврушник', 'лакейский', 'лакейство', 'лакейщина', 'лампасник', 'либераст', 'либерастия', 'лизать', 'лизоблюд', 'лукавый', 'царедворец', 'лыка', 'мавр', 'майданутый', 'мамкоёб', 'мигалочник', 'мизинца', 'михрютка', 'мракобес', 'мракобесие', 'мудаком', 'националюга', 'недобиток', 'недоверок', 'нечисть', 'обезьянничать', 'образованец', 'образованщина', 'обрыган', 'огарок', 'одёр', 'ОКУПанты', 'оскотиниться', 'отродье', 'офицерня', 'офицерщина', 'офицерьё', 'папик', 'тролль', 'паханат', 'певичка', 'перебежчик', 'перец', 'ПЖиВ', 'пиараст', 'писачка', 'плебейство', 'погань', 'подонство', 'политикан', 'порнограф', 'постсовок', 'потёмкинская', 'поцреот', 'православнутый', 'праздношатающийся', 'присный', 'приспособленчество', 'прихватизатор', 'прихватизаторский', 'прихватизационный', 'прихлебательница', 'прокаркать', 'пропагандон', 'пропагандонский', 'пропагандонство', 'пропагандонствовать', 'проприетарщина', 'проститутка', 'прохвост', 'прощелыга', 'путиноид', 'мясо', 'ренегат', 'сбрендить', 'сброд', 'сексотить', 'сексотка', 'сексотство', 'сибаритство', 'сквалыга', 'сквалыжник', 'скэб', 'смерд', 'смердящий', 'собчачий', 'соглашательство', 'сопливец', 'сосулька', 'спидозник', 'ссыкло', 'баранов', 'стихокропатель', 'стихоплётство', 'стрюцкий', 'сучка', 'съездюк', 'сытый', 'типок', 'тряпичность', 'тюремщик', 'укурок', 'фефёла', 'хам', 'хамить', 'хамка', 'хамство', 'ханжа', 'ханжеский', 'ханжество', 'хуила', 'хуило', 'моржовый', 'черносотенец', 'чинодрал', 'чинуша', 'чумазый', 'Чуркистан', 'чухна', 'шаркун', 'петушок', 'школоло', 'школярство', 'шкурничество', 'шлюха', 'шпана', 'щегол', 'яйцеголовый']
    # https://ru.wiktionary.org/wiki/Категория:Пренебрежительные_выражения/ru
    __neglect_words = ['абортмахер', 'агитка', 'азер', 'актриска', 'америкашка', 'америкос', 'аршинник', 'аршинничать', 'баба', 'бабёха', 'бабий', 'бабища', 'бабка', 'бабский', 'байда', 'баклан', 'балахонник', 'бандура', 'банкирчик', 'банная', 'кочерга', 'барахло', 'барахольщик', 'бахвал', 'башка', 'бебехи', 'бездарь', 'безлимитка', 'белиберда', 'белибердень', 'берданка', 'балалайка', 'бланбек', 'бодяжить', 'болтология', 'бомба', 'бомжатник', 'бомжина', 'борцун', 'босяк', 'ботаник', 'бредни', 'бредовый', 'бредятина', 'брехлама', 'брехня', 'брошенка', 'бубен', 'бульбаш', 'бумагомаратель', 'бытовщина', 'вафлю', 'вафля', 'вахлак', 'Верка', 'верун', 'верхоглядство', 'видеоподвал', 'видеопорнушка', 'видеоширпотреб', 'википедик', 'вирш', 'водяра', 'воришка', 'воспиталка', 'восьмиклашка', 'вошь', 'вульгарщина', 'вшивый', 'выдра',  'выжига', 'высер', 'выскочка', 'выступальщик', 'вякать', 'гарниза', 'тетеря', 'говённый', 'говно', 'говнотечка', 'говночист', 'голодранец', 'голосовальщик', 'голытьба', 'гомо советикус', 'городишко', 'гороховое пальто', 'горючее', 'грамотёшка', 'гяур', 'бубен', 'хрюсло', 'даун', 'дворянчик', 'девчонка', 'дед', 'дезертир', 'демократишка', 'депутатишко', 'деревенщина', 'деревня', 'деталюшка', 'детективщина', 'детский', 'лепет', 'дешёвка', 'деятель', 'джанк', 'джинса', 'динозавр', 'дистрофик', 'додик', 'дохлый', 'дохнуть', 'дрова', 'дрянь', 'дубарь', 'думак', 'дуралей', 'дурачина', 'душонка', 'дядька', 'дятел', 'ебак', 'ебота', 'еботе', 'жвачка', 'желторотый', 'жёлтый', 'жестянка', 'животное', 'жид', 'жидовский', 'жиртрес', 'жиртрест', 'жмот', 'жраньё', 'журналец', 'забугорник', 'забугорье', 'загнать', 'задохлик', 'заёба', 'заединщик', 'заежка', 'закуток', 'залезать', 'замануха', 'онанизмом', 'заправлять', 'заседалово', 'зассыха', 'затрапезный', 'захудаленький', 'зачирикать', 'звездулька', 'звездун', 'звездунья', 'зелёный', 'зомбоящик', 'зубодёр', 'зюганоид', 'зюзя', 'индус', 'интеллигент', 'итальянщина', 'кабысдох', 'калякать', 'крыса', 'капиталист', 'каракатица', 'каталажка', 'кафр', 'кацап', 'квашня', 'кикимора', 'киномакулатура', 'киноопус', 'кисляй', 'клепать', 'клешня', 'кликуша', 'клоповник', 'клуша', 'клюв', 'клянчить', 'кляузник', 'кляча', 'князёнок', 'князь', 'кобыла', 'кобылятник', 'коза', 'колбасник', 'комса', 'коновал', 'контрабас', 'корсак', 'корыто', 'костыль', 'кошатник', 'красавчик', 'краснобайский', 'крендель', 'кропатель', 'крохобор', 'крысить', 'кудахтать', 'кулёк', 'кулугур', 'кулхацкер', 'культик', 'культурка', 'кустарщина', 'кутейница', 'лабух', 'лапотник', 'лаптем', 'щи', 'латиноамериканщина', 'латыш', 'лахудра', 'левацкий', 'легкотня', 'лесбуха', 'летун', 'лжеца', 'лизун', 'литературщик', 'литературщина', 'личер', 'личинус', 'лось', 'лох', 'лохань', 'лоховский', 'лошара', 'лошарик', 'лошок', 'лудить', 'лыбиться', 'любительство', 'любительщина', 'лягуха', 'лягушатник', 'лядащий', 'ляпать', 'мазилка', 'майданщик', 'макаронник', 'маклак', 'макулатурный', 'малевать', 'малёк', 'мальчишка', 'мамзель', 'манекен', 'маратель', 'мартышка', 'мебель', 'меблирашки', 'межеумок', 'мелево', 'мелкота', 'мелкотравчатость', 'мелкочиновный', 'мелюзга', 'меньшевиствовать', 'метёлка', 'милочка', 'миньетчик', 'мозгля', 'хуёк', 'моралфаг', 'моргать', 'мордодел', 'мордочка', 'свинка', 'москаль', 'моська', 'мохнатка', 'мочалка', 'мудачок', 'мудилка', 'мужварьё', 'музейчик', 'мурзик', 'мурзилка', 'мусоровоз', 'мусорок', 'мутота', 'мухомор', 'Мухосранск', 'мымра', 'мякинник', 'нафига', 'навальнёнок', 'надрываться', 'наехать', 'нажраться', 'наймит', 'накропать', 'намазать', 'напялить', 'нарик', 'невменяшка', 'недалёкий', 'недоносок', 'нежность', 'немчик', 'немчура', 'новояз', 'нюня', 'обалдуй', 'обещальщик', 'оболтус', 'обормот', 'образина', 'образованец', 'образованщина', 'образчик', 'овуляшка', 'одноклеточный', 'окорок', 'олень', 'олеография', 'олух', 'опоздун', 'отброс', 'отдыхайка', 'копыта', 'отрыжка', 'очкануть', 'очкарик', 'очкастый', 'очконавт', 'палка', 'палку кинуть', 'пальтишечко', 'пальтишко', 'папик', 'папист', 'папуас', 'парочка', 'парткомщик', 'патриархальщина', 'пепелац', 'пердальник', 'пердь', 'переплюевка', 'Петька', 'пехтура', 'пешка', 'пивас', 'пивнуха', 'пидорок', 'пижня', 'пиздёж', 'пиздища', 'пиздорванка', 'пиздятина', 'пилотка', 'пиндос', 'Пиндостан', 'пипка', 'писака', 'писанина', 'писулька', 'питекантроп', 'плебей', 'плевать', 'пленарка', 'бабьи', 'козлячьи', 'подёнщик', 'подзаборник', 'подстилка', 'подтявкивать', 'подхалимаж', 'поебать', 'политиканчик', 'поп', 'попадейка', 'пописывать', 'попса', 'попсятина', 'попяра', 'портфеленосец', 'посрать', 'постсовок', 'посудина', 'похлёбка', 'свинья', 'пошехонец', 'поэтишка', 'православие', 'приготовишка', 'придурок', 'придурочек', 'проспаться', 'простачок', 'простофиля', 'пугалка', 'пузомерка', 'пустельга', 'пшек', 'пшекать', 'пшекнуть', 'пшют', 'разбежаться', 'распустёха', 'рвань', 'ремеслуха', 'речуга', 'рифмач', 'рокопопс', 'рокопопсовый', 'рохля', 'рублишко', 'русня', 'русопят', 'рухлядь', 'салага', 'салака', 'самец', 'самка', 'самоварник', 'самоиграйка', 'самурай', 'сапожник', 'сбывать', 'свистун', 'свищ', 'сводня', 'семейка', 'сепаратня', 'серенький', 'серость', 'сиволапый', 'скакать', 'скобарь', 'скулить', 'слабак', 'слабачка', 'слёток', 'словопрение', 'смазливый', 'смерд', 'сморчок', 'свиным', 'рылом', 'собака', 'собачья', 'смерть', 'собачонка', 'совдеп', 'совдепия', 'совещаловка', 'совкизм', 'совковость', 'совковский', 'совковщина', 'совпис', 'совчиновник', 'солдатьё', 'солдафон', 'сопливец', 'сопляк', 'соска', 'сосунок', 'социальщина', 'сочинительство', 'спидонос', 'спидоносец', 'спидоносица', 'спидоноска', 'спиногрыз', 'спискота', 'сральник', 'срать', 'стихоплёт', 'стишата', 'субчик', 'супешник', 'сявка', 'табачишко', 'таратайка', 'татарва', 'тёлка', 'терпила', 'технодрочер', 'толстомясый', 'торгаш', 'трахнуться', 'трепач', 'трындеть', 'тряпка', 'тряпочка', 'тряпьё', 'тупоголовый', 'тявкать', 'ублюдок', 'уёбок', 'ужратый', 'ужраться', 'узколобость', 'урюк', 'ухлопать', 'училка', 'фанаберия', 'фанера', 'фанфарон', 'фентезятина', 'ферт', 'фиговина', 'философастер', 'финтифлюшка', 'флюшка', 'форточка', 'фофан', 'фриц', 'фуррятник', 'фуфло', 'фэнтезятина', 'фэнтэзятина', 'халдей', 'халтура', 'халтурщик', 'халупа', 'хамьё', 'ханурик', 'хач', 'хачик', 'хер', 'хлам', 'хлюпик', 'хмырь', 'холоп', 'хрен', 'хреновина', 'хрыч', 'хуёвина', 'хуесос', 'хуета', 'хуец', 'хуй', 'хуйня', 'царёк', 'цекашный', 'цунареф', 'цыганёнок', 'человечина', 'черкать', 'черножопый', 'чубайсёнок', 'чувырла', 'чурбан', 'чурек', 'чурка', 'чухна', 'чухня', 'шабала', 'шаболда', 'шавка', 'шалыга', 'шантропа' 'швабра', 'шваль', 'шелупонь', 'шибздик', 'школяр', 'шкура', 'шлак', 'шляпа', 'шмакодявка', 'шмотки', 'шняга', 'шоферюга', 'шпак', 'штамповать', 'штафирка', 'штиблета', 'штукатурка', 'шушера', 'щелкопёр', 'щенок', 'лаптем', 'эсэнговия', 'юбка', 'юзверь', 'юнец', 'яйца', 'яйцеголовый', 'янки', 'ящик']
    # https://ru.wiktionary.org/w/index.php?title=Категория:Уничижительные_выражения/ru
    __humiliation_words = ['аблакат', 'автоворишка', 'адвокатишка', 'адъютантик', 'алкаш', 'амбарушка', 'амёба', 'анекдотец', 'аристократишка', 'армячишко', 'афишка', 'Афонька', 'бабёшка', 'балабошка', 'банчишко', 'баржонка', 'баритончик', 'бложик', 'блядёшка', 'блядь', 'богачиха', 'братец', 'бредня', 'брошенка', 'брючата', 'брючишки', 'брючонки', 'букашка', 'букетец', 'буржуй', 'Ванька', 'Васька', 'вдовушка', 'возишко', 'волосёнки', 'волчара', 'выкрест', 'выползень', 'газетёнка', 'гешефтмахер', 'говнарь', 'говноед', 'господишки', 'грантоед', 'графчик', 'дворишко', 'дегенератка', 'деградант', 'дегтишко', 'декадентщина', 'делишко', 'деньжишки', 'деньжонки', 'дерьмократ', 'дерьмократический', 'дерьмократия', 'догнить', 'докторишка', 'донкихотишка', 'доходишко', 'драчка', 'дровнишки', 'дура', 'ебанатик', 'ебарёк', 'жалованьишко', 'женишок', 'жид', 'жидоед', 'житьецо', 'житьишко', 'жлоб', 'жопа', 'журналишко', 'жучара', 'заводишко', 'заёба', 'закатишко', 'замчишко', 'захребетничек', 'зверёныш', 'здоровьишко', 'зипунишко', 'притон', 'игрочишка', 'идиотишка', 'избёнка', 'изумрудец', 'инженерик', 'инженеришка', 'инструментишко', 'интеллигентик', 'интеллигентишка', 'ископаемое', 'кабачишко', 'казачишка', 'казачня', 'камарилья', 'капиталец', 'капотишко', 'карасишка', 'картишки', 'картузишко', 'кафтанишко', 'каютишка', 'квартирёнка', 'кенгурятник', 'кепчонка', 'кинед', 'клячонка', 'книженция', 'книжонка', 'кнутишко', 'князишка', 'кобылёнка', 'колбасня', 'комнатишка', 'конишка', 'копипаста', 'кормишко', 'коробчонка', 'корова', 'королёк', 'косоглазый', 'костюмишко', 'кофеишко', 'кофтёнка', 'крестишко', 'кровишка', 'кулак', 'кулачишко', 'кулачок', 'куплетец', 'купчина', 'курчонка', 'кучеришка', 'лакеишка', 'лаптишко', 'лапшишка', 'лейтенантишка', 'лесишко', 'литературка', 'лодчонка', 'лошадёнка', 'людишки', 'Манька', 'матросня', 'мелочишка', 'местишко', 'месячишко', 'мещанинишка', 'мироед', 'молокосос', 'мостишко', 'мотишка', 'мудачок', 'мудилка', 'мужичонка', 'мужчинка', 'музыкантик', 'мундиришко', 'мыслишка', 'навесец', 'навозец', 'народец', 'народишко', 'натуришка', 'недочеловек', 'нервишки', 'пизду', 'ниггер', 'ничтожество', 'новодел', 'новостишка', 'обедец', 'обозец', 'овинишко', 'овощ', 'овсец', 'овсишко', 'одеялишко', 'одобрямс', 'опездал', 'отбитый', 'планктон', 'офицеришка', 'девочка', 'пальтишко', 'папаша', 'папашка', 'паровозишко', 'пароходишко', 'паспортишко', 'пацанчик', 'певун', 'педиковатый', 'переплётец', 'пёс', 'пиджачишко', 'Пиндосия', 'пират', 'писаришка', 'писателишка', 'пистолетишко', 'платьишко', 'плащишко', 'плотишко', 'плохонький', 'козлячьи', 'поваришка', 'повестца', 'подписота', 'поживишка', 'политота', 'полудурок', 'понятьице', 'портняжка', 'поэмка', 'поэтик', 'правозащитничек', 'претенциозный', 'прибамбас', 'притон', 'проектец', 'прокуроришко', 'профурсетка', 'прудишко', 'прыщ', 'девка', 'пудишко', 'пулемётишко', 'пупырь', 'пшекать', 'пшекнуть', 'работёнка', 'рагуль', 'револьверишко', 'рептилия', 'ржишка', 'рублишко', 'рюкзачишко', 'салопишко', 'самоваришко', 'самолюбьишко', 'сапожишко', 'сараишко', 'сарафанишко', 'сбруишка', 'свекруха', 'свинячить', 'сертучишко', 'скандалец', 'скарбишко', 'слизняк', 'совковый', 'совок', 'солдатишка', 'солдатня', 'сопливый', 'сопляк', 'союзничек', 'старикашка', 'старушонка', 'статьишка', 'стиляжка', 'стишок', 'стишонки', 'столяришка', 'страстишка', 'сундучишко', 'сюрпризец', 'сюртучишко', 'Танька', 'таракашка', 'тафтица', 'Тимошка', 'толеразм', 'толераст', 'толобаец', 'торговлишка', 'тошниловка', 'тракторишко', 'требуха', 'пробка', 'тысчонка', 'уголёк', 'усратый', 'фанфаронишка', 'фараончик', 'фразёр', 'французик', 'французишка', 'фрачишка', 'фрачок', 'харчишки', 'харя', 'хахалишка', 'хлопотишки', 'хлыщ', 'хозяюшка', 'холостяга', 'хохол', 'хуерыга', 'хуец', 'хуило', 'хуишко', 'хуй', 'моржовый', 'хуторишко', 'цербер', 'церквёнка', 'чекменишко', 'человечек', 'человечишка', 'человечишко', 'челядь', 'чемоданишко', 'чепанишко', 'чмо', 'чмошник', 'чмошница', 'чуйка', 'чулчишки', 'шавка', 'шапчонка', 'шаромыга', 'школота', 'шкурник', 'шлимазл', 'шляться', 'шофёришка', 'шпажонка', 'шпионишка', 'шулеришка', 'шушунишко', 'щегол', 'юбчонка', 'Яшка']

    @staticmethod
    def word_list_maker(words):
        return [word for word in process_text(u' '.join(words)).split(' ') if len(word.strip()) > 0]

    @staticmethod
    def get_props(prop):
        if WiktionaryOrg.__props is not None:
            return WiktionaryOrg.__props.get(prop, lambda: [])

        WiktionaryOrg.__props = {
            "obscene": WiktionaryOrg.obscene_words,
            "abusive": WiktionaryOrg.abusive_words,
            "rude": WiktionaryOrg.rude_words,
            "irony": WiktionaryOrg.irony_words,
            "contempt": WiktionaryOrg.contempt_words,
            "neglect": WiktionaryOrg.neglect_words,
            "humiliation": WiktionaryOrg.humiliation
        }
        return WiktionaryOrg.get_props(prop)

    @staticmethod
    def obscene_words():
        if WiktionaryOrg.processed_obscene_word_list is not None:
            return WiktionaryOrg.processed_obscene_word_list
        WiktionaryOrg.processed_obscene_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__obscene_words)
        return WiktionaryOrg.processed_obscene_word_list

    @staticmethod
    def abusive_words():
        if WiktionaryOrg.processed_abusive_word_list is not None:
            return WiktionaryOrg.processed_abusive_word_list
        WiktionaryOrg.processed_abusive_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__abusive_words)
        return WiktionaryOrg.processed_abusive_word_list

    @staticmethod
    def rude_words():
        if WiktionaryOrg.processed_rude_word_list is not None:
            return WiktionaryOrg.processed_rude_word_list
        WiktionaryOrg.processed_rude_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__rude_words)
        return WiktionaryOrg.processed_rude_word_list

    @staticmethod
    def irony_words():
        if WiktionaryOrg.processed_irony_word_list is not None:
            return WiktionaryOrg.processed_irony_word_list
        WiktionaryOrg.processed_irony_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__irony_words)
        return WiktionaryOrg.processed_irony_word_list

    @staticmethod
    def contempt_words():
        if WiktionaryOrg.processed_contempt_word_list is not None:
            return WiktionaryOrg.processed_contempt_word_list
        WiktionaryOrg.processed_contempt_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__contempt_words)
        return WiktionaryOrg.processed_contempt_word_list

    @staticmethod
    def neglect_words():
        if WiktionaryOrg.processed_neglect_word_list is not None:
            return WiktionaryOrg.processed_neglect_word_list
        WiktionaryOrg.processed_neglect_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__neglect_words)
        return WiktionaryOrg.processed_neglect_word_list

    @staticmethod
    def humiliation_words():
        if WiktionaryOrg.processed_humiliation_word_list is not None:
            return WiktionaryOrg.processed_humiliation_word_list
        WiktionaryOrg.processed_humiliation_word_list = WiktionaryOrg.word_list_maker(WiktionaryOrg.__humiliation_words)
        return WiktionaryOrg.processed_humiliation_word_list