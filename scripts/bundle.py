#!/usr/bin/env python3
"""
Validates and bundles the keyword data for keywords.ictsoeasy.co.uk.

Inputs:
  ui.json                              languages + UI strings (shared by all subjects)
  subjects.json                        list of subjects (display order = file order)
  subjects/<id>/topics.json            topics for that subject
  subjects/<id>/keywords/*.json        one file per keyword

Outputs:
  dist/subjects.json                   languages, UI strings, subject list (+ counts)
  dist/subject/<id>.json               everything one subject page needs

Usage:
  python3 scripts/bundle.py            validate, then write dist/
  python3 scripts/bundle.py --check    validate only (used on pull requests)

Exits non-zero, writing nothing, if any problem is found.
"""
import glob
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECT_ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')   # used in URLs: /computing/
KEYWORD_ID = re.compile(r'^[a-z0-9_]+$')
PRIMARY = 'en'

errors = []


def err(path, msg):
    errors.append(f'{os.path.relpath(path, ROOT)}: {msg}')


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        err(path, 'file is missing')
    except json.JSONDecodeError as e:
        err(path, f'invalid JSON — line {e.lineno}, column {e.colno}: {e.msg}')
    return None


def check_labels(path, what, labels, langs, field):
    if not isinstance(labels, dict) or not labels.get(PRIMARY):
        err(path, f'{what}: "{field}" must include "{PRIMARY}"')
        return
    for code in labels:
        if code not in langs:
            err(path, f'{what}: unknown language code "{code}" in "{field}"')


def build_subject(subject, langs):
    sid = subject['id']
    base = os.path.join(ROOT, 'subjects', sid)
    if not os.path.isdir(base):
        err(os.path.join(ROOT, 'subjects.json'), f'subject "{sid}" has no folder subjects/{sid}/')
        return None

    topics_path = os.path.join(base, 'topics.json')
    topics = load(topics_path)
    if not isinstance(topics, list):
        if topics is not None:
            err(topics_path, 'must be a JSON array of topics')
        return None
    topic_ids = set()
    for t in topics:
        tid = t.get('id') if isinstance(t, dict) else None
        if not tid or not KEYWORD_ID.match(tid):
            err(topics_path, f'topic id {tid!r} must be lowercase letters, numbers and underscores')
            continue
        if tid in topic_ids:
            err(topics_path, f'duplicate topic id "{tid}"')
        topic_ids.add(tid)
        check_labels(topics_path, f'topic "{tid}"', t.get('labels'), langs, 'labels')

    keywords, seen = [], set()
    for path in sorted(glob.glob(os.path.join(base, 'keywords', '*.json'))):
        kw = load(path)
        if not isinstance(kw, dict):
            if kw is not None:
                err(path, 'must be a JSON object')
            continue
        stem = os.path.splitext(os.path.basename(path))[0]
        kid = kw.get('id')
        if kid != stem:
            err(path, f'"id" is {kid!r} but must match the filename "{stem}"')
        elif not KEYWORD_ID.match(kid):
            err(path, f'id "{kid}" must be lowercase letters, numbers and underscores')
        if kid in seen:
            err(path, f'duplicate keyword id "{kid}"')
        seen.add(kid)

        kt = kw.get('topics')
        if not isinstance(kt, list) or not kt:
            err(path, '"topics" must be a non-empty list')
        else:
            for tid in kt:
                if tid not in topic_ids:
                    err(path, f'topic "{tid}" is not in subjects/{sid}/topics.json')

        tr = kw.get('translations')
        if not isinstance(tr, dict) or PRIMARY not in tr:
            err(path, f'"translations" must include "{PRIMARY}"')
        else:
            for code, entry in tr.items():
                if code not in langs:
                    err(path, f'unknown language code "{code}" (add it to ui.json first)')
                elif not isinstance(entry, dict) or not str(entry.get('term', '')).strip() \
                        or not str(entry.get('definition', '')).strip():
                    err(path, f'"{code}" needs both a "term" and a "definition"')
        keywords.append(kw)

    return {'topics': topics, 'keywords': keywords}


def main():
    check_only = '--check' in sys.argv

    ui = load(os.path.join(ROOT, 'ui.json'))
    subjects_path = os.path.join(ROOT, 'subjects.json')
    subjects = load(subjects_path)
    if ui is None or subjects is None:
        return report()

    langs = {l['code'] for l in ui.get('languages', [])}
    if PRIMARY not in langs:
        err(os.path.join(ROOT, 'ui.json'), f'languages must include "{PRIMARY}"')

    built, sids = {}, set()
    for s in subjects:
        sid = s.get('id', '')
        if not SUBJECT_ID.match(sid):
            err(subjects_path, f'subject id {sid!r} must be lowercase letters, numbers and hyphens')
            continue
        if sid in sids:
            err(subjects_path, f'duplicate subject id "{sid}"')
        sids.add(sid)
        check_labels(subjects_path, f'subject "{sid}"', s.get('names'), langs, 'names')
        data = build_subject(s, langs)
        if data is not None:
            built[sid] = (s, data)

    # Folders that exist but aren't listed are probably a mistake
    for d in glob.glob(os.path.join(ROOT, 'subjects', '*', '')):
        name = os.path.basename(os.path.dirname(d))
        if name not in sids:
            err(d, 'folder is not listed in subjects.json')

    if errors:
        return report()

    meta_langs = ui['languages']
    index = {
        'meta': {'version': '2.0', 'languages': meta_langs},
        'ui': ui['strings'],
        'subjects': [
            {**s, 'draft': bool(s.get('draft')),
             'keyword_count': len(d['keywords']), 'topic_count': len(d['topics'])}
            for s, d in built.values()
        ],
    }

    summary = ', '.join(f'{sid}: {len(d["keywords"])}' for sid, (_, d) in built.items())
    if check_only:
        print(f'OK — {len(built)} subjects ({summary})')
        return 0

    dist = os.path.join(ROOT, 'dist')
    out_dir = os.path.join(dist, 'subject')
    shutil.rmtree(out_dir, ignore_errors=True)   # drop bundles for removed subjects
    os.makedirs(out_dir)
    write(os.path.join(dist, 'subjects.json'), index)
    for sid, (s, d) in built.items():
        write(os.path.join(out_dir, f'{sid}.json'), {
            'meta': {'version': '2.0', 'languages': meta_langs,
                     'subject': {'id': sid, 'icon': s.get('icon', ''), 'names': s['names']}},
            'ui': ui['strings'],
            'topics': d['topics'],
            'keywords': d['keywords'],
        })
    print(f'Bundled {len(built)} subjects into dist/ ({summary})')
    return 0


def write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def report():
    print(f'Found {len(errors)} problem(s):', file=sys.stderr)
    for e in errors:
        print(f'  ✗ {e}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
