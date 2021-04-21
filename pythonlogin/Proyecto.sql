/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.18-MariaDB : Database - proyecto
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`proyecto` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `proyecto`;

/*Table structure for table `asignatura` */

DROP TABLE IF EXISTS `asignatura`;

CREATE TABLE `asignatura` (
  `ID_ASIGNATURA` int(10) NOT NULL AUTO_INCREMENT,
  `Asignatura` varchar(50) NOT NULL,
  `Fecha_Creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `Estado` int(1) DEFAULT NULL,
  PRIMARY KEY (`ID_ASIGNATURA`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `asignatura` */

insert  into `asignatura`(`ID_ASIGNATURA`,`Asignatura`,`Fecha_Creacion`,`Estado`) values 
(1,'INGLES','2021-04-03 18:08:52',1),
(2,'ESPAÑOL','2021-04-03 18:09:00',1),
(3,'FISICA','2021-04-03 18:09:07',1),
(4,'ELECTRONICA','2021-04-03 18:10:28',1),
(5,'MECANICA','2021-04-13 19:18:09',1),
(6,'PROGRAMACION','2021-04-13 19:18:26',1),
(7,'CALCULO','2021-04-13 19:18:57',1),
(8,'DESARROLLO HUMANO','2021-04-13 19:19:05',1);

/*Table structure for table `disponibilidad_asesor` */

DROP TABLE IF EXISTS `disponibilidad_asesor`;

CREATE TABLE `disponibilidad_asesor` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `ID_USUARIO` int(10) NOT NULL,
  `Hora_Inicial` timestamp NULL DEFAULT NULL,
  `Hora_Final` timestamp NULL DEFAULT NULL,
  `Estado` int(1) NOT NULL,
  `Fecha_Creacion` timestamp NULL DEFAULT current_timestamp(),
  KEY `ID` (`ID`),
  KEY `ID_USUARIO` (`ID_USUARIO`),
  CONSTRAINT `disponibilidad_asesor_ibfk_1` FOREIGN KEY (`ID_USUARIO`) REFERENCES `usuarios` (`ID_USUARIO`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `disponibilidad_asesor` */

insert  into `disponibilidad_asesor`(`ID`,`ID_USUARIO`,`Hora_Inicial`,`Hora_Final`,`Estado`,`Fecha_Creacion`) values 
(2,2,'2021-04-13 20:44:00','2021-04-14 20:44:00',1,'2021-04-13 20:56:21'),
(3,2,'2021-04-14 20:56:00','2021-04-16 20:56:00',1,'2021-04-13 20:56:13');

/*Table structure for table `relacion_usuario` */

DROP TABLE IF EXISTS `relacion_usuario`;

CREATE TABLE `relacion_usuario` (
  `ID_RELACION` int(10) NOT NULL AUTO_INCREMENT,
  `ID_USUARIO` int(10) NOT NULL,
  `ID_ASIGNATURA` int(10) NOT NULL,
  `ID_ASESOR` int(10) NOT NULL,
  `Estado` int(1) NOT NULL,
  `Hora_Inicial` timestamp NULL DEFAULT NULL,
  `Hora_Final` timestamp NULL DEFAULT NULL,
  KEY `ID` (`ID_RELACION`),
  KEY `ID_USUARIO` (`ID_USUARIO`),
  KEY `ID_ASIGNATURA` (`ID_ASIGNATURA`),
  KEY `ID_ASESOR` (`ID_ASESOR`),
  CONSTRAINT `relacion_usuario_ibfk_1` FOREIGN KEY (`ID_USUARIO`) REFERENCES `usuarios` (`ID_USUARIO`),
  CONSTRAINT `relacion_usuario_ibfk_2` FOREIGN KEY (`ID_ASIGNATURA`) REFERENCES `asignatura` (`ID_ASIGNATURA`),
  CONSTRAINT `relacion_usuario_ibfk_3` FOREIGN KEY (`ID_ASESOR`) REFERENCES `usuarios` (`ID_USUARIO`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `relacion_usuario` */

insert  into `relacion_usuario`(`ID_RELACION`,`ID_USUARIO`,`ID_ASIGNATURA`,`ID_ASESOR`,`Estado`,`Hora_Inicial`,`Hora_Final`) values 
(1,2,1,3,1,NULL,NULL),
(2,2,2,3,1,NULL,NULL),
(3,2,3,5,1,NULL,NULL),
(4,2,4,4,1,NULL,NULL);

/*Table structure for table `roles` */

DROP TABLE IF EXISTS `roles`;

CREATE TABLE `roles` (
  `ID_ROL` int(10) NOT NULL AUTO_INCREMENT,
  `Rol` varchar(50) NOT NULL,
  `Fecha_Creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `Estado` int(1) NOT NULL,
  PRIMARY KEY (`ID_ROL`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `roles` */

insert  into `roles`(`ID_ROL`,`Rol`,`Fecha_Creacion`,`Estado`) values 
(1,'ADMINISTRADOR','2021-04-03 17:47:30',1),
(2,'ASESOR','2021-04-03 17:47:54',1),
(3,'ESTUDIANTE','2021-04-12 23:55:34',1);

/*Table structure for table `usuarios` */

DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `ID_USUARIO` int(10) NOT NULL AUTO_INCREMENT,
  `Cedula` varchar(10) NOT NULL,
  `Nombres` varchar(50) NOT NULL,
  `Apellidos` varchar(50) NOT NULL,
  `Correo` varchar(50) NOT NULL,
  `Telefono` varchar(10) NOT NULL,
  `Usuario` varchar(50) NOT NULL,
  `Contraseña` varchar(50) NOT NULL,
  `ID_ROL` int(10) NOT NULL,
  `Estado` int(1) NOT NULL,
  `Fecha_Creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID_USUARIO`),
  KEY `Rol` (`ID_ROL`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`ID_ROL`) REFERENCES `roles` (`ID_ROL`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4;

/*Data for the table `usuarios` */

insert  into `usuarios`(`ID_USUARIO`,`Cedula`,`Nombres`,`Apellidos`,`Correo`,`Telefono`,`Usuario`,`Contraseña`,`ID_ROL`,`Estado`,`Fecha_Creacion`) values 
(2,'1111','BRYAN ','VILLANUEVA RIVAS','BR@HOY.COM','300706952','Bryan1234','12345',1,1,'2021-04-03 18:12:08'),
(3,'222','PEDRO ALVERTO','RIVAS','PD@HOY.COM','42342545','Pedro123','123',3,1,'2021-04-03 18:12:52'),
(4,'333','JUAN','VARON','JN@HOY.COM','24545245','Juan123','123',2,1,'2021-04-03 18:16:09'),
(5,'444','PEPE JUAN','VILLA','PE@HOY.COM','23213413','PEPE','123',2,1,'2021-04-03 18:16:54'),
(6,'666','JUANITO','PEREZ','JN@HOY.COM','30073','Juanito12','123',3,1,'2021-04-03 18:57:25'),
(8,'111','JUANITA MARIA','PEREA','JU@HOT.COM','13425635','JUA','123',3,1,'2021-04-11 23:57:53'),
(21,'123','ALVERTO','PEREA','ALVERTO@hoy.com','123124','ALVERTO123','123',3,1,'2021-04-13 00:19:17'),
(22,'1233425','LUIS','dddd','luis@hoy.com','1230148','luis23','123',3,1,'2021-04-13 00:33:30'),
(23,'567456356','RUPERTO ALFONSO','VARON','RUPERTO@hoy.com','13290','RUPERTO123','1234',2,1,'2021-04-13 00:36:09'),
(24,'1232435245','DORIAN','DE DONDE','DORIAN@hoy.com','324234234','DORIAN123','1234',2,2,'2021-04-13 18:30:36'),
(28,'2134134','JOSE MIGUEL','CASTRILLON','JOSE@HOY.COM','340928342','JOSE123','12345',1,1,'2021-04-16 13:42:08');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
