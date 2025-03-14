"""Creación de tablas

Revision ID: 76e00e4022b1
Revises: 
Create Date: 2025-03-09 01:46:13.920123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e00e4022b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('cantidad_disponible', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reporte',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.String(length=100), nullable=False),
    sa.Column('contenido', sa.Text(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('zona_trabajo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('rol_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('asistencia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trabajador_id', sa.Integer(), nullable=False),
    sa.Column('check_in', sa.DateTime(), nullable=False),
    sa.Column('check_out', sa.DateTime(), nullable=True),
    sa.Column('ubicacion', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['trabajador_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('solicitud_material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trabajador_id', sa.Integer(), nullable=False),
    sa.Column('material_id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('fecha_solicitud', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['material_id'], ['material.id'], ),
    sa.ForeignKeyConstraint(['trabajador_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tarea',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descripcion', sa.String(length=200), nullable=False),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('trabajador_id', sa.Integer(), nullable=False),
    sa.Column('zona_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trabajador_id'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['zona_id'], ['zona_trabajo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tarea')
    op.drop_table('solicitud_material')
    op.drop_table('asistencia')
    op.drop_table('usuarios')
    op.drop_table('zona_trabajo')
    op.drop_table('rol')
    op.drop_table('reporte')
    op.drop_table('material')
    # ### end Alembic commands ###
