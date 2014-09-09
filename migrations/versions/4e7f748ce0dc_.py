"""empty message

Revision ID: 4e7f748ce0dc
Revises: None
Create Date: 2014-09-06 11:31:30.684115

"""

# revision identifiers, used by Alembic.
revision = '4e7f748ce0dc'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_number', sa.String(length=64), nullable=False),
    sa.Column('application_type', sa.String(length=50), nullable=False),
    sa.Column('detail', postgresql.JSON(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('work_queue', sa.String(length=100), nullable=False),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.Column('submitted_by', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cases')
    ### end Alembic commands ###