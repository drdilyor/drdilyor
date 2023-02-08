![Greatings, Earthling!](drdilyor.png)

**Why not play mastermind while you are here?**

- **A**: Correct color and position
- **B**: Correct color but wrong position

History
<table>
<tr>
<th>1</th>
<th>2</th>
<th>3</th>
<th>4</th>
<th>A / B</th>
</tr>
{% for history in game.history %}
<tr>
{% for c in history.colors %}
<td>{{ color(c) }}</td>
{% endfor %}
<td>{{ history.correct_position }} / {{ history.correct_color }}</td>
</tr>
{% endfor %}
<tr>
{% for c in game.current %}
<td>{{ color(c) }}</td>
{% endfor %}
<td><strong>Current</strong> (<a href="{{ new_issue_url('mastermind:commit') }}">Commit</a>)</td>
</tr>
</table>



{% if game.won %}
<strong>Congratulations. You won :tada:</strong>
[>New game<]({{ new_issue_url('mastermind:new') }})
{% else %}
<strong>Select colors</strong>
<table>
{% for i in range(1, 7) %}
<tr>
{% for j in range(4) %}
<td>
{% if game.current[j].value == i %}
\>{{ color(i) }}<
{% else %}
&nbsp;<a href="{{ select_url(j, i) }}">
{{ color(i) }}
</a>&nbsp;&nbsp;
{% endif %}
</td>
{% endfor %}
</tr>
{% endfor %}
</table>
[New game]({{ new_issue_url('mastermind:new') }})
{% endif %}


[![Telegram](https://badgen.net/badge/telegram/drdilyor/179cde?icon=telegram)](https://t.me/drdilyor)
![visitors](https://visitor-badge.glitch.me/badge?page_id=drdilyor)

I'm a developer from Uzbekistan 🇺🇿.  People often find me
under username 'drdilyor'.  I think I'm good at learning new things
(except AWS, of course).

Also, I *love* automation.

> Imagine me doing awkward robot dance when you read this. AU-TO-MA-TION

[![Drdilyor's GitHub stats](https://github-readme-stats.vercel.app/api?username=drdilyor&show_icons=1&&theme=vue&hide_title=1&hide_border=1&border_radius=0)](https://github.com/drdilyor)
