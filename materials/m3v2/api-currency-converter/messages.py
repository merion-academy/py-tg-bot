from telebot import formatting

start_text = "<b>Привет!</b> Давай общаться. Как дела?"

help_text = """Привет! Доступные команды:
/start - начать работу
/help - помощь (это сообщение)
/joke - случайная штука
/jpy_to_rub 100 - конвертировать 100 JPY в RUB
/cvt 100 JPY - конвертировать 100 JPY в RUB
"""

whatsup_message_text = "Хорошо! А у вас как?"
goodbye_message_text = "До новых встреч!"

dont_forward_commands = (
    "Пожалуйста, не пересылайте команды."
    " Это может быть опасно."
)

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
error_fetching_currencies_text = (
    "Что-то пошло не так при запросе, попробуйте позже."
)
error_no_such_currency = (
    "Неизвестная валюта {currency}, укажите существующую."
)


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
