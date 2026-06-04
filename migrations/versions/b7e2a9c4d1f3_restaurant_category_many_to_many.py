"""restaurant category many-to-many

Revision ID: b7e2a9c4d1f3
Revises: 293f0af1fea2
Create Date: 2026-06-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e2a9c4d1f3'
down_revision = '293f0af1fea2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'restaurant_category',
        sa.Column('restaurant_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('restaurant_id', 'category_id'),
    )
    # Preserve existing single-category assignments before dropping the column.
    op.execute(
        "INSERT INTO restaurant_category (restaurant_id, category_id) "
        "SELECT id, category_id FROM restaurant"
    )
    op.drop_column('restaurant', 'category_id')


def downgrade():
    # Best-effort reversal: a multi-category restaurant collapses to one category.
    op.add_column('restaurant', sa.Column('category_id', sa.Integer(), nullable=True))
    op.execute(
        "UPDATE restaurant SET category_id = ("
        "SELECT MIN(category_id) FROM restaurant_category rc "
        "WHERE rc.restaurant_id = restaurant.id)"
    )
    op.alter_column('restaurant', 'category_id', nullable=False)
    op.create_foreign_key(
        'restaurant_category_id_fkey', 'restaurant', 'category', ['category_id'], ['id']
    )
    op.drop_table('restaurant_category')
