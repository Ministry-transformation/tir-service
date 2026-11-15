const input = document.querySelector('#engine-search');
const engines = [...document.querySelectorAll('#engine-list span')];
const empty = document.querySelector('#no-results');
const normalize = value => value.toLocaleLowerCase('uk').replace(/[\s\-–—]/g, '');
if (input && empty) input.addEventListener('input', () => {
  const query = normalize(input.value);
  let visible = 0;
  engines.forEach(engine => {
    const match = normalize(engine.textContent).includes(query);
    engine.hidden = !match;
    if (match) visible++;
  });
  empty.hidden = visible > 0;
});

const form = document.querySelector('#request-form');
if (form) {
  const params = new URLSearchParams(location.search);
  if (location.hash === '#parts' || params.get('type') === 'parts') document.querySelector('#request-type').value = 'Підбір деталі';
  if (params.has('engine')) document.querySelector('#request-engine').value = params.get('engine').slice(0, 100);
  if (params.has('item')) document.querySelector('#request-description').value = 'Потрібна деталь: ' + params.get('item').slice(0, 200);
  form.addEventListener('submit', event => {
    event.preventDefault();
    const type = document.querySelector('#request-type').value;
    const model = document.querySelector('#request-engine').value.trim();
    const details = document.querySelector('#request-description').value.trim();
    if (!model || !details) return;
    document.querySelector('#request-text').value = `Вітаю! ${type}.\nДвигун: ${model}\nЗапит: ${details}`;
    document.querySelector('#request-result').hidden = false;
    document.querySelector('#copy-status').textContent = '';
  });
  document.querySelector('#copy-request').addEventListener('click', async () => {
    const field = document.querySelector('#request-text');
    const status = document.querySelector('#copy-status');
    try {
      await navigator.clipboard.writeText(field.value);
      status.textContent = 'Текст скопійовано. Заявку не надіслано.';
    } catch {
      field.focus();
      field.select();
      status.textContent = 'Не вдалося скопіювати автоматично. Скопіюйте виділений текст вручну.';
    }
  });
}

// Local callback mockup: no personal data is sent or persisted.
function setupCallbackForm(form) {
  form.addEventListener('submit', event => {
    event.preventDefault();
    const name = form.elements.name.value.trim();
    const phone = form.elements.phone.value.trim();
    const digits = phone.replace(/\D/g, '');
    if (digits.length < 9 || digits.length > 15) {
      form.elements.phone.setCustomValidity('Вкажіть номер телефону з 9–15 цифр.');
      form.elements.phone.reportValidity();
      return;
    }
    form.elements.phone.setCustomValidity('');
    const result = form.querySelector('.callback-result');
    result.querySelector('textarea').value = `Вітаю! Мене звати ${name}. Прошу консультацію щодо ремонту двигуна. Телефон: ${phone}`;
    result.hidden = false;
    result.querySelector('[role="status"]').textContent = 'Звернення підготовлено, але ще не надіслано.';
  });
  form.elements.phone.addEventListener('input', () => form.elements.phone.setCustomValidity(''));
  form.querySelector('[data-copy-callback]').addEventListener('click', async () => {
    const field = form.querySelector('.callback-result textarea');
    const status = form.querySelector('.callback-result [role="status"]');
    try { await navigator.clipboard.writeText(field.value); status.textContent = 'Текст скопійовано. Заявку не надіслано.'; }
    catch { field.focus(); field.select(); status.textContent = 'Скопіюйте виділений текст вручну.'; }
  });
}
document.querySelectorAll('[data-callback-form]').forEach(setupCallbackForm);

const popup = document.createElement('dialog');
popup.className = 'callback-dialog';
popup.setAttribute('aria-labelledby', 'callback-title');
popup.innerHTML = `<div class="callback-dialog-inner"><button type="button" class="callback-close" aria-label="Закрити">×</button><h2 id="callback-title">Потрібна консультація?</h2><p class="callback-dialog-intro">Вітаємо! Допоможемо обговорити ремонт вашого двигуна. Залиште ім’я та номер телефону.</p><form data-callback-form><label>Ваше ім’я<input name="name" autocomplete="name" maxlength="100" required placeholder="Як до вас звертатися"></label><label>Номер телефону<input name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="25" required placeholder="+380"></label><button class="button" type="submit">Підготувати звернення <span aria-hidden="true">↗</span></button><p class="callback-note">Локальний макет: заявка не надсилається. Текст можна скопіювати.</p><div class="callback-result" hidden><label>Текст звернення<textarea rows="3" readonly></textarea></label><button class="outline-button" type="button" data-copy-callback>Скопіювати текст</button><p role="status"></p></div></form></div>`;
document.body.append(popup);
setupCallbackForm(popup.querySelector('form'));
popup.querySelector('.callback-close').addEventListener('click', () => popup.close());
popup.addEventListener('click', event => { if (event.target === popup) popup.close(); });
try {
  const firstVisit = Number(sessionStorage.getItem('tirVisitStart')) || Date.now();
  sessionStorage.setItem('tirVisitStart', String(firstVisit));
  if (!sessionStorage.getItem('tirPopupShown')) {
    let ready = false;
    const showWhenAppropriate = () => {
      if (!ready || document.hidden || document.activeElement?.closest('form')) return;
      if (typeof popup.showModal === 'function' && !popup.open && !sessionStorage.getItem('tirPopupShown')) {
        popup.showModal();
        sessionStorage.setItem('tirPopupShown', '1');
      }
    };
    setTimeout(() => { ready = true; showWhenAppropriate(); }, Math.max(0, 50000 - (Date.now() - firstVisit)));
    document.addEventListener('visibilitychange', showWhenAppropriate);
    document.addEventListener('focusout', () => setTimeout(showWhenAppropriate, 0));
    document.querySelectorAll('form').forEach(existingForm => existingForm.addEventListener('submit', () => {
      if (existingForm !== popup.querySelector('form')) sessionStorage.setItem('tirPopupShown', '1');
    }));
  }
} catch { /* Storage unavailable: keep browsing and the inline form functional. */ }
