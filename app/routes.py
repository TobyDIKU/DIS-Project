from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Beverage, Category, FoodItem, Restaurant, Review

main_bp = Blueprint("main", __name__)

MEAL_ORDER = ["appetizer", "main", "side", "dessert"]


@main_bp.get("/")
def index():
    categories = db.session.execute(
        db.select(Category).order_by(Category.name)
    ).scalars().all()

    category_id = request.args.get("category", type=int)

    avg_sub = (
        db.select(
            Review.restaurant_id,
            func.round(func.avg(Review.rating), 1).label("avg_rating"),
            func.count(Review.id).label("review_count"),
        )
        .group_by(Review.restaurant_id)
        .subquery()
    )

    query = (
        db.select(Restaurant, avg_sub.c.avg_rating, avg_sub.c.review_count)
        .outerjoin(avg_sub, Restaurant.id == avg_sub.c.restaurant_id)
        .order_by(Restaurant.name)
    )

    if category_id:
        query = query.where(Restaurant.category_id == category_id)

    results = db.session.execute(query).all()

    return render_template(
        "index.html",
        results=results,
        categories=categories,
        active_category=category_id,
    )


@main_bp.get("/restaurants/<int:id>")
def restaurant(id):
    r = db.session.get(Restaurant, id)
    if r is None:
        abort(404)

    food_items = db.session.execute(
        db.select(FoodItem)
        .where(FoodItem.restaurant_id == id)
        .order_by(FoodItem.meal_type, FoodItem.name)
    ).scalars().all()

    beverages = db.session.execute(
        db.select(Beverage)
        .where(Beverage.restaurant_id == id)
        .order_by(Beverage.name)
    ).scalars().all()

    reviews = db.session.execute(
        db.select(Review)
        .where(Review.restaurant_id == id)
        .order_by(Review.created_at.desc())
    ).scalars().all()

    food_by_type = {}
    for item in food_items:
        food_by_type.setdefault(item.meal_type, []).append(item)
    food_groups = [(t, food_by_type[t]) for t in MEAL_ORDER if t in food_by_type]

    avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else None

    return render_template(
        "restaurant.html",
        restaurant=r,
        food_groups=food_groups,
        beverages=beverages,
        reviews=reviews,
        avg_rating=avg_rating,
    )


@main_bp.post("/restaurants/<int:id>/reviews")
@login_required
def post_review(id):
    r = db.session.get(Restaurant, id)
    if r is None:
        abort(404)

    try:
        rating = int(request.form["rating"])
        assert 1 <= rating <= 5
    except (ValueError, KeyError, AssertionError):
        flash("Rating must be a number between 1 and 5.", "error")
        return redirect(url_for("main.restaurant", id=id))

    comment = request.form.get("comment", "").strip() or None

    db.session.add(Review(
        user_id=current_user.id,
        restaurant_id=id,
        rating=rating,
        comment=comment,
    ))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("You have already reviewed this restaurant.", "error")

    return redirect(url_for("main.restaurant", id=id))
