

from pydantic import BaseModel
from typing import Optional

#basemodel type validation, parsing, and serialization for my API data

class validationgist(BaseModel):
        id: str
        description: Optional[str] = None
        url: str


        # description: str = None

# ❌ Works, but type hints are technically wrong

# Python type hint says “str” but default is None
# Tools like mypy would complain

# Optional[str] = None → correct type hint
        