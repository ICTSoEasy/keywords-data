# Contributing to Keywords

Thank you for helping make subject vocabulary more accessible! Contributions of all sizes are welcome: fixing a typo, improving a definition, adding a keyword, translating into a new language, or starting a whole new subject.

---

## Before you start

A few principles keep the site useful for its audience (students aged 8–18, including many EAL learners):

- **Plain language.** Write definitions as if explaining to a smart 12-year-old. Avoid defining a word using harder words.
- **Short and clear.** One or two sentences is ideal. Aim for under 30 words per definition.
- **No jargon in the definition itself** unless the jargon is also defined elsewhere in the same subject.
- **Consistent tone.** Friendly and informative, not textbook-dry.

---

## How the repo works

Each subject has its own folder in `subjects/` (e.g. `subjects/maths/`). Inside it:

- `topics.json` lists the topics for that subject (e.g. Algebra, Geometry)
- `keywords/` holds one file per keyword (e.g. `subjects/maths/keywords/fraction.json`)

Two files at the top level are shared by every subject:

- `subjects.json` lists the subjects
- `ui.json` holds the language list and translated UI labels

When a pull request is opened, a GitHub Actions bot **checks every file** and reports any problems on the PR (invalid JSON, an unknown topic, a filename that doesn't match its `id`, and so on). When the PR is merged into `main`, the bot builds everything into `dist/`, which the website then fetches. **You never need to edit anything in `dist/` yourself.**

To run the same check on your own computer: `python3 scripts/bundle.py --check`

---

## Ways to contribute

### 1. Fix a typo or improve a definition

You don't need to clone anything for a small fix.

1. Browse to the file in `subjects/<subject>/keywords/` on GitHub
2. Click the **pencil icon** (✏️) in the top-right of the file view
3. Make your change
4. Scroll down and click **"Propose changes"**
5. Click **"Create pull request"**

That's it. GitHub handles the fork automatically.

---

### 2. Add a new keyword

Each keyword is a separate JSON file in its subject's `keywords/` folder. The filename must match the keyword's `id`.

**Example file: `subjects/computing/keywords/bubble_sort.json`**

```json
{
  "id": "bubble_sort",
  "topics": ["algorithms"],
  "translations": {
    "en": {
      "term": "Bubble Sort",
      "definition": "A simple sorting method that repeatedly steps through a list, compares neighbouring items, and swaps them if they are in the wrong order."
    },
    "pl": {
      "term": "Sortowanie bąbelkowe",
      "definition": "Prosta metoda sortowania, która wielokrotnie przechodzi przez listę, porównuje sąsiednie elementy i zamienia je miejscami, jeśli są w złej kolejności."
    }
  }
}
```

**Field guide:**

| Field | Description |
|---|---|
| `id` | Lowercase letters, numbers and underscores only (e.g. `bubble_sort`, not `bubble-sort`). Must match the filename without `.json`, and be unique within the subject. |
| `topics` | List of topic IDs this keyword belongs to. They must exist in **that subject's** `topics.json`. A keyword can belong to more than one topic. |
| `translations` | One entry per language. `en` is required; the others are optional. |
| `term` | The keyword as displayed on the site. |
| `definition` | Plain language, 1–2 sentences, suitable for ages 8–18. |

The same word can appear in more than one subject (e.g. "variable" in both Computing and Maths), each with a definition suited to that subject.

**Don't speak all the languages?** No problem. Add the languages you know and note in your PR that others still need translating. The site shows "translation not yet available" until someone fills them in.

**To submit:** fork the repo, create the new file, and open a pull request.

---

### 3. Add a translation for an existing keyword

Find the keyword's file and add a new language key inside `translations`:

```json
"translations": {
  "en": { "term": "Algorithm", "definition": "..." },
  "pl": { "term": "Algorytm", "definition": "..." },
  "ro": { "term": "Algoritm", "definition": "..." }
}
```

The language code must already exist in `ui.json`. If you're adding a brand-new language, see section 6.

---

### 4. Add a new topic

Edit the subject's `topics.json` and add an entry to the array:

```json
{
  "id": "new_topic",
  "icon": "🔧",
  "labels": {
    "en": "New Topic",
    "pl": "Nowy temat",
    "cy": "Pwnc Newydd",
    "ar": "موضوع جديد",
    "ro": "Subiect nou",
    "prs": "موضوع جدید",
    "ps": "نوی موضوع"
  }
}
```

Only `en` is required in `labels`, but please add every language you can. Topic colours on the site are assigned by position in the file, so add new topics **at the end** to avoid changing existing colours. There are 16 colours, after which they repeat.

---

### 5. Add a new subject

1. Add the subject to `subjects.json`:

   ```json
   {
     "id": "geography",
     "icon": "🌍",
     "draft": true,
     "names": { "en": "Geography", "pl": "Geografia", "cy": "Daearyddiaeth" }
   }
   ```

   - `id` becomes the web address (`keywords.ictsoeasy.co.uk/geography/`). Use lowercase letters, numbers and hyphens only.
   - `"draft": true` keeps the subject **off the home page** while it's being built. You can still preview it at its address. Remove the line (or set it to `false`) when it's ready to launch.
2. Create `subjects/geography/topics.json` (see section 4)
3. Add keywords to `subjects/geography/keywords/` (see section 2)

No change to the website itself is needed. New subjects appear automatically.

---

### 6. Add a new language

**Step 1: `ui.json`.** Add the language to the `languages` array, and add a full set of UI strings to `strings` (copy the `en` block and translate each value):

```json
"languages": [
  ...,
  { "code": "fr", "label": "Français", "english_label": "French" }
],
```

Right-to-left scripts (Arabic, Dari, Pashto, Urdu, Hebrew…) are detected automatically. For any other right-to-left language, add `"dir": "rtl"`.

**Step 2:** add a label for the new language to every subject in `subjects.json` and to every topic in each `subjects/*/topics.json`.

**Step 3 (optional but welcome):** add `translations` for the new language to as many keyword files as you can.

---

## Pull request checklist

Before submitting, please check:

- [ ] Every new keyword has at least an `en` translation
- [ ] The `id` matches the filename (without `.json`) and uses only lowercase letters, numbers and underscores
- [ ] `topics` values match IDs in that subject's `topics.json`
- [ ] Definitions are plain English, suitable for ages 8–18
- [ ] You have **not** edited anything in `dist/`

The bot checks most of this for you. If something is wrong, the PR shows a red ✗. Click **Details** next to it to see exactly which file and what to fix.

---

## Questions?

Open an issue and we'll help you out.
