from telebot import formatting, types

start_text = "<b>Привет!</b> Давай общаться. Как дела?"

help_text = """Привет! Доступные команды:
/start - начать работу
/help - помощь (это сообщение)
/joke - случайная штука
/joke2 - шутка с каламбуром
/jpy_to_rub 100 - конвертировать 100 JPY в RUB
/cvt 100 JPY - конвертировать 100 JPY в RUB
/cvt 100 JPY IDR - конвертировать 100 JPY в IDR
/set_my_currency RUB - установить целевую валюту
/set_local_currency BYN - установить локальную (исходную) валюту
"""

whatsup_message_text = "Хорошо! А у вас как?"
goodbye_message_text = "До новых встреч!"

dont_forward_commands = "Пожалуйста, не пересылайте команды." " Это может быть опасно."

secret_message_for_admin = "Вот ваше секретное слово: ..."
secret_message_not_admin = "Вам сюда нельзя!"

user_info_doc_caption = "Ваша информация в файле"

great_cat = "Какой классный кот!"

cvt_help_message = "Пожалуйста, укажите аргумент для конвертации, например:"
cvt_jpy_to_rub_how_to = formatting.format_text(
    cvt_help_message,
    formatting.hcode("/jpy_to_rub 100"),
)

cvt_how_to = formatting.format_text(
    cvt_help_message,
    formatting.hcode("/cvt 100 JPY"),
)

invalid_argument_text = "Неправильный аргумент:"
error_fetching_currencies_text = "Что-то пошло не так при запросе, попробуйте позже."
error_no_such_currency = "Неизвестная валюта {currency}, укажите существующую."


set_my_currency_help_message_text = formatting.format_text(
    "Пожалуйста, укажите выбранную валюту. Например:",
    formatting.hcode("/set_my_currency RUB"),
)

set_my_currency_success_message_text = formatting.format_text(
    "Успешно установлена валюта по умолчанию:",
    "{currency}",
)

set_local_currency_help_message = formatting.format_text(
    "Необходимо указать локальную валюту, например:",
    formatting.hcode("/set_local_currency RUB"),
)
set_local_currency_success_message = "Локальная валюта {currency} указана успешно!"

set_local_currency_only_in_private_chat = (
    "Установка локальной валюты доступна только в личном чате."
)

random_message_text = formatting.format_text(
    "Вот сообщение с клавиатурой с рандомом",
)

# survey

survey_cancel_suggestion = formatting.format_text(
    "",
    formatting.format_text(
        "Отменить опрос можно командой /cancel или просто отправьте",
        formatting.hcode("отмена"),
        separator=" ",
    ),
)

survey_message_welcome_what_is_your_full_name = formatting.format_text(
    "Добро пожаловать! Пожалуйста, представьтесь.",
    "Напишите ваше полное имя, например Иван Иванов.",
    survey_cancel_suggestion,
)
survey_message_full_name_not_text = formatting.format_text(
    "Это не текст, а мы хотели бы узнать ваше имя.",
    "Пожалуйста, укажите ваше настоящее имя.",
    survey_cancel_suggestion,
)
survey_message_full_name_ok_and_ask_for_email = formatting.format_text(
    "Добро пожаловать, {full_name}!",
    "Пожалуйста, отправьте ваш email.",
)
survey_message_email_not_ok = formatting.format_text(
    "Это не настоящий email",
    "Пожалуйста, укажите валидный.",
    survey_cancel_suggestion,
)
survey_message_email_ok = formatting.format_text(
    "Почту записали, можно подписать вас на рассылку?",
)
survey_message_invalid_number = formatting.format_text(
    "Это не валидное число. Укажите цифрами."
)
survey_message_invalid_yes_or_no = formatting.format_text(
    "Не понимаю, пожалуйста отправьте да или нет."
)
survey_message_cancelled = formatting.format_text(
    "Опрос отменён. Пройти заново: /survey"
)


def format_message_content_currency_conversion(
    from_curr: str,
    to_curr: str,
    amount_str,
    result_amount_str,
):
    content = types.InputTextMessageContent(
        message_text=formatting.format_text(
            f"{formatting.hcode(amount_str)} {from_curr} в {to_curr}:",
            formatting.hcode(result_amount_str),
        ),
        parse_mode="HTML",
    )
    return content


def format_content_to_result_article(
    from_currency: str,
    to_currency: str,
    amount,
    total_amount,
):
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()
    amount_str = f"{amount:,}"
    result_amount_str = f"{total_amount:,.2f}"
    content = format_message_content_currency_conversion(
        from_curr=from_curr,
        to_curr=to_curr,
        amount_str=amount_str,
        result_amount_str=result_amount_str,
    )
    result = types.InlineQueryResultArticle(
        id=f"{from_currency}-{to_curr}-{amount}",
        title=f"{result_amount_str} {to_curr}",
        description=f"{amount_str} {from_curr} = {result_amount_str} {to_curr}",
        input_message_content=content,
    )
    return result


def prepare_default_result_article(query_id):
    content = types.InputTextMessageContent(
        message_text=formatting.format_text(
            formatting.hbold("Это сообщение из inline запроса!"),
            f"id запроса inline: {formatting.hcode(query_id)}",
        ),
        parse_mode="HTML",
    )
    result = types.InlineQueryResultArticle(
        id="default-answer",
        title="Inline сообщение",
        description="Тут будет информация о текущем запросе и ответе",
        input_message_content=content,
    )
    return result


def format_currency_convert_message(
    from_currency,
    to_currency,
    from_amount,
    to_amount,
):
    return formatting.format_text(
        formatting.hcode(f"{from_amount:,}"),
        f"{from_currency.upper()} это примерно",
        formatting.hcode(f"{to_amount:,.2f}"),
        to_currency.upper(),
        separator=" ",
    )


def format_jpy_to_rub_message(jpy_amount, rub_amount):
    return format_currency_convert_message(
        from_currency="JPY",
        to_currency="RUB",
        from_amount=jpy_amount,
        to_amount=rub_amount,
    )


markdown_text = r"""
*bold \*text*
_italic \_text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=1039918686)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
# pre-formatted fixed-width code block written in the Python programming language

@bot.message_handler(commands=["md"])
def send_markdown_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.markdown_text,
        parse_mode="MarkdownV2",
    )
```
>Block quotation started
>Block quotation continued
>The last line of the block quotation

>The second block quotation started right after the previous

>The third block quotation started right after the previous
"""

html_text = """
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=1039918686">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python"># pre-formatted fixed-width code block written in the Python programming language

@bot.message_handler(commands=["html"])
def send_html_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.html_text,
        parse_mode="HTML",
    )
</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>

<blockquote>Block quotation started
Block quotation continued
The last line of the block quotation
</blockquote>
"""
