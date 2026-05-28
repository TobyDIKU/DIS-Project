from datetime import datetime
from decimal import Decimal
from typing import Optional

from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    restaurants: Mapped[list["Restaurant"]] = relationship(back_populates="category")


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price_tier: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1–3

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="restaurants")

    items: Mapped[list["Item"]] = relationship(back_populates="restaurant")
    reviews: Mapped[list["Review"]] = relationship(back_populates="restaurant")


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    reviews: Mapped[list["Review"]] = relationship(back_populates="user")


class Review(db.Model):
    __tablename__ = "review"
    __table_args__ = (UniqueConstraint("user_id", "restaurant_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"), nullable=False)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1–5
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reviews")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="reviews")


class Item(db.Model):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price_dkk: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    restaurant: Mapped["Restaurant"] = relationship(back_populates="items")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "item",
    }


class FoodItem(Item):
    __tablename__ = "food_item"

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    is_vegetarian: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_vegan: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    allergens: Mapped[Optional[str]] = mapped_column(Text)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)  # appetizer | main | dessert | side

    __mapper_args__ = {"polymorphic_identity": "food"}


class Beverage(Item):
    __tablename__ = "beverage"

    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    is_alcoholic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    volume_ml: Mapped[Optional[int]] = mapped_column(Integer)
    is_hot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __mapper_args__ = {"polymorphic_identity": "beverage"}
