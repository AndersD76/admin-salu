from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User, UserRole
from app.models.property import Property, Photo
from app.models.contact import Contact, ContactStatus
from app.models.broker import Broker
from app.models.import_log import ImportLog
from app.models.favorites import Favorite
from app.models.notification import Notification, NotificationType
from app.schemas import (
    UserResponse, UserListResponse,
    PropertyResponse, PropertyListResponse,
    ContactResponse, ContactListResponse,
    BrokerResponse, BrokerListResponse,
    ImportLogResponse, DashboardResponse,
    ContactStatusUpdate,
)
from app.core.config import settings
import uuid
from datetime import datetime
from typing import Optional

router = APIRouter()

MAX_PAGE_LIMIT = 200


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get dashboard statistics (Admin only)"""

    total_properties = db.query(Property).count()
    active_properties = db.query(Property).filter(Property.is_active == True).count()
    total_contacts = db.query(Contact).count()
    total_users = db.query(User).count()
    total_brokers = db.query(Broker).count()

    # Properties by type
    properties_by_type = db.query(
        Property.property_type,
        func.count(Property.id).label('count')
    ).group_by(Property.property_type).all()

    # Properties by purpose
    properties_by_purpose = db.query(
        Property.purpose,
        func.count(Property.id).label('count')
    ).group_by(Property.purpose).all()

    # Contacts by status
    contacts_by_status = db.query(
        Contact.status,
        func.count(Contact.id).label('count')
    ).group_by(Contact.status).all()

    # Recent contacts
    recent_contacts = db.query(Contact).order_by(
        Contact.created_at.desc()
    ).limit(10).all()

    # Top properties
    top_properties = db.query(Property).filter(
        Property.is_active == True
    ).order_by(
        Property.view_count.desc()
    ).limit(5).all()

    return {
        "overview": {
            "total_properties": total_properties,
            "active_properties": active_properties,
            "total_contacts": total_contacts,
            "total_users": total_users,
            "total_brokers": total_brokers
        },
        "properties_by_type": [
            {"type": t, "count": c} for t, c in properties_by_type
        ],
        "properties_by_purpose": [
            {"purpose": p, "count": c} for p, c in properties_by_purpose
        ],
        "contacts_by_status": [
            {"status": s.value if hasattr(s, 'value') else str(s), "count": c}
            for s, c in contacts_by_status
        ],
        "recent_contacts": recent_contacts,
        "top_properties": top_properties
    }


def notify_users_of_removed_properties(db: Session, removed_property_ids: list):
    """Notifica usuarios quando imoveis favoritos sao removidos"""
    if not removed_property_ids:
        return 0

    notifications_created = 0

    # Buscar favoritos dos imoveis removidos
    favorites = db.query(Favorite).filter(
        Favorite.property_id.in_(removed_property_ids)
    ).all()

    for favorite in favorites:
        # Buscar informacoes do imovel
        property = db.query(Property).filter(Property.id == favorite.property_id).first()
        if not property:
            continue

        # Criar notificacao
        notification = Notification(
            id=str(uuid.uuid4()),
            user_id=favorite.user_id,
            title="Imovel nao esta mais disponivel",
            message=f"O imovel '{property.title or property.property_type}' em {property.neighborhood}, {property.city} que voce favoritou nao esta mais disponivel.",
            type=NotificationType.PROPERTY_REMOVED,
            link=f"/buscar?city={property.city}&type={property.property_type}"
        )
        db.add(notification)
        notifications_created += 1

    return notifications_created


@router.get("/import-logs")
async def get_import_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get import logs (Admin only)"""

    logs = db.query(ImportLog).order_by(
        ImportLog.started_at.desc()
    ).limit(20).all()

    return {"logs": [ImportLogResponse.model_validate(log) for log in logs]}


# ===== USERS MANAGEMENT =====

