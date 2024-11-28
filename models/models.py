from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    Float,
    ARRAY,
    Index,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

from db import Base




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    img = Column(String, nullable=True)
    country = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    desc = Column(Text, nullable=True)
    is_seller = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    gigs = relationship("Gig", back_populates="user")
    seller_orders = relationship("Order", back_populates="seller", foreign_keys="Order.seller_id")
    buyer_orders = relationship("Order", back_populates="buyer", foreign_keys="Order.buyer_id")
    reviews = relationship("Review", back_populates="user")
    seller_conversations = relationship("Conversation", back_populates="seller", foreign_keys="Conversation.seller_id")
    buyer_conversations = relationship("Conversation", back_populates="buyer", foreign_keys="Conversation.buyer_id")


class Gig(Base):
    __tablename__ = "gigs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    desc = Column(Text, nullable=False)
    total_stars = Column(Integer, default=0)
    star_number = Column(Integer, default=0)
    cat = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    cover = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    short_title = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    delivery_time = Column(Integer, nullable=False)
    revision_number = Column(Integer, nullable=False)
    features = Column(ARRAY(String), nullable=False)
    sales = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="gigs")
    orders = relationship("Order", back_populates="gig")
    reviews = relationship("Review", back_populates="gig")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gig_id = Column(Integer, ForeignKey("gigs.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    img = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    payment_intent = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    gig = relationship("Gig", back_populates="orders")
    seller = relationship("User", back_populates="seller_orders", foreign_keys=[seller_id])
    buyer = relationship("User", back_populates="buyer_orders", foreign_keys=[buyer_id])


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    desc = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    read_by_seller = Column(Boolean, default=False)
    read_by_buyer = Column(Boolean, default=False)
    last_message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    messages = relationship("Message", back_populates="conversation")
    seller = relationship("User", back_populates="seller_conversations", foreign_keys=[seller_id])
    buyer = relationship("User", back_populates="buyer_conversations", foreign_keys=[buyer_id])


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gig_id = Column(Integer, ForeignKey("gigs.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    star = Column(Integer, nullable=False)
    desc = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    gig = relationship("Gig", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    # Index
    __table_args__ = (
        Index("ix_reviews_gig_user", "gig_id", "user_id"),
    )
