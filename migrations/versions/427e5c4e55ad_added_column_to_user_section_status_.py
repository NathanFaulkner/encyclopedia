"""Added column to User Section Status model for last grade before decay

Revision ID: 427e5c4e55ad
Revises: e34e4b37506f
Create Date: 2020-12-06 09:34:46.522132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427e5c4e55ad'
down_revision = 'e34e4b37506f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_section_status', sa.Column('grade_after_last_user_attempt', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_section_status', 'grade_after_last_user_attempt')
    # ### end Alembic commands ###