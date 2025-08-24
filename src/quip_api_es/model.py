from typing import Literal

from pydantic import BaseModel, field_validator

Categoria = Literal[
    "motivacion", "amor", "humor", "filosofia", "vida", "exito", "amistad", "educacion", "otro"
]


class Quote(BaseModel):
    texto: str
    autor: str | None = None
    categoria: Categoria | None = "otro"
    fuente_url: str | None = None
    licencia: str | None = "desconocida"

    @field_validator("texto")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("texto vacío")
        return v
