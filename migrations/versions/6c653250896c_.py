"""empty message

Revision ID: 6c653250896c
Revises: 613e096d1e8f
Create Date: 2023-06-03 16:28:18.962070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c653250896c'
down_revision = '613e096d1e8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_joined_at'), ['joined_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_fav')
    )
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_favorite_movie_id'), ['movie_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_favorite_user_id'), ['user_id'], unique=False)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_created'), ['created'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_movie_id'), ['movie_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie')
    )
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_rating_movie_id'), ['movie_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_rating_rate'), ['rate'], unique=False)
        batch_op.create_index(batch_op.f('ix_rating_user_id'), ['user_id'], unique=False)

    op.create_table('post_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post_comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_comment_created'), ['created'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post_comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_comment_created'))

    op.drop_table('post_comment')
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_rating_user_id'))
        batch_op.drop_index(batch_op.f('ix_rating_rate'))
        batch_op.drop_index(batch_op.f('ix_rating_movie_id'))

    op.drop_table('rating')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_movie_id'))
        batch_op.drop_index(batch_op.f('ix_post_created'))

    op.drop_table('post')
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_favorite_user_id'))
        batch_op.drop_index(batch_op.f('ix_favorite_movie_id'))

    op.drop_table('favorite')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_joined_at'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
