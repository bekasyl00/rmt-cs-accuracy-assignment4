# Что делает каждый основной файл

Для обычной проверки нужен только `python3 reproduce_all.py --verify` из корня проекта. Остальные скрипты он вызывает сам.

## Документы и проверка

| Файл | Назначение |
|---|---|
| `Assignment4_Report.docx` | Итоговый отчёт |
| `README_RU.md`, `README.md` | Быстрый старт на русском и сведения о проекте на английском |
| `reproduce_all.py` | Пересчитывает и проверяет все 22 CSV/SVG |
| `environment.txt` | Требуемая версия Python для расчётов |
| `input_manifest.json` | Контрольные суммы сохранённых исходных данных |
| `reference_outputs.json` | Контрольные суммы эталонных таблиц и графиков |
| `LICENSE` | Лицензия программного кода |

## Исходный эксперимент

| Файл | Назначение |
|---|---|
| `data/Assignment3_Main_Experiment_Data.json` | 40 вопросов, 120 исходных ответов, эталоны, оценки и ссылки на источники |
| `data/error_codes.csv` | Коды 19 ошибок исходного эксперимента |
| `analysis/original_results.py` | Создаёт пять исходных таблиц; отдельный запуск: `python3 analysis/original_results.py --verify` |
| `analysis/audit_original.py` | Независимо проверяет арифметику, сетку ответов, тесты и интервалы |
| `analysis/robustness.py` | Проверяет результаты по экосистемам и при исключении каждой экосистемы |
| `analysis/plot_original.py` | Создаёт два графика первоначального релиза |
| `analysis/plot_report.py` | Создаёт три графика для отчёта |
| `results/main_results.csv` | Основные показатели исходных трёх ИИ |
| `results/paired_topic_comparisons.csv` | Разница established/recent, парные тесты и интервалы |
| `results/sensitivity.csv` | Строгая оценка и оценка только по контрольным пунктам |
| `results/error_summary.csv`, `results/error_audit.csv` | Число ошибок по типам и все исходные ошибочные случаи |
| `diagnostics/ecosystem_results.csv` | Исходные результаты по пяти экосистемам |
| `diagnostics/leave_one_ecosystem_out.csv`, `diagnostics/robustness_summary.csv` | Исключение экосистем и сводка устойчивости |
| `audit/answer_level.csv`, `audit/matched_pairs.csv`, `audit/statistics_exact.json` | Проверяемые записи по каждому ответу, каждой паре и точные вероятности |
| `figures/`, `report_figures/` | Первоначальные и отчётные SVG-графики; различие намеренное |

## Дополнительный эксперимент

| Файл | Назначение |
|---|---|
| `supplement/raw/answers.jsonl` | Все 120 реальных новых выходов, запросы, фрагменты документов, время и токены |
| `supplement/raw/ratings.jsonl` | Все 120 оценок с тремя контрольными пунктами, объяснениями и хэшами ответов |
| `supplement/raw/model_load.json` | Время загрузки модели отдельно от времени ответа |
| `supplement/scripts/analyze_supplement.py` | Пересчитывает новые показатели из сохранённых ответов и оценок |
| `supplement/scripts/figures_supplement.py` | Строит два новых SVG-графика |
| `supplement/scripts/build_corpus.py` | Скачивает и разбивает официальную документацию; для обычной проверки не нужен |
| `supplement/scripts/run_experiment.py` | Получает новые выходы модели и поиска; не оценивает их автоматически. Для обычной проверки не нужен |
| `supplement/scripts/ANALYSIS_README.md` | Формат данных для анализа |
| `supplement/results/main_results.csv` | Новые показатели по трём условиям и двум группам тем |
| `supplement/results/paired_comparisons.csv` | Пять парных тестов, поправка Холма и интервалы |
| `supplement/results/sensitivity.csv` | Влияние штрафа за дополнительные ошибки |
| `supplement/results/efficiency.csv` | Время выполнения и количество токенов |
| `supplement/results/answer_audit.csv`, `supplement/results/error_cases.csv` | Все оценки и все 106 случаев ниже полной правильности |
| `supplement/results/retrieval_coverage.csv` | Наличие исходных reference source ID среди найденных документов |
| `supplement/figures/` | Графики новых условий |
| `supplement/corpus/manifest.json` | 56 источников, результаты скачивания и хэши |
| `supplement/corpus/chunks.json` | Замороженные фрагменты документов; входит в полный ZIP для нового запуска |
| `supplement/protocol/PROTOCOL.md` | Полный протокол дополнительного этапа |
| `supplement/protocol/questions_only.json` | Вопросы без эталонных ответов для генератора |
| `supplement/protocol/freeze_manifest.json`, `history/` | Контрольные суммы и история изменения плана до запусков |
| `supplement/protocol/model_snapshot.json`, `host.json`, `requirements-generation.txt` | Модель, компьютер и точные зависимости нового запуска |
| `supplement/protocol/submission_status.json` | Фактический статус предварительной подачи протокола |
| `supplement/experiment_integrity.json` | Проверка последовательности фиксации протокола и получения выходов |

## Пояснения и история

| Файл или папка | Назначение |
|---|---|
| `docs/defence_notes_ru.md` | Объяснения расчётов и новых сравнений для защиты |
| `docs/reproduction_record.json`, `docs/reproduction_record.md` | Фактическая запись запуска проверки Бекасылом |
| `docs/fresh_generation.md` | Необязательный повторный запуск модели на Apple Silicon |
| `docs/contributions.md` | Распределение ответственности команды и сведения об AI assistance |
| `logs/` | Журналы первоначальной, подготовительной и полной программной проверки |
| `archive/README_original_release.md` | Историческая инструкция; имена файлов в ней относятся к прежнему релизу |
| `reproduced/` | Автоматически пересоздаваемые результаты проверки; это не новые исходные ответы |

Имена людей сохраняются внутри авторства и фактических записей действий. Рабочие названия файлов описывают назначение, а не единственного автора.
