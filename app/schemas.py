from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ===== User Schemas =====

class UserResponse(BaseModel):
    id: str
    name: Optional[str] = None
    email: str
    email_verified: Optional[datetime] = None
    image: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    users: List[UserResponse]


class UserDetailResponse(UserResponse):
    pass


# ===== Property Schemas =====

class PhotoResponse(BaseModel):
    id: str
    property_id: str
    file_name: str
    url: str
    is_primary: bool
    type: Optional[str] = None
    order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PropertyResponse(BaseModel):
    id: str
    external_code: str
    client_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    registration_date: Optional[datetime] = None
    last_update_date: Optional[datetime] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    condominium_name: Optional[str] = None
    property_type: str
    purpose: str
    usable_area: Optional[float] = None
    total_area: Optional[float] = None
    bedrooms: int
    suites: int
    bathrooms: int
    parking_spaces: int
    sale_price: Optional[float] = None
    rental_price: Optional[float] = None
    iptu_price: Optional[float] = None
    condominium_price: Optional[float] = None
    price_per_sqm: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None
    has_bbq: bool
    has_pool: bool
    has_sauna: bool
    has_service_area: bool
    has_balcony: bool
    has_elevator: bool
    has_security: bool
    has_gym: bool
    has_party_room: bool
    has_garden: bool
    is_active: bool
    is_featured: bool
    view_count: int
    contact_count: int
    favorite_count: int
    site_url: Optional[str] = None
    xml_source: Optional[str] = None
    broker_id: Optional[str] = None

    model_config = {"from_attributes": True}


class PropertyListResponse(BaseModel):
    total: int
    properties: List[PropertyResponse]


# ===== Contact Schemas =====

class ContactResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    property_id: str
    broker_id: Optional[str] = None
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    type: str
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContactListResponse(BaseModel):
    total: int
    contacts: List[ContactResponse]


# ===== Broker Schemas =====

class BrokerResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    external_code: Optional[str] = None
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    photo: Optional[str] = None
    creci: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    is_active: bool
    last_lead_assigned_at: Optional[datetime] = None
    lead_count: int
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    whatsapp: Optional[str] = None
    total_sales: int
    total_rentals: int
    rating: Optional[float] = None
    review_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BrokerListResponse(BaseModel):
    total: int
    brokers: List[BrokerResponse]


# ===== Import Log Schemas =====

class ImportLogResponse(BaseModel):
    id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    source: Optional[str] = None
    properties_count: int
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}


# ===== Dashboard Schemas =====

class DashboardOverview(BaseModel):
    total_properties: int
    active_properties: int
    total_contacts: int
    total_users: int
    total_brokers: int


class TypeCount(BaseModel):
    type: Optional[str] = None
    count: int


class PurposeCount(BaseModel):
    purpose: Optional[str] = None
    count: int


class StatusCount(BaseModel):
    status: str
    count: int


class DashboardResponse(BaseModel):
    overview: DashboardOverview
    properties_by_type: List[TypeCount]
    properties_by_purpose: List[PurposeCount]
    contacts_by_status: List[StatusCount]
    recent_contacts: List[ContactResponse]
    top_properties: List[PropertyResponse]


# ===== Auth Schemas =====

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MeResponse(BaseModel):
    id: str
    name: Optional[str] = None
    email: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ===== Contact Status Update =====

class ContactStatusUpdate(BaseModel):
    status: str
