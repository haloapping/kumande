from pydantic import BaseModel, Field


class Food(BaseModel):
    user_id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    owner_id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    location_id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    image: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    name: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    description: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    price: int = Field(
        strict=True,
        json_schema_extra={"format": "int"},
    )
    review: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )


class AllFoodsResp(BaseModel):
    count: int = Field(
        strict=True,
        json_schema_extra={
            "format": "int",
        },
    )
    data: list[Food]


class AddFoodReq(BaseModel):
    owner_id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    location_id: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    image: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    name: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    description: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    price: int = Field(
        strict=True,
        json_schema_extra={"format": "int"},
    )
    review: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )


class AddFoodResp(BaseModel):
    message: str = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    data: Food


class UpdateFoodReq(BaseModel):
    user_id: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    owner_id: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    location_id: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    image: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    name: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    description: str | None = Field(
        strict=True,
        min_length=1,
        json_schema_extra={
            "format": "string",
        },
    )
    price: int | None = Field(
        default=None,
        strict=True,
        json_schema_extra={"format": "int"},
    )
    review: str | None = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )


class UpdateFoodResp(BaseModel):
    message: str = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    data: Food


class DeleteFoodResp(BaseModel):
    message: str = Field(
        default=None,
        strict=True,
        min_length=1,
        json_schema_extra={"format": "string"},
    )
    data: Food
