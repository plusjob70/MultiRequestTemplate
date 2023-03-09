from dataclasses import dataclass


@dataclass
class ClientRequestResult:
    success: bool
    content: bytes
