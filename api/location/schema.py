from pydantic import BaseModel, Field


class AddLocationReq(BaseModel):
    district: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    city: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    province: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    postal_code: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    details: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )


class Location(BaseModel):
    id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    district: str = Field(
        strict=True, min_length=1, json_schema_extra={"format": "string"}
    )
    city: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    province: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    postal_code: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    details: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )


class AddLocationResp(BaseModel):
    message: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    data: Location = Field(strict=True)


class UpdateLocationReq(BaseModel):
    district: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    city: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    province: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    postal_code: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    details: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )


class UpdateLocationResp(BaseModel):
    message: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    data: Location | None = Field(strict=True)
