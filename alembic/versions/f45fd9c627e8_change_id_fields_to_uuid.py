"""change_id_fields_to_uuid

Revision ID: f45fd9c627e8
Revises: 9bc2e3bb6c97
Create Date: 2025-04-02 08:30:26.659718

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision: str = 'f45fd9c627e8'
down_revision: Union[str, None] = '9bc2e3bb6c97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Add a new UUID column
    op.add_column('users', sa.Column('new_id', postgresql.UUID(as_uuid=True)))
    
    # Generate UUID for each existing row
    connection = op.get_bind()
    connection.execute(sa.text(
        "UPDATE users SET new_id = uuid_generate_v4();"
    ))
    
    # Make the new column not nullable
    op.alter_column('users', 'new_id',
                    existing_type=postgresql.UUID(),
                    nullable=False)
    
    # Drop the old primary key constraint
    op.drop_constraint('users_pkey', 'users', type_='primary')
    
    # Drop the old id column
    op.drop_column('users', 'id')
    
    # Rename the new column to id
    op.alter_column('users', 'new_id',
                    new_column_name='id',
                    existing_type=postgresql.UUID(),
                    nullable=False)
    
    # Add the primary key constraint back
    op.create_primary_key('users_pkey', 'users', ['id'])
    
    # Recreate the index
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    # Add integer id column
    op.add_column('users', sa.Column('new_id', sa.Integer()))
    
    # Generate sequential IDs
    connection = op.get_bind()
    connection.execute(sa.text(
        "UPDATE users SET new_id = nextval('users_id_seq');"
    ))
    
    # Make the new column not nullable
    op.alter_column('users', 'new_id',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Drop the old primary key constraint
    op.drop_constraint('users_pkey', 'users', type_='primary')
    
    # Drop the old UUID column
    op.drop_column('users', 'id')
    
    # Rename the new column to id
    op.alter_column('users', 'new_id',
                    new_column_name='id',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Add the primary key constraint back
    op.create_primary_key('users_pkey', 'users', ['id'])
    
    # Recreate the index
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