@router.get("/users", response_model=UserListResponse)
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=MAX_PAGE_LIMIT),
    role: Optional[str] = None
):
    """List all users (Admin only)"""
    query = db.query(User)

    if role:
        # Validar role contra enum
        valid_roles = [r.value for r in UserRole]
        if role.upper() not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role. Valid values: {valid_roles}"
            )
        query = query.filter(User.role == role.upper())

    total = query.count()
    users = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "users": users
    }


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get user details (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# ===== PROPERTIES MANAGEMENT =====

@router.get("/properties", response_model=PropertyListResponse)
async def list_properties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=MAX_PAGE_LIMIT),
    is_active: Optional[bool] = None
):
    """List all properties (Admin only)"""
    query = db.query(Property)

    if is_active is not None:
        query = query.filter(Property.is_active == is_active)

    total = query.count()
    properties = query.order_by(Property.created_at.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "properties": properties
    }


@router.patch("/properties/{property_id}/toggle-active")
async def toggle_property_active(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Toggle property active status (Admin only)"""
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    property.is_active = not property.is_active
    db.commit()

    return {"message": f"Property {'activated' if property.is_active else 'deactivated'}", "is_active": property.is_active}


@router.patch("/properties/{property_id}/toggle-featured")
async def toggle_property_featured(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Toggle property featured status (Admin only)"""
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    property.is_featured = not property.is_featured
    db.commit()

    return {"message": f"Property {'featured' if property.is_featured else 'unfeatured'}", "is_featured": property.is_featured}


# ===== CONTACTS MANAGEMENT =====

@router.get("/contacts", response_model=ContactListResponse)
async def list_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=MAX_PAGE_LIMIT),
    status: Optional[str] = None
):
    """List all contacts (Admin only)"""
    query = db.query(Contact)

    if status:
        # Validar status contra enum
        valid_statuses = [s.value for s in ContactStatus]
        if status.upper() not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Valid values: {valid_statuses}"
            )
        query = query.filter(Contact.status == status.upper())

    total = query.count()
    contacts = query.order_by(Contact.created_at.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "contacts": contacts
    }


@router.patch("/contacts/{contact_id}/status")
async def update_contact_status(
    contact_id: str,
    body: ContactStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update contact status (Admin only)"""
    # Validar status contra enum
    valid_statuses = [s.value for s in ContactStatus]
    if body.status.upper() not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Valid values: {valid_statuses}"
        )

    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact.status = body.status.upper()
    db.commit()

    return {"message": "Contact status updated", "status": body.status.upper()}


# ===== BROKERS MANAGEMENT =====

@router.get("/brokers", response_model=BrokerListResponse)
async def list_brokers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=MAX_PAGE_LIMIT)
):
    """List all brokers (Admin only)"""
    query = db.query(Broker)

    total = query.count()
    brokers = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "brokers": brokers
    }


@router.patch("/brokers/{broker_id}/toggle-active")
async def toggle_broker_active(
    broker_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Toggle broker active status (Admin only)"""
    broker = db.query(Broker).filter(Broker.id == broker_id).first()
    if not broker:
        raise HTTPException(status_code=404, detail="Broker not found")

    broker.is_active = not broker.is_active
    db.commit()

    return {"message": f"Broker {'activated' if broker.is_active else 'deactivated'}", "is_active": broker.is_active}


# ===== CRON ENDPOINT (para Railway/schedulers externos) =====

@router.get("/cron/status")
async def cron_status(
    db: Session = Depends(get_db),
    x_cron_secret: Optional[str] = Header(None, alias="X-Cron-Secret")
):
    """
    Verifica o status da ultima sincronizacao.
    Requer X-Cron-Secret header quando CRON_SECRET esta configurado.
    """
    if not settings.CRON_SECRET:
        raise HTTPException(
            status_code=503,
            detail="Cron secret not configured"
        )

    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=401, detail="Invalid cron secret")

    last_log = db.query(ImportLog).order_by(
        ImportLog.started_at.desc()
    ).first()

    if not last_log:
        return {"status": "no_imports", "message": "Nenhuma importacao realizada ainda"}

    return {
        "status": last_log.status,
        "started_at": last_log.started_at.isoformat() if last_log.started_at else None,
        "completed_at": last_log.completed_at.isoformat() if last_log.completed_at else None,
        "properties_count": last_log.properties_count,
        "error_message": last_log.error_message
    }
