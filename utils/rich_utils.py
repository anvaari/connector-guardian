import logging
from rich.console import Console


rprint = Console(soft_wrap=True).print
class MyRichLogHandler(logging.Handler):
    LEVEL_MAPPING = {
        logging.DEBUG: "[blue]DEBUG[/blue]",
        logging.INFO: "[green]INFO[/green]",
        logging.WARNING: "[yellow]WARNING[/yellow]",
        logging.ERROR: "[red]ERROR[/red]",
        logging.CRITICAL: "[bold red]CRITICAL[/bold red]",
    }
    def emit(self, record):
        msg = self.format(record)
        rprint(msg)

    def format(self, record):
        levelname = self.LEVEL_MAPPING.get(record.levelno, str(record.levelno))
        
        file_name_line = (
            f"[link file://{record.filename}#{record.lineno}]"
            f"{record.filename}:{record.lineno}"
            f"[/link file://{record.filename}#{record.lineno}]")
        
        record.levelname = levelname
        record.filename = file_name_line
        return super().format(record)