-- Schema v2 — Taller Mecánico (OT extras)
-- Ejecutar contra la BD: docker exec -i tm_db psql -U tm_user -d taller_mecanico_dev -v ON_ERROR_STOP=1 -f /tmp/schema_v2.sql

ALTER TABLE orden_trabajo
  ADD COLUMN IF NOT EXISTS fecha_ingreso TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS fecha_salida TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS matricula VARCHAR(20) NULL,
  ADD COLUMN IF NOT EXISTS color VARCHAR(30) NULL,
  ADD COLUMN IF NOT EXISTS kilometraje INTEGER NULL,
  ADD COLUMN IF NOT EXISTS ingresado_en_grua BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS datos_adicionales TEXT NULL;

-- Índices opcionales
CREATE INDEX IF NOT EXISTS idx_ot_fecha_ingreso ON orden_trabajo (fecha_ingreso);
CREATE INDEX IF NOT EXISTS idx_ot_fecha_salida ON orden_trabajo (fecha_salida);