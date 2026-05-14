import math
import subprocess
from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel


class GetCurrentDateTimeArgs(BaseModel):
    format: str = "%Y-%m-%d %H:%M:%S"


class GetCurrentDateTimeCall(BaseModel):
    tool_name: Literal["get_current_datetime"]
    tool_args: GetCurrentDateTimeArgs


def get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get the current date and time.

    Args:
        format: The strftime format string. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        The current date and time as a formatted string.
    """
    return datetime.now().strftime(format)


class CalculatorArgs(BaseModel):
    operation: str
    a: int | float
    b: int | float | None = None


class CalculatorCall(BaseModel):
    tool_name: Literal["calculator"]
    tool_args: CalculatorArgs


def calculator(
    operation: str, a: Union[int, float], b: Union[int, float, None] = None
) -> Union[int, float, str]:
    """Perform an arithmetic calculation.

    Args:
        operation: The operation to perform.
            Two-operand operations: "add", "subtract", "multiply", "divide", "power", "root", "mod".
            One-operand operations: "sin", "cos", "tan" (input in radians).
        a: The first operand.
        b: The second operand. Required for two-operand operations, ignored for one-operand operations.

    Returns:
        The result of the calculation, or an error message string.
    """
    two_operand_ops = {"add", "subtract", "multiply", "divide", "power", "root", "mod"}

    if operation in two_operand_ops and b is None:
        return f"Error: Operation '{operation}' requires two operands"

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero",
        "power": lambda x, y: x**y,
        "root": lambda x, y: x ** (1 / y) if y != 0 else "Error: Cannot take 0th root",
        "mod": lambda x, y: x % y if y != 0 else "Error: Modulo by zero",
        "sin": lambda x, _: math.sin(x),
        "cos": lambda x, _: math.cos(x),
        "tan": lambda x, _: math.tan(x),
    }

    if operation not in operations:
        return f"Error: Unknown operation '{operation}'. Use: {', '.join(operations.keys())}"

    return operations[operation](a, b)


class RunTerminalCommandArgs(BaseModel):
    command: str
    timeout: int = 30


class RunTerminalCommandCall(BaseModel):
    tool_name: Literal["run_terminal_command"]
    tool_args: RunTerminalCommandArgs


def run_terminal_command(command: str, timeout: int = 30) -> str:
    """Run a shell command and return its output.

    Args:
        command: The shell command to execute.
        timeout: Seconds to wait before killing the command. Defaults to 30.

    Returns:
        The combined stdout and stderr output of the command, or an error message.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout
        if result.stderr:
            output += f"\nstderr: {result.stderr}"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {e}"
