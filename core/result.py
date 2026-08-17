from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolResult:
    """
    Standard result returned by every SAHVIA tool.

    success  -> True if the tool completed successfully
    message  -> Human-readable result
    data     -> Optional structured data returned by the tool
    error    -> Error description if the tool failed
    """

    success: bool
    message: str = ""
    data: Any = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, message: str = "", data: Any = None):
        """Create a successful tool result."""
        return cls(
            success=True,
            message=message,
            data=data,
            error=None
        )

    @classmethod
    def fail(cls, error: str, message: str = ""):
        """Create a failed tool result."""
        return cls(
            success=False,
            message=message,
            data=None,
            error=error
        )

    def __bool__(self):
        """Allow: if result: ..."""
        return self.success

    def __str__(self):
        """Convert the result into readable text."""
        if self.success:
            return self.message or "Action completed successfully."

        return self.error or self.message or "Action failed."


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":
    success = ToolResult.ok(
        "Chrome opened successfully."
    )

    failure = ToolResult.fail(
        "Chrome executable was not found."
    )

    print(success)
    print(success.success)

    print(failure)
    print(failure.success)