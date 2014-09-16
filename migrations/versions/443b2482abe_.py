"""empty message

Revision ID: 443b2482abe
Revises: 309c10f553c2
Create Date: 2014-09-12 16:27:58.939236

"""

# revision identifiers, used by Alembic.
revision = '443b2482abe'
down_revision = '309c10f553c2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cases', 'title')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cases', sa.Column('title', sa.TEXT(), autoincrement=False, nullable=True))
    ### end Alembic commands ###