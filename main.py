from abc import ABC, abstractmethod

from colorama import Fore, Style, init as colorama_init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.operations import OperationFactory

colorama_init(autoreset=True)


def ok(m): return f"{Fore.GREEN}{m}{Style.RESET_ALL}"
def err(m): return f"{Fore.RED}{m}{Style.RESET_ALL}"
def info(m): return f"{Fore.CYAN}{m}{Style.RESET_ALL}"


def register_help(desc):
    def wrap(func):
        func.help_text = desc
        return func
    return wrap


class Command(ABC):
    @abstractmethod
    def execute(self, args):
        raise NotImplementedError


class ArithmeticCommand(Command):
    def __init__(self, calc, op):
        self.calc, self.op = calc, op

    def execute(self, args):
        if len(args) != 2:
            return err(f"'{self.op}' requires exactly two numbers.")
        try:
            return ok(f"Result: {self.calc.perform_operation(self.op, args[0], args[1])}")
        except (ValidationError, OperationError) as e:
            return err(f"Error: {e}")


class CalculatorREPL:
    def __init__(self, calc=None):
        self.calc = calc or Calculator()
        self.running = True
        self.commands = {op: ArithmeticCommand(self.calc, op)
                         for op in OperationFactory.available_operations()}

    @register_help("Display calculation history")
    def cmd_history(self, args):
        h = self.calc.get_history()
        return info("History is empty.") if not h else "\n".join(f"{i+1}. {c}" for i, c in enumerate(h))

    @register_help("Clear calculation history")
    def cmd_clear(self, args):
        self.calc.clear_history()
        return ok("History cleared.")

    @register_help("Undo the last calculation")
    def cmd_undo(self, args):
        return ok("Undo successful.") if self.calc.undo() else info("Nothing to undo.")

    @register_help("Redo the last undone calculation")
    def cmd_redo(self, args):
        return ok("Redo successful.") if self.calc.redo() else info("Nothing to redo.")

    @register_help("Save history to CSV")
    def cmd_save(self, args):
        try:
            self.calc.save_history()
            return ok("History saved.")
        except OperationError as e:
            return err(str(e))

    @register_help("Load history from CSV")
    def cmd_load(self, args):
        try:
            self.calc.load_history()
            return ok("History loaded.")
        except OperationError as e:
            return err(str(e))

    @register_help("Display available commands")
    def cmd_help(self, args):
        return self.build_help()

    @register_help("Exit the application")
    def cmd_exit(self, args):
        self.running = False
        return info("Goodbye!")

    def build_help(self):
        lines = [info("Available commands:")]
        for op in OperationFactory.available_operations():
            lines.append(f"  {op} <a> <b>  - Perform {op}")
        for name, h in self._meta().items():
            lines.append(f"  {name:<12} - {h.help_text}")
        return "\n".join(lines)

    def _meta(self):
        return {"history": self.cmd_history, "clear": self.cmd_clear,
                "undo": self.cmd_undo, "redo": self.cmd_redo,
                "save": self.cmd_save, "load": self.cmd_load,
                "help": self.cmd_help, "exit": self.cmd_exit}

    def evaluate(self, line):
        parts = line.strip().split()
        if not parts:
            return ""
        cmd, args = parts[0].lower(), parts[1:]
        if cmd in self.commands:
            return self.commands[cmd].execute(args)
        if cmd in self._meta():
            return self._meta()[cmd](args)
        return err(f"Unknown command: '{cmd}'. Type 'help'.")

    def run(self):
        print(info("Enhanced Calculator. Type 'help'."))
        while self.running:
            try:
                line = input(Fore.YELLOW + "calc> " + Style.RESET_ALL)
            except (EOFError, KeyboardInterrupt):
                print("\n" + info("Goodbye!"))
                break
            out = self.evaluate(line)
            if out:
                print(out)


if __name__ == "__main__":
    CalculatorREPL().run()
