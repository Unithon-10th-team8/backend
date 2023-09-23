"""empty message

Revision ID: 0c28d35b2aa8
Revises: 3b7d061f4b5c
Create Date: 2023-09-23 22:52:46.655522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c28d35b2aa8"
down_revision: Union[str, None] = "3b7d061f4b5c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("profile_image_url", sa.Text(), nullable=True))
    op.add_column(
        "user",
        sa.Column("google_access_token", sa.Text(), server_default="", nullable=False),
    )
    op.add_column(
        "user",
        sa.Column("google_refresh_token", sa.Text(), server_default="", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "google_refresh_token")
    op.drop_column("user", "google_access_token")
    op.drop_column("user", "profile_image_url")
    # ### end Alembic commands ###