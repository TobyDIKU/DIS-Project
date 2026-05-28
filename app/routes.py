from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, nullslast
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Beverage, Category, FoodItem, Item, Restaurant, Review

main_bp = Blueprint("main", __name__)

MEAL_ORDER = ["appetizer", "main", "side", "dessert"]
REVIEW_PERIODS = {"month": 30, "6months": 180, "year": 365}
DRINK_PRICE_THRESHOLDS = [30, 40, 50]


@main_bp.get("/")
def index():
    categories = db.session.execute(
        db.select(Category).order_by(Category.name)
    ).scalars().all()

    raw_categories = request.args.getlist("category", type=int)
    active_categories = {c for c in raw_categories if c > 0}
    raw_max_drink = request.args.get("max_drink", type=int)
    max_drink_price = raw_max_drink if raw_max_drink in DRINK_PRICE_THRESHOLDS else None
    active_sort = request.args.get("sort") if request.args.get("sort") in ("rating_desc", "rating_asc") else None

    avg_sub = (
        db.select(
            Review.restaurant_id,
            func.round(func.avg(Review.rating), 1).label("avg_rating"),
            func.count(Review.id).label("review_count"),
        )
        .group_by(Review.restaurant_id)
        .subquery()
    )

    min_drink_sub = (
        db.select(
            Item.restaurant_id,
            func.min(Item.price_dkk).label("min_drink_price"),
        )
        .join(Beverage, Item.id == Beverage.id)
        .where(Beverage.is_alcoholic == True)
        .group_by(Item.restaurant_id)
        .subquery()
    )

    query = (
        db.select(
            Restaurant,
            avg_sub.c.avg_rating,
            avg_sub.c.review_count,
            min_drink_sub.c.min_drink_price,
        )
        .outerjoin(avg_sub, Restaurant.id == avg_sub.c.restaurant_id)
        .outerjoin(min_drink_sub, Restaurant.id == min_drink_sub.c.restaurant_id)
    )

    if active_sort == "rating_desc":
        query = query.order_by(nullslast(avg_sub.c.avg_rating.desc()))
    elif active_sort == "rating_asc":
        query = query.order_by(nullslast(avg_sub.c.avg_rating.asc()))
    else:
        query = query.order_by(Restaurant.name)

    if active_categories:
        query = query.where(Restaurant.category_id.in_(active_categories))

    if max_drink_price:
        query = query.where(min_drink_sub.c.min_drink_price <= max_drink_price)

    results = db.session.execute(query).all()

    return render_template(
        "index.html",
        results=results,
        categories=categories,
        active_categories=active_categories,
        max_drink_price=max_drink_price,
        drink_thresholds=DRINK_PRICE_THRESHOLDS,
        active_sort=active_sort,
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

    # Parse filters
    raw_ratings = request.args.getlist("rating", type=int)
    active_ratings = {n for n in raw_ratings if 1 <= n <= 5}
    active_period = request.args.get("period") if request.args.get("period") in REVIEW_PERIODS else None

    base_reviews_query = (
        db.select(Review)
        .where(Review.restaurant_id == id)
        .order_by(Review.created_at.desc())
    )

    all_reviews = db.session.execute(base_reviews_query).scalars().all()

    filtered_query = base_reviews_query
    if active_ratings:
        filtered_query = filtered_query.where(Review.rating.in_(active_ratings))
    if active_period:
        cutoff = datetime.utcnow() - timedelta(days=REVIEW_PERIODS[active_period])
        filtered_query = filtered_query.where(Review.created_at >= cutoff)

    reviews = db.session.execute(filtered_query).scalars().all()

    food_by_type = {}
    for item in food_items:
        food_by_type.setdefault(item.meal_type, []).append(item)
    food_groups = [(t, food_by_type[t]) for t in MEAL_ORDER if t in food_by_type]

    avg_rating = round(sum(rv.rating for rv in all_reviews) / len(all_reviews), 1) if all_reviews else None

    return render_template(
        "restaurant.html",
        restaurant=r,
        food_groups=food_groups,
        beverages=beverages,
        reviews=reviews,
        avg_rating=avg_rating,
        total_review_count=len(all_reviews),
        active_ratings=active_ratings,
        active_period=active_period,
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
