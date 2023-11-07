"""Simple application to try and make a Textual display break."""

from dataclasses import dataclass
from itertools import cycle

from rich.segment import Segment
from rich.style import Style

from textual import on
from textual.app import App, ComposeResult
from textual.events import Click
from textual.message import Message
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Log, Tree

class TestCard(Widget, can_focus=True):

    @dataclass
    class CellPicked(Message):
        offset: int

    def on_click(self, event: Click) -> None:
        self.post_message(self.CellPicked(event.style.meta["offset"]))

    def render_line(self, y: int) -> Strip:
        lines = cycle(Tree.LINES["bold"][1:])
        return Strip(
            Segment(
                next(lines),
                style=Style(color=self.styles.color.rich_color, meta={"offset": (y * self.size.width) + char}),
            ) for char in range(self.size.width)
        )

class TestCardApp(App[None]):

    CSS = """
    TestCard {
        height: 8fr;
        color: cornflowerblue;
    }

    Screen > * {
        background: $surface;
    }

    Screen > *:focus {
        background: $surface-lighten-1;
    }
    """

    def compose(self) -> ComposeResult:
        yield TestCard()
        yield Log()

    @on(TestCard.CellPicked)
    def log_cell(self, event: TestCard.CellPicked) -> None:
        self.query_one(Log).write_line(f"{event!r}")

def run():
    TestCardApp().run()

if __name__ == "__main__":
    run()

### __main__.py ends here
