"""Describe your changes

Revision ID: ce6183c0e33a
Revises: 
Create Date: 2024-10-18 18:46:44.201578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce6183c0e33a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_blogs_id', table_name='blogs')
    op.drop_index('ix_blogs_title', table_name='blogs')
    op.drop_table('blogs')
    op.add_column('comments', sa.Column('is_blocked', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'is_blocked')
    op.create_table('blogs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('story', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='blogs_pkey')
    )
    op.create_index('ix_blogs_title', 'blogs', ['title'], unique=False)
    op.create_index('ix_blogs_id', 'blogs', ['id'], unique=False)
    # ### end Alembic commands ###
