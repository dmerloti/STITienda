-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 19-08-2026 a las 10:47:56
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `stistore`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos`
--

DROP TABLE IF EXISTS `articulos`;
CREATE TABLE IF NOT EXISTS `articulos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idarticulo` int NOT NULL,
  `codigo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `precontado` float NOT NULL,
  `cuotas6de` float NOT NULL,
  `cuotas12de` float NOT NULL,
  `idrubro` int NOT NULL,
  `foto` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  `codigoBarras` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `existencia` float NOT NULL,
  `puntoReposicion` float NOT NULL,
  `idumedida` smallint NOT NULL,
  `precio` float NOT NULL,
  `iva` float NOT NULL,
  `dolar` float NOT NULL,
  `precioCosto` float NOT NULL,
  `precioVentaMayorista` float NOT NULL,
  `idproveedor` smallint NOT NULL,
  `idmarca` smallint NOT NULL,
  `idtipoiva` smallint NOT NULL,
  `idusuario` smallint NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `porcentajeGanancia` float NOT NULL,
  `porcentajeGananciaMayorista` float NOT NULL,
  `fechaVencimiento` datetime NOT NULL,
  `fechaUltimaCarga` datetime NOT NULL,
  `oferta` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos`
--

INSERT INTO `articulos` (`id`, `idarticulo`, `codigo`, `concepto`, `descripcion`, `precontado`, `cuotas6de`, `cuotas12de`, `idrubro`, `foto`, `activo`, `codigoBarras`, `existencia`, `puntoReposicion`, `idumedida`, `precio`, `iva`, `dolar`, `precioCosto`, `precioVentaMayorista`, `idproveedor`, `idmarca`, `idtipoiva`, `idusuario`, `fechaActualizacion`, `porcentajeGanancia`, `porcentajeGananciaMayorista`, `fechaVencimiento`, `fechaUltimaCarga`, `oferta`) VALUES
(1, 9774, 'n151', 'NOTEBOOK GFAST N-151 (15.6/N4020/4GB/128SSD/WIN11)', 'Procesador Intel N4020\r\nMemoria 4 GB - Disco SSD 128 Mb \r\nPantalla 15.6 pulgadas', 390000, 87000, 0, 1, '2026101616GFastN151.jpeg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0),
(2, 9847, '214236', 'Notebook HP 15.6 255 R3-7330U', 'Procesador AMD Ryzen 3 R3-7330U\r\nDisco Sólido 256 GB - Memoria RAM de 8 GB.	\r\nPantalla LED de 15\".	\r\n', 770000, 176000, 0, 1, '2026101637notebook.jpg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0),
(3, 9848, '214237', 'NB HP 15.6 250 I3-1315U 8GB SSD256GB', 'Procesador Core I3-1315U\r\nDisco Sólido 512 GB - Memoria RAM de 8 GB.	\r\nPantalla LED de 15\".		\r\n', 850000, 195000, 0, 1, '2026101649Bangho CoreI3.jpeg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0),
(4, 1000, 'Nx.d2zal.001', 'Notebook ACER Aspire Lite 14 Ci3 ', 'Procesador Core I3 N355 \r\nDisco Sólido 256 GB - Memoria RAM de 8 GB.	\r\nPantalla LED de 14\".\r\n', 670000, 155000, 0, 0, '2026101700Bangho CoreI3b.jpeg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0),
(5, 0, '215433', 'NB DELL 14 INSPIRON 5440 I5-1334U', 'Procesador CORE I5-1334U \r\nDisco Sólido 512 GB - Memoria RAM de 8 GB.	\r\nPantalla LED de 14\".	\r\n', 1400000, 320000, 0, 0, '2026101711BanghoCoreI5.jpeg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0),
(6, 0, 'AIOHP', 'All In One HP procesador Core I3 Memoria 4 GB disco 240 Gb', '', 0, 0, 0, 0, '2026100817AIOHP.jpeg', 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_grupos`
--

