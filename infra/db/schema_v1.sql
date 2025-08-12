-- Schema v1 — Taller Mecánico (PostgreSQL 16)
-- Encoding/zone
SET client_encoding = 'UTF8';
SET timezone = 'UTC';
SET lock_timeout = '5s';
SET idle_in_transaction_session_timeout = '30s';

-- Usuarios/Roles/Permisos
CREATE TABLE IF NOT EXISTS app_user (
  user_id BIGSERIAL PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(254) UNIQUE NOT NULL,
  phone VARCHAR(30),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS role (
  role_id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS permission (
  permission_id BIGSERIAL PRIMARY KEY,
  code VARCHAR(100) UNIQUE NOT NULL,
  description VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS user_role (
  user_id BIGINT NOT NULL REFERENCES app_user(user_id) ON DELETE CASCADE,
  role_id BIGINT NOT NULL REFERENCES role(role_id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS role_permission (
  role_id BIGINT NOT NULL REFERENCES role(role_id) ON DELETE CASCADE,
  permission_id BIGINT NOT NULL REFERENCES permission(permission_id) ON DELETE CASCADE,
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (role_id, permission_id)
);

-- Clientes/Vehículos
CREATE TABLE IF NOT EXISTS cliente (
  cliente_id BIGSERIAL PRIMARY KEY,
  razon_social VARCHAR(150) NOT NULL,
  documento VARCHAR(50),
  email VARCHAR(254),
  telefono VARCHAR(30),
  direccion TEXT,
  ciudad VARCHAR(100),
  provincia VARCHAR(100),
  codigo_postal VARCHAR(20),
  notes TEXT,
  UNIQUE (documento),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vehiculo (
  vehiculo_id BIGSERIAL PRIMARY KEY,
  cliente_id BIGINT NOT NULL REFERENCES cliente(cliente_id) ON DELETE RESTRICT,
  placa VARCHAR(20) NOT NULL,
  vin VARCHAR(50),
  marca VARCHAR(50),
  modelo VARCHAR(50),
  anio SMALLINT,
  color VARCHAR(30),
  UNIQUE (placa),
  UNIQUE (vin),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_vehiculo_cliente ON vehiculo (cliente_id);

-- Órdenes de Trabajo (creada antes de inventario)
CREATE TABLE IF NOT EXISTS orden_trabajo (
  ot_id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  cliente_id BIGINT NOT NULL REFERENCES cliente(cliente_id) ON DELETE RESTRICT,
  vehiculo_id BIGINT NOT NULL REFERENCES vehiculo(vehiculo_id) ON DELETE RESTRICT,
  asignado_a_user_id BIGINT REFERENCES app_user(user_id) ON DELETE SET NULL,
  estado VARCHAR(20) NOT NULL CHECK (estado IN ('creada','diagnostico','en_proceso','en_espera','finalizada','entregada','cancelada')),
  diagnostico TEXT,
  notas TEXT,
  fecha_apertura TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  fecha_cierre TIMESTAMPTZ,
  subtotal NUMERIC(14,2) NOT NULL DEFAULT 0,
  impuestos NUMERIC(14,2) NOT NULL DEFAULT 0,
  descuento NUMERIC(14,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ot_estado ON orden_trabajo (estado);
CREATE INDEX IF NOT EXISTS idx_ot_asignado ON orden_trabajo (asignado_a_user_id);
CREATE INDEX IF NOT EXISTS idx_ot_vehiculo ON orden_trabajo (vehiculo_id);

-- Repuestos
CREATE TABLE IF NOT EXISTS repuesto (
  repuesto_id BIGSERIAL PRIMARY KEY,
  sku VARCHAR(60) NOT NULL UNIQUE,
  nombre VARCHAR(150) NOT NULL,
  unidad VARCHAR(20) DEFAULT 'unidad',
  ubicacion VARCHAR(100),
  precio_lista NUMERIC(12,2) DEFAULT 0,
  stock_actual NUMERIC(12,3) NOT NULL DEFAULT 0,
  stock_minimo NUMERIC(12,3) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ítems de OT
CREATE TABLE IF NOT EXISTS ot_item (
  ot_item_id BIGSERIAL PRIMARY KEY,
  ot_id BIGINT NOT NULL REFERENCES orden_trabajo(ot_id) ON DELETE CASCADE,
  tipo VARCHAR(12) NOT NULL CHECK (tipo IN ('repuesto','mano_obra')),
  repuesto_id BIGINT REFERENCES repuesto(repuesto_id) ON DELETE SET NULL,
  descripcion TEXT NOT NULL,
  cantidad NUMERIC(12,3) NOT NULL CHECK (cantidad > 0),
  precio_unitario NUMERIC(12,2) NOT NULL CHECK (precio_unitario >= 0),
  impuestos NUMERIC(12,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) GENERATED ALWAYS AS (cantidad * precio_unitario + impuestos) STORED
);
CREATE INDEX IF NOT EXISTS idx_ot_item_ot ON ot_item (ot_id);
CREATE INDEX IF NOT EXISTS idx_ot_item_repuesto ON ot_item (repuesto_id);

-- Movimientos de Inventario
CREATE TABLE IF NOT EXISTS movimiento_inventario (
  movimiento_id BIGSERIAL PRIMARY KEY,
  repuesto_id BIGINT NOT NULL REFERENCES repuesto(repuesto_id) ON DELETE RESTRICT,
  tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('entrada','salida','ajuste')),
  cantidad NUMERIC(12,3) NOT NULL CHECK (cantidad >= 0),
  costo_unitario NUMERIC(12,2) NOT NULL CHECK (costo_unitario >= 0),
  total_costo NUMERIC(14,2) GENERATED ALWAYS AS (cantidad * costo_unitario) STORED,
  referencia TEXT,
  ot_id BIGINT,
  user_id BIGINT REFERENCES app_user(user_id) ON DELETE SET NULL,
  fecha TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_mov_inv_repuesto_fecha ON movimiento_inventario (repuesto_id, fecha);
ALTER TABLE movimiento_inventario
  ADD CONSTRAINT IF NOT EXISTS movimiento_inventario_ot_fk
  FOREIGN KEY (ot_id) REFERENCES orden_trabajo(ot_id) ON DELETE SET NULL;

-- Agenda / Turnos
CREATE TABLE IF NOT EXISTS turno (
  turno_id BIGSERIAL PRIMARY KEY,
  cliente_id BIGINT NOT NULL REFERENCES cliente(cliente_id) ON DELETE RESTRICT,
  vehiculo_id BIGINT REFERENCES vehiculo(vehiculo_id) ON DELETE SET NULL,
  asignado_a_user_id BIGINT REFERENCES app_user(user_id) ON DELETE SET NULL,
  titulo VARCHAR(150) NOT NULL,
  descripcion TEXT,
  estado VARCHAR(15) NOT NULL CHECK (estado IN ('pendiente','confirmado','cancelado','no_asistio','atendido')),
  fecha_inicio TIMESTAMPTZ NOT NULL,
  fecha_fin TIMESTAMPTZ NOT NULL,
  recordatorio_min INT DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_turno_fechas ON turno (fecha_inicio, fecha_fin);
CREATE INDEX IF NOT EXISTS idx_turno_estado ON turno (estado);

-- Presupuestos
CREATE TABLE IF NOT EXISTS presupuesto (
  presupuesto_id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  cliente_id BIGINT NOT NULL REFERENCES cliente(cliente_id) ON DELETE RESTRICT,
  vehiculo_id BIGINT REFERENCES vehiculo(vehiculo_id) ON DELETE SET NULL,
  creado_por_user_id BIGINT REFERENCES app_user(user_id) ON DELETE SET NULL,
  estado VARCHAR(12) NOT NULL CHECK (estado IN ('borrador','aprobado','rechazado','anulado')),
  observaciones TEXT,
  fecha_emision TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  subtotal NUMERIC(14,2) NOT NULL DEFAULT 0,
  impuestos NUMERIC(14,2) NOT NULL DEFAULT 0,
  descuento NUMERIC(14,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS presupuesto_item (
  presupuesto_item_id BIGSERIAL PRIMARY KEY,
  presupuesto_id BIGINT NOT NULL REFERENCES presupuesto(presupuesto_id) ON DELETE CASCADE,
  tipo VARCHAR(12) NOT NULL CHECK (tipo IN ('repuesto','mano_obra')),
  repuesto_id BIGINT REFERENCES repuesto(repuesto_id) ON DELETE SET NULL,
  descripcion TEXT NOT NULL,
  cantidad NUMERIC(12,3) NOT NULL CHECK (cantidad > 0),
  precio_unitario NUMERIC(12,2) NOT NULL CHECK (precio_unitario >= 0),
  impuestos NUMERIC(12,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) GENERATED ALWAYS AS (cantidad * precio_unitario + impuestos) STORED
);
CREATE INDEX IF NOT EXISTS idx_presupuesto_estado ON presupuesto (estado);

-- Facturación
CREATE TABLE IF NOT EXISTS factura (
  factura_id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  cliente_id BIGINT NOT NULL REFERENCES cliente(cliente_id) ON DELETE RESTRICT,
  vehiculo_id BIGINT REFERENCES vehiculo(vehiculo_id) ON DELETE SET NULL,
  presupuesto_id BIGINT REFERENCES presupuesto(presupuesto_id) ON DELETE SET NULL,
  ot_id BIGINT REFERENCES orden_trabajo(ot_id) ON DELETE SET NULL,
  emitida_por_user_id BIGINT REFERENCES app_user(user_id) ON DELETE SET NULL,
  estado VARCHAR(10) NOT NULL CHECK (estado IN ('borrador','emitida','anulada','pagada')),
  fecha_emision TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  moneda VARCHAR(3) NOT NULL DEFAULT 'ARS',
  subtotal NUMERIC(14,2) NOT NULL DEFAULT 0,
  impuestos NUMERIC(14,2) NOT NULL DEFAULT 0,
  descuento NUMERIC(14,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_factura_estado ON factura (estado);
CREATE INDEX IF NOT EXISTS idx_factura_fecha ON factura (fecha_emision);

CREATE TABLE IF NOT EXISTS factura_item (
  factura_item_id BIGSERIAL PRIMARY KEY,
  factura_id BIGINT NOT NULL REFERENCES factura(factura_id) ON DELETE CASCADE,
  tipo VARCHAR(12) NOT NULL CHECK (tipo IN ('repuesto','mano_obra')),
  repuesto_id BIGINT REFERENCES repuesto(repuesto_id) ON DELETE SET NULL,
  descripcion TEXT NOT NULL,
  cantidad NUMERIC(12,3) NOT NULL CHECK (cantidad > 0),
  precio_unitario NUMERIC(12,2) NOT NULL CHECK (precio_unitario >= 0),
  impuestos NUMERIC(12,2) NOT NULL DEFAULT 0,
  total NUMERIC(14,2) GENERATED ALWAYS AS (cantidad * precio_unitario + impuestos) STORED
);