import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class SourceClass(str, enum.Enum):
    OFFICIAL = "official"      # органы власти
    OPERATOR = "operator"      # операторы инфраструктуры
    MEDIA = "media"            # верифицированные СМИ
    MONITORING = "monitoring"  # мониторинговые каналы
    
    
class CollectionMethod(str, enum.Enum):
    TG = "tg"
    RSS = "rss"
    API = "api"

class Region(str, enum.Enum):
    CRIMEA = "crimea"
    RUSSIA = "russia"
    BORDERLAND = "borderland"
    
class Source(Base):
    __tablename__ = "sources"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization: Mapped[str] = mapped_column(String(200)) 
    source_class: Mapped[SourceClass] = mapped_column(Enum(SourceClass))
    collection_method: Mapped[CollectionMethod] = mapped_column(Enum(CollectionMethod))
    address: Mapped[str] = mapped_column(String(500), unique=True)
    trust_level: Mapped[int] = mapped_column(Integer, default=5) #1-5
    default_region: Mapped[Region | None] = mapped_column(Enum(Region), nullable=True)
    categories: Mapped[list] = mapped_column(JSONB, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tg_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    
class RawMessage(Base):
    __tablename__ = "raw_messages"
    __table_args__ = (UniqueConstraint("source_id", "external_id", name="uq_source_external"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"))
    external_id: Mapped[str] = mapped_column(String(255))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    content_hash: Mapped[str] = mapped_column(String(64), index=True)           
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    media: Mapped[list] = mapped_column(JSONB, default=list)
    url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    raw_meta: Mapped[dict] = mapped_column(JSONB, default=dict)