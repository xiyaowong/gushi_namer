try:
    from .namer import (
        BOOK_CHUCI,
        BOOK_CIFU,
        BOOK_GUSHI,
        BOOK_SHIJING,
        BOOK_SONGCI,
        BOOK_TANGSHI,
        BOOK_YUEFU,
        Namer
    )
except Exception:
    from namer import (  # type: ignore
        Namer,
        BOOK_CHUCI,
        BOOK_CIFU,
        BOOK_GUSHI,
        BOOK_SHIJING,
        BOOK_SONGCI,
        BOOK_TANGSHI,
        BOOK_YUEFU,
    )

from bullet import Bullet, Numbers, VerticalPrompt
from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel


def render(items: list):
    rprint(Columns([Panel(item) for item in items]))


prompt = VerticalPrompt(
    [
        Numbers('生成多少个？'),
        Bullet(
            "选择什么文集？",
            choices=['楚辞', '辞赋', '古诗', '诗经', '宋词', '唐诗', '乐府'],
        ),
    ]
)
result = prompt.launch()
count = result[0][1]
book = result[1][1]

namer = Namer(
    {
        '楚辞': BOOK_CHUCI,
        '辞赋': BOOK_CIFU,
        '古诗': BOOK_GUSHI,
        '诗经': BOOK_SHIJING,
        '宋词': BOOK_SONGCI,
        '唐诗': BOOK_TANGSHI,
        '乐府': BOOK_YUEFU,
    }[book]
)


names = []

for _ in range(int(count)):
    name = namer.genarate()
    if not name:
        continue
    for s in name.name:
        name.sentence = name.sentence.replace(s, f'[bold blue]{s}[/bold blue]')
    names.append(
        '[cyan]{}[/cyan]  「 {}」\n《{} • {}》 ----- 【{}】{}'.format(
            name.name, name.sentence, name.book, name.title, name.dynasty, name.author
        )
    )

render(names)
