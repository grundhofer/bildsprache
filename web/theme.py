"""Gemeinsames Seitentheme (System / Hell / Dunkel), übernommen aus Designsprache.

Die Bilder behalten ihre eigenen Farben; das Theme betrifft nur die Seite drumherum.
Kontraste prüft tests/test_theme.py.
"""
from pathlib import Path

PALETTES = {
    'light': {
        'ground':'#ECE9E2', 'surface':'#F7F5F0', 'surface-2':'#FDFCF9',
        'ink':'#1B1A17', 'ink-2':'#524E47', 'ink-3':'#5A554D',
        'rule':'#C9C3B7', 'rule-soft':'#DFDAD0',
        'accent':'#8A3324', 'accent-ink':'#FDFCF9', 'accent-soft':'#F0DCD4', 'brass':'#7A5C22',
        'tag-style':'#F3DED6', 'tag-motif':'#E4E1DA', 'tag-guard':'#EDE3C9',
    },
    'dark': {
        'ground':'#1D1B18', 'surface':'#292622', 'surface-2':'#34302B',
        'ink':'#F2EFE9', 'ink-2':'#C8C1B5', 'ink-3':'#B5AC9F',
        'rule':'#6B6358', 'rule-soft':'#47413A',
        'accent':'#F0A28C', 'accent-ink':'#2A130D', 'accent-soft':'#4B2B22', 'brass':'#D8BB82',
        'tag-style':'#4B2B22', 'tag-motif':'#3A3631', 'tag-guard':'#463D27',
    },
}


def css():
    def values(mode):
        shadow = ('0 1px 2px rgba(27,26,23,.06), 0 10px 28px -14px rgba(27,26,23,.22)'
                  if mode == 'light' else '0 1px 2px rgba(0,0,0,.3), 0 12px 32px -14px rgba(0,0,0,.5)')
        return ''.join('--'+key+':'+value+';' for key, value in PALETTES[mode].items())+'--shadow:'+shadow+';color-scheme:'+mode+';'
    return (':root {'+values('light')+'}\n'
            '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {'+values('dark')+'} }\n'
            ':root[data-theme="dark"] {'+values('dark')+'}\n')


def script():
    return '<script id="theme-controller">\n'+(Path(__file__).parent/'theme.js').read_text()+'\n</script>\n'


def controls(lang):
    labels = {'de': ('System', 'Hell', 'Dunkel'), 'en': ('System', 'Light', 'Dark')}[lang]
    title = {'de': 'Darstellung', 'en': 'Appearance'}[lang]
    buttons = ''.join(f'<button type="button" data-theme-choice="{mode}" aria-pressed="false">{labels[i]}</button>'
                      for i, mode in enumerate(('system', 'light', 'dark')))
    return f'<div class="theme-switch" data-theme-controls role="group" aria-label="{title}" hidden>{buttons}</div>'
