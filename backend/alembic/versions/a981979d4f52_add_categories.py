"""add categories

Revision ID: a981979d4f52
Revises: 
Create Date: 2026-11-24 14:08:33.324267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a981979d4f52'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### EDIT 1: keep the created table in a variable, so we can add rows to it! ###
    categories_table = op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

     ## EDIT 2: add the starter categories (seeding)
    op.bulk_insert(categories_table, [
        {'name': 'Hardware'},
        {'name': 'Software'},
        {'name': 'Network'},
        {'name': 'Account access'},
        {'name': 'Other'},
    ])
    op.add_column('tickets', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_tickets_category_id'), 'tickets', ['category_id'], unique=False)
    # EDIT 3: give the foreign key a NAME (was None)
    op.create_foreign_key('fk_tickets_category_id', 'tickets', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###

    # EDIT 2 (continued): give the existing tickets the "Other" category
    op.execute(
        "UPDATE tickets SET category_id = "
        "(SELECT id FROM categories WHERE name = 'Other') "
        "WHERE category_id IS NULL"
    )



def downgrade() -> None:
    """Downgrade schema."""
# EDIT 3: the same name here, so the undo knows what to remove
    op.drop_constraint('fk_tickets_category_id', 'tickets', type_='foreignkey')
    op.drop_index(op.f('ix_tickets_category_id'), table_name='tickets')
    op.drop_column('tickets', 'category_id')
    op.drop_table('categories')
    # ### end Alembic commands ###
