"""add_comments

Revision ID: 7c9b0f1a2d34
Revises: d673870a3ced
Create Date: 2026-03-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c9b0f1a2d34"
down_revision: Union[str, Sequence[str], None] = "d673870a3ced"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.create_table(
    "comments",
    sa.Column("user_id", sa.Uuid(), nullable=False),
    sa.Column("task_id", sa.Uuid(), nullable=False),
    sa.Column("content", sa.String(), nullable=False),
    sa.Column("parent_id", sa.Uuid(), nullable=True),
    sa.Column("id", sa.Uuid(), nullable=False),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    sa.ForeignKeyConstraint(["parent_id"], ["comments.id"]),
    sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
  op.create_index(op.f("ix_comments_task_id"), "comments", ["task_id"], unique=False)
  op.create_index(op.f("ix_comments_user_id"), "comments", ["user_id"], unique=False)


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_index(op.f("ix_comments_user_id"), table_name="comments")
  op.drop_index(op.f("ix_comments_task_id"), table_name="comments")
  op.drop_index(op.f("ix_comments_id"), table_name="comments")
  op.drop_table("comments")
