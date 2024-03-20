start_text = "<b>Привет!</b> Давай общаться. Как дела?"

help_text = """Привет! Доступные команды:
/start - начать работу
/help - помощь (это сообщение)
/joke - случайная штука
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
