"""Actualizar modelo SolicitudMaterial con ENUM estado

Revision ID: dd33f5acebff
Revises: 06000aace817
Create Date: 2025-05-10 17:16:22.209832

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = 'dd33f5acebff'
down_revision = '06000aace817'
branch_labels = None
depends_on = None

# Define el tipo ENUM
estado_enum = ENUM(
    'Pendiente', 
    'Aprobado', 
    'Rechazado', 
    'Aprobado Parcialmente', 
    name='estadoenum'
)

def upgrade():
    # Crear el tipo ENUM en la base de datos
    estado_enum.create(op.get_bind(), checkfirst=True)

    # Modificar la columna estado para usar el tipo ENUM con la cláusula USING
    with op.batch_alter_table('solicitudes_material', schema=None) as batch_op:
        batch_op.execute(
            "ALTER TABLE solicitudes_material ALTER COLUMN estado TYPE estadoenum USING estado::estadoenum"
        )

def downgrade():
    # Revertir los cambios: volver a usar VARCHAR
    with op.batch_alter_table('solicitudes_material', schema=None) as batch_op:
        batch_op.execute(
            "ALTER TABLE solicitudes_material ALTER COLUMN estado TYPE VARCHAR(50)"
        )

    # Eliminar el tipo ENUM de la base de datos
    estado_enum.drop(op.get_bind(), checkfirst=True)
