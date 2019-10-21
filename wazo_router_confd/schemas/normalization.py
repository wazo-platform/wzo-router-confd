# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class NormalizationProfile(BaseModel):
    id: int
    tenant_id: int
    name: constr(max_length=256)  # type: ignore
    country_code: Optional[constr(max_length=64)]  # type: ignore
    area_code: Optional[constr(max_length=64)]  # type: ignore
    intl_prefix: Optional[constr(max_length=64)]  # type: ignore
    ld_prefix: Optional[constr(max_length=64)]  # type: ignore
    always_ld: bool = False

    class Config:
        orm_mode = True


class NormalizationProfileCreate(BaseModel):
    tenant_id: int
    name: constr(max_length=256)  # type: ignore
    country_code: Optional[constr(max_length=64)]  # type: ignore
    area_code: Optional[constr(max_length=64)]  # type: ignore
    intl_prefix: Optional[constr(max_length=64)]  # type: ignore
    ld_prefix: Optional[constr(max_length=64)]  # type: ignore
    always_ld: bool = False


class NormalizationProfileUpdate(BaseModel):
    tenant_id: int
    name: constr(max_length=256)  # type: ignore
    country_code: Optional[constr(max_length=64)]  # type: ignore
    area_code: Optional[constr(max_length=64)]  # type: ignore
    intl_prefix: Optional[constr(max_length=64)]  # type: ignore
    ld_prefix: Optional[constr(max_length=64)]  # type: ignore
    always_ld: bool = False


class NormalizationRule(BaseModel):
    id: int
    profile_id: int
    match_regex: constr(max_length=256)  # type: ignore
    replace_regex: constr(max_length=256)  # type: ignore

    class Config:
        orm_mode = True


class NormalizationRuleCreate(BaseModel):
    profile_id: int
    match_regex: constr(max_length=256)  # type: ignore
    replace_regex: constr(max_length=256)  # type: ignore


class NormalizationRuleUpdate(BaseModel):
    profile_id: int
    match_regex: constr(max_length=256)  # type: ignore
    replace_regex: constr(max_length=256)  # type: ignore