from pydantic import BaseModel, Field


class Owner(BaseModel):
    id: str = Field(strict=True, min_length=1, json_schema_extra={"format": "string"})
    image: str = Field(
        strict=True, min_length=1, json_schema_extra={"format": "string"}
    )
    name: str = Field(strict=True, min_length=1, json_schema_extra={"format": "string"})


class AllOwnersResp(BaseModel):
    count: int = Field(strict=True, json_schema_extra={"format": "int"})
    data: list[Owner]


class AddOwnerReq(BaseModel):
    image: str = Field(
        strict=True, min_length=1, json_schema_extra={"format": "string"}
    )
    name: str = Field(strict=True, min_length=1, json_schema_extra={"format": "string"})


class AddOwnerResp(BaseModel):
    data: Owner
