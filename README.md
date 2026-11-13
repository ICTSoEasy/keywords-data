# Keywords Data

The keyword data behind **[keywords.ictsoeasy.co.uk](https://keywords.ictsoeasy.co.uk)**, a free, searchable reference of subject vocabulary for students aged 8–18. Every keyword is shown in English alongside a second language the student chooses.

## What this repo is

This repository holds every keyword definition shown on the website, for every subject. Anyone can suggest new keywords, fix definitions, or add translations by opening a pull request. When a PR is merged into `main`, the website updates automatically.

## How to contribute

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for full details.

The short version:
1. Fork this repo
2. Add or edit a file in `subjects/<subject>/keywords/`
3. Open a pull request. A bot checks your files and reports any problems on the PR.
4. Once it's merged, the bot rebuilds the site data and your changes go live shortly after.

> **Never edit anything in `dist/`.** It is generated automatically.

## Repository structure

```
ui.json                          ← languages + UI strings (shared by all subjects)
subjects.json                    ← list of subjects, in the order shown on the site
subjects/
  computing/
    topics.json                  ← that subject's topics, with icons and translated labels
    keywords/*.json              ← one file per keyword
  maths/
    topics.json
    keywords/*.json
dist/                            ← auto-generated, do not edit
  subjects.json
  subject/<id>.json
scripts/bundle.py                ← validates everything and builds dist/ (runs via GitHub Actions)
```

## Subjects

| Subject | Folder | URL |
|---|---|---|
| 💻 Computing | `subjects/computing/` | [/computing/](https://keywords.ictsoeasy.co.uk/computing/) |
| ➗ Maths *(in progress)* | `subjects/maths/` | [/maths/](https://keywords.ictsoeasy.co.uk/maths/) |

## Languages

| Language | Code |
|---|---|
| English | `en` |
| Polski (Polish) | `pl` |
| Cymraeg (Welsh) | `cy` |
| العربية (Arabic) | `ar` |
| Română (Romanian) | `ro` |
| دری (Dari) | `prs` |
| پښتو (Pashto) | `ps` |

Want to add a new language? See [Add a new language](CONTRIBUTING.md#6-add-a-new-language).

## License

Content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). It is free to use and share with attribution.
