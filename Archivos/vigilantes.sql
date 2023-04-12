-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-11-2022 a las 18:00:54
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `vigilantes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caja`
--

CREATE TABLE `caja` (
  `Codigo_Caja` int(11) NOT NULL,
  `Accion` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Total` varchar(500) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cobros_2022`
--

CREATE TABLE `cobros_2022` (
  `placa` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `id_clientes` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `enero` bigint(20) DEFAULT NULL,
  `febrero` bigint(20) DEFAULT NULL,
  `marzo` bigint(20) DEFAULT NULL,
  `abril` bigint(20) DEFAULT NULL,
  `mayo` bigint(20) DEFAULT NULL,
  `junio` bigint(20) DEFAULT NULL,
  `julio` bigint(20) DEFAULT NULL,
  `agosto` bigint(20) DEFAULT NULL,
  `septiembre` bigint(20) DEFAULT NULL,
  `octubre` bigint(20) DEFAULT NULL,
  `noviembre` bigint(20) DEFAULT NULL,
  `diciembre` bigint(20) DEFAULT NULL,
  `fecha_ultimo_pago` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compras`
--

CREATE TABLE `compras` (
  `ID_Usuarios` int(11) NOT NULL,
  `Codigo` int(11) NOT NULL,
  `Valor` int(11) DEFAULT NULL,
  `Documento` blob NOT NULL,
  `Fecha_Compra` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `creditos`
--

CREATE TABLE `creditos` (
  `ID_Usuarios` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Codigo_Producto` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Fecha_Credito` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Meses_Cobrados` varchar(500) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `egresos`
--

CREATE TABLE `egresos` (
  `Consepto` text COLLATE utf8_unicode_ci NOT NULL,
  `Codigo_Caja` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `Valor` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Fecha_Pago` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas_ingresos`
--

CREATE TABLE `facturas_ingresos` (
  `ID_Usuarios` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Codigo_Caja` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresos`
--

CREATE TABLE `ingresos` (
  `ID_Productos` text COLLATE utf8_unicode_ci NOT NULL,
  `Codigo_Caja` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `Valor` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Fecha_Pago` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `Codigo` int(11) NOT NULL,
  `Nombre` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Precio` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Cantidad` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID_Usuarios` int(11) NOT NULL,
  `Nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Telefono` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Correo` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Cedula` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Direccion` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Clave_Seguridad` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Fecha_Registro` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_eliminados`
--

CREATE TABLE `usuarios_eliminados` (
  `ID_Usuarios` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Nombre` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Telefono` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Correo` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Cedula` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Direccion` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Clave_Seguridad` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `Fecha_Eliminacion` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `ID_Vehiculos` int(11) NOT NULL,
  `id_client` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `placa` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_gps` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_vehiculo` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name_client` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `estado` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_instalacion` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fecha_instalacion` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `caja`
--
ALTER TABLE `caja`
  ADD PRIMARY KEY (`Codigo_Caja`);

--
-- Indices de la tabla `compras`
--
ALTER TABLE `compras`
  ADD PRIMARY KEY (`ID_Usuarios`,`Codigo`),
  ADD KEY `Codigo` (`Codigo`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`Codigo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID_Usuarios`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`ID_Vehiculos`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `caja`
--
ALTER TABLE `caja`
  MODIFY `Codigo_Caja` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `Codigo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID_Usuarios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `ID_Vehiculos` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
