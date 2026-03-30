"""initial

Revision ID: b5fd561af392
Revises:
Create Date: 2026-03-23 14:23:31.808743

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b5fd561af392'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('google_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_id')
    )
    op.create_table('plans',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('user_id', sa.String(36), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('user_id', sa.String(36), nullable=False),
    sa.Column('career_goal', sa.String(), nullable=True),
    sa.Column('skills', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('rejections',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('user_id', sa.String(36), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('action_title', sa.String(), nullable=False),
    sa.Column('rejected_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('actions',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('plan_id', sa.String(36), nullable=False),
    sa.Column('priority', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('objective', sa.String(), nullable=False),
    sa.Column('context', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('sequence', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('educations',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('profile_id', sa.String(36), nullable=False),
    sa.Column('institution', sa.String(), nullable=False),
    sa.Column('level', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('study_area', sa.String(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('experiences',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('profile_id', sa.String(36), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('seniority', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gaps',
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('plan_id', sa.String(36), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('relevance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('gaps')
    op.drop_table('experiences')
    op.drop_table('educations')
    op.drop_table('actions')
    op.drop_table('rejections')
    op.drop_table('profiles')
    op.drop_table('plans')
    op.drop_table('users')
