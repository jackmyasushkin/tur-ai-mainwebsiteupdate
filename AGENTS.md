# Current task and precedence

The latest owner-approved homepage category is **Enterprise Process Orchestration Platform**. First read `docs/IMPLEMENTATION_HANDOFF.md`. The exact hero is locked in `content/home/decisions.md`. This is a homepage messaging decision; do not silently rewrite the separate TechCrunch positioning repository.

`HOME-003` alone has a documented, exact-value exception to legacy segment budgets. Keep original `max_chars`, IDs and raw source descriptors intact. `tools/check.py` validates it explicitly through `hero_copy_exception.py`, then validates all other fields using the frozen checker. No other exceptions are authorized.

The owner assigned implementation of the pinned edition and explicitly approved all 7 shared-definition changes across the six English pages. The run is recorded in implementation/2026-10-13-enterprise-orchestration/REPORT.md. Do not replay applied writes without a new task and live reconciliation. The owner subsequently approved issue #3: preserve Finsweet animation and format HOME-071/074/077/080 to two digits. The applied formatter is a registered script in the English Home footer only; four data-tur-number-format markers select the targets. See implementation/2026-10-13-ordinal-animation/REPORT.md. Do not disable the animation or apply the formatter globally. Never publish without separate authorization.

# Робота агентів у цьому репозиторії

The owner subsequently published the ordinal fix and confirmed it works. Current acceptance is recorded in implementation/2026-10-13-ordinal-animation-acceptance/ACCEPTANCE.md; Webflow lastPublished is 2026-10-13T05:42:48.576Z. Treat issue #3 as resolved and owner-accepted. Do not reapply the fix or treat historical unpublished snapshots as the current publication state. This acceptance does not authorize new publication, merge, or unrelated scope changes.

## Контекст

Оновлюємо контент основного сайту Tur.ai, починаючи з Home у Webflow-пісочниці. Аудиторія: бізнес-керівники, C-level та власники трансформації процесів; AI automation для B2B, зокрема регульованих галузей. Ринки: Україна, Нідерланди та США. Консультаційний продаж, конкретна цінність, підтверджені кейси; без тиску, маніпуляцій, вигаданих можливостей і джерел Gartner.

## Перед роботою

Прочитай `README.md`, `docs/NEXT_AGENT.md`, `content/home/business-brief.md`, `baseline/home/2026-10-12/00_BRIEF_FOR_AGENT.md` і `baseline/home/2026-10-12/03_FACTS_AND_DUPLICATES.md`. Інструкції користувача визначають поточний обсяг. Сам доступ до Webflow не є завданням змінювати сайт.

## Джерело та редакція

- `baseline/` — незмінний знімок. Не виправляй вихідні тексти, ліміти, контрольні суми чи докази. Нове зняття стану зберігається окремим датованим знімком у межах відповідного завдання.
- Редагуй `content/home/rewrite.json`; зберігай усі 228 ID, `original_text`, `max_chars`, порядок та джерельні поля сегментів. Не маскуй перевищення зміною ліміту.
- Чернетки нових формулювань і питання зберігай у `content/home/proposal.md`; це супровід, а `rewrite.json` — точний набір замін.
- Не змінюй класи, CSS, структуру блоків, посилання, ідентифікатори, поведінку форм або компоненти, щоб умістити текст.
- Не переписуй захищені цитати, юридичні згоди та інші `hold` поля як звичайний копірайтинг. Зміни фактів потребують конкретних доказів.
- Основна мова Home — англійська; робочі пояснення можна вести українською. Home UA — інша сторінка.
- Не додавай токени, cookies, `.env`, MCP-конфігурацію, персональні дані лідів або локальні абсолютні шляхи.

## Перевірка та статус

Запускай `python3 tools/check.py` після редагування. Перед передачею готового набору запускай `python3 tools/check.py --complete` і створи `content/home/READY_FOR_REVIEW`. Онови `content/home/STATUS.md` із фактичним станом та результатом перевірок. Незавершений набір не позначай готовим.

Розрізняй: чернетка, пройдені редакційні перевірки, схвалення текстів, внесення у пісочницю, візуальне приймання та публікація. Автоматичний тест не підтверджує факти, зміст або верстку. `layout_review` залишається `pending` на етапі підготовки текстів.

Подальші редакції оформлюй у тематичній гілці з pull request, щоб зміни було зручно переглянути. Не застосовуй force push. Внесення в Webflow виконуй лише коли це входить у поточне завдання; перед записом перевір Site ID, Page ID і актуальність джерела. **Не публікуй сайт без прямого доручення власника.**
