"""Shared, client-supplied repair workflow for the local preview."""
from html import escape

STEPS = [
    ('Звернення та звірка', 'Повідомте модель і повне маркування, назву техніки та опишіть несправність.', '<path d="M7 3h10l3 3v15H7z"/><path d="M17 3v4h4M10 11h7M10 15h7"/>'),
    ('Розбирання та очищення', 'Двигун розбирають, деталі очищують і миють, видаляють нагар та кокс.', '<path d="M4 8h12M7 5v6m3-6v6m6-5 4 4-7 7-4-4z"/><path d="M4 18l3 3"/>'),
    ('Вимірювання і дефектація', 'Деталі вимірюють інструментами та визначають їхній стан і необхідні роботи.', '<path d="M4 19 19 4l3 3L7 22zM8 15l2 2m1-5 2 2m1-5 2 2m1-5 2 2"/>'),
    ('Погодження ремонту', 'За результатами дефектації узгоджують роботи, потрібні запчастини, вартість і строк.', '<path d="M5 4h14v17H5zM8 8h8M8 12h4m-4 5 2 2 5-5"/>'),
    ('Відновлення і складання', 'Деталі, придатні до ремонту, відновлюють; непридатні замінюють новими та складають двигун.', '<path d="M14 5a4 4 0 0 0-4 5l-6 6a2 2 0 0 0 3 3l6-6a4 4 0 0 0 5-4l-3 2-2-2z"/>'),
    ('Випробування і протокол', 'На стенді записують відео одним кадром із заводським номером, фіксують показники та оформлюють протокол.', '<circle cx="12" cy="12" r="8"/><path d="M12 12l4-4M8 16h8M12 4v2M4 12h2M18 12h2"/>'),
]

def workflow(prefix=''):
    items = ''.join(f'<li><div class="workflow-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg><span>{i:02d}</span></div><h3>{escape(title)}</h3><p>{escape(text)}</p></li>' for i, (title, text, icon) in enumerate(STEPS, 1))
    href, label = (prefix + 'kontakty/', 'Обговорити двигун ↗') if prefix else ('yak-my-pratsiuiemo/', 'Умови та деталі роботи ↗')
    return f'''<section class="section repair-workflow" id="repair-workflow"><div class="workflow-heading"><div><h2>Як відбувається<br>ремонт двигуна.</h2><p>Від першого звернення до перевірки готового двигуна — послідовність робіт залежить від його стану та узгодженого завдання.</p></div><a class="text-link" href="{href}">{label}</a></div><ol class="workflow-list">{items}</ol><p class="workflow-note">Для деяких типів двигунів стендові випробування проводять підрядники. Умови перевірки та гарантії визначають для конкретного замовлення.</p></section>'''