DROP TABLE IF EXISTS `articulos_grupos`;
CREATE TABLE IF NOT EXISTS `articulos_grupos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos_grupos`
--

INSERT INTO `articulos_grupos` (`id`, `concepto`, `activo`) VALUES
(1, 'EQUIPOS', 1),
(2, 'INSUMOS', 1),
(3, 'ACCESORIOS', 1),
(4, 'IMPRESORAS', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_marcas`
--

DROP TABLE IF EXISTS `articulos_marcas`;
CREATE TABLE IF NOT EXISTS `articulos_marcas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos_marcas`
--

INSERT INTO `articulos_marcas` (`id`, `concepto`, `activo`) VALUES
(1, 'HP', 1),
(2, 'Lenovo', 1),
(3, 'GFast', 1),
(4, 'Bangho', 1),
(5, 'CX', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_rubros`
--

DROP TABLE IF EXISTS `articulos_rubros`;
CREATE TABLE IF NOT EXISTS `articulos_rubros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos_rubros`
--

INSERT INTO `articulos_rubros` (`id`, `concepto`, `activo`) VALUES
(1, 'Notebooks', 1),
(2, 'Computadoras', 1),
(3, 'Impresoras', 1),
(4, 'Cartuchos', 1),
(5, 'Toners', 1),
(6, 'Mouses', 1),
(9, 'Teclados', 1),
(11, 'conectividad', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_tipos_iva`
--

DROP TABLE IF EXISTS `articulos_tipos_iva`;
CREATE TABLE IF NOT EXISTS `articulos_tipos_iva` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `alicuota` float NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos_tipos_iva`
--

INSERT INTO `articulos_tipos_iva` (`id`, `concepto`, `alicuota`, `activo`) VALUES
(1, '21 %', 1.21, 1),
(2, '10.5 %', 1.105, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos_unidades`
--

DROP TABLE IF EXISTS `articulos_unidades`;
CREATE TABLE IF NOT EXISTS `articulos_unidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `articulos_unidades`
--

INSERT INTO `articulos_unidades` (`id`, `concepto`, `activo`) VALUES
(1, 'Unidad', 1),
(2, 'Litro', 0),
(3, 'Kilo', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cuit` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idtipocontribuyente` smallint NOT NULL,
  `direccion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `barrio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idlocali` smallint NOT NULL,
  `celular` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `concepto`, `cuit`, `idtipocontribuyente`, `direccion`, `barrio`, `idlocali`, `celular`, `telefono`, `mail`, `activo`) VALUES
(1, 'Yayo', '', 3, 'Monseñor Lindor ferreyra', '', 3, '', '', '', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `localidades`
--

DROP TABLE IF EXISTS `localidades`;
CREATE TABLE IF NOT EXISTS `localidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cp` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idprovincia` smallint NOT NULL DEFAULT '1',
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `localidades`
--

INSERT INTO `localidades` (`id`, `concepto`, `cp`, `idprovincia`, `activo`) VALUES
(1, 'Villa del Rosario', '5963', 1, 1),
(3, 'Córdoba', '5000', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paises`
--

DROP TABLE IF EXISTS `paises`;
CREATE TABLE IF NOT EXISTS `paises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paises`
--

INSERT INTO `paises` (`id`, `concepto`, `activo`) VALUES
(1, 'Argentina', 1),
(3, 'EEUU', 1),
(4, 'Brasil', 1),
(5, 'Chile', 1),
(6, 'Uruguay', 1),
(7, 'Paraguay', 1),
(8, 'Bolivia', 1),
(9, 'Peru', 1),
(10, 'Ecuador', 1),
(11, 'Venezuela', 1),
(12, 'Mexico', 1),
(13, 'Alemania', 1),
(14, 'Suiza', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
CREATE TABLE IF NOT EXISTS `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idlocali` smallint NOT NULL DEFAULT '1',
  `direccion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `barrio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `celular` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idtipocontribuyente` smallint NOT NULL DEFAULT '1',
  `cuit` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id`, `concepto`, `idlocali`, `direccion`, `barrio`, `telefono`, `celular`, `mail`, `idtipocontribuyente`, `cuit`, `activo`) VALUES
(4, 'Air Computers', 3, 'Ramirez de Arellano', '', '', '', '', 3, '54545545454', 1),
(2, 'office insumos', 3, 'General Bustos', '', '', 'dfdfdf', 'office@hotmail.com', 3, '20216935986', 1),
(3, 'trade it', 3, 'Rivera Indarte', '', '', '', '', 3, '54545455544', 1),
(5, 'Mariani Insumos', 1, 'San Juan', '', '', '', '', 2, '', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincias`
--

DROP TABLE IF EXISTS `provincias`;
CREATE TABLE IF NOT EXISTS `provincias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  `idpais` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `provincias`
--

INSERT INTO `provincias` (`id`, `concepto`, `activo`, `idpais`) VALUES
(1, 'Cordoba', 1, 1),
(3, 'Santa Fe', 1, 1),
(4, 'Buenos Aires', 1, 1),
(5, 'Salta', 1, 1),
(6, 'Mendoza', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_contribuyente`
--

DROP TABLE IF EXISTS `tipos_contribuyente`;
CREATE TABLE IF NOT EXISTS `tipos_contribuyente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_contribuyente`
--

INSERT INTO `tipos_contribuyente` (`id`, `concepto`, `activo`) VALUES
(1, 'Monotributista', 1),
(2, 'Responsable Inscripto', 1),
(3, 'Exento', 1),
(4, 'Sujeto No Inscripto', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rol` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idrol` int NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `password`, `rol`, `idrol`, `activo`) VALUES
(1, 'dmerlo', 'scrypt:32768:8:1$CzMFNuo1GIzD51zi$7846a6602968548398797f274783d2a1f7f67507adbd7a3cf04b53c3e9e3ee252e1cceea3ca2d20dcb9093317886803ac3209f43dfb8e25f5cdb28c925624494', 'admin', 1, 0),
(2, 'silfa', 'scrypt:32768:8:1$rAqDcUyNDNhGixnb$4089138cdb6db6adb7a946588006d330f864066fb78e0babfb96d881ba80c56539de5c154201a1cd6f7e21f766b0e28ae99bb2d8d72941aebaba436ba3afd2bd', 'empleado', 1, 0),
(3, 'anita', 'scrypt:32768:8:1$4Zb1zzCa63JZDRY9$41a93ccc3b742103dfae609553bb02c1934a1a9b0ab79ef837063e5f97cb9c8f6596ba33bc4bb966a7b67dbffa4807e7d2fb4b13eaa349a704f5bff5ae527474', 'vendedor', 2, 0),
(5, 'cliente1', 'scrypt:32768:8:1$DURQqQIJJTIMXHfQ$cbe6d6c7515d848e2d035c5c61077f4f5d31dc8fe6abaa19edf6a29b5cc305468098f886243245ddc1aa947ae745c38965f8eb0f89d286a06846da9e596692db', '', 3, 0),
(6, 'camila', 'scrypt:32768:8:1$D5E07pYCA8fYYBcI$4b344016b0c094d96a7e18b92d644a869511c78a4d254c56e816809bbaad703464400a9658a778de87ded48b488078127c681c74a1a1b14216cdac6921d81c65', '', 3, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_roles`
--

DROP TABLE IF EXISTS `usuarios_roles`;
CREATE TABLE IF NOT EXISTS `usuarios_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `concepto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios_roles`
--

INSERT INTO `usuarios_roles` (`id`, `concepto`, `activo`) VALUES
(1, 'admin', 0),
(2, 'empleado', 0),
(3, 'cliente', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
