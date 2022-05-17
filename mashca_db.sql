-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mashca
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (5,'Agricultor');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (17,5,61),(18,5,62),(19,5,63),(20,5,64);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add estacion',7,'add_estacion'),(26,'Can change estacion',7,'change_estacion'),(27,'Can delete estacion',7,'delete_estacion'),(28,'Can view estacion',7,'view_estacion'),(29,'Can add estacion coordenadas',8,'add_estacioncoordenadas'),(30,'Can change estacion coordenadas',8,'change_estacioncoordenadas'),(31,'Can delete estacion coordenadas',8,'delete_estacioncoordenadas'),(32,'Can view estacion coordenadas',8,'view_estacioncoordenadas'),(33,'Can add datos calamaca',9,'add_datoscalamaca'),(34,'Can change datos calamaca',9,'change_datoscalamaca'),(35,'Can delete datos calamaca',9,'delete_datoscalamaca'),(36,'Can view datos calamaca',9,'view_datoscalamaca'),(37,'Can add usuario',10,'add_usuario'),(38,'Can change usuario',10,'change_usuario'),(39,'Can delete usuario',10,'delete_usuario'),(40,'Can view usuario',10,'view_usuario'),(41,'Can add Rol',11,'add_rol'),(42,'Can change Rol',11,'change_rol'),(43,'Can delete Rol',11,'delete_rol'),(44,'Can view Rol',11,'view_rol'),(61,'Can add Agricultor',11,'add_Agricultor'),(62,'Can change Agricultor',11,'change_Agricultor'),(63,'Can delete Agricultor',11,'delete_Agricultor'),(64,'Can view Agricultor',11,'view_Agricultor');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$320000$HymwawHLqoiXZWkGYq8a6z$MuVS3pF2sowsqSWoZNW+sNT/SEKIHtnXqN16Qv5ds4w=','2022-05-12 09:49:44.000000',1,'admin','Alejandro','López','alexlopezmartin2001@yahoo.es',1,1,'2022-02-21 17:52:25.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id_idx` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `usuarios_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (63,'2022-05-17 19:28:02.364631','5','Agricultor',1,'[{\"added\": {}}]',11,6);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'Estacion','datoscalamaca'),(7,'Estacion','estacion'),(8,'Estacion','estacioncoordenadas'),(6,'sessions','session'),(11,'Usuarios','rol'),(10,'Usuarios','usuario');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'Estacion','0001_initial','2022-04-07 09:55:54.471832'),(2,'Estacion','0002_alter_estacion_options_alter_estacion_latitud_and_more','2022-04-07 09:55:54.575254'),(3,'Estacion','0003_remove_estacion_latitud_remove_estacion_longitud_and_more','2022-04-07 09:55:54.734337'),(4,'Estacion','0004_estacion_formato_estacion_latitud_estacion_longitud_and_more','2022-04-07 09:55:54.844976'),(5,'Estacion','0005_alter_estacion_formato_alter_estacion_latitud_and_more','2022-04-07 09:55:54.852610'),(6,'Estacion','0006_alter_estacion_formato','2022-04-07 09:55:54.858591'),(7,'Estacion','0007_alter_estacion_formato','2022-04-07 09:55:54.863650'),(8,'Estacion','0008_datoscalamaca','2022-04-07 09:55:54.888218'),(9,'contenttypes','0001_initial','2022-04-07 09:55:54.929891'),(10,'auth','0001_initial','2022-04-07 09:55:55.699907'),(11,'admin','0001_initial','2022-04-07 09:55:55.861594'),(12,'admin','0002_logentry_remove_auto_add','2022-04-07 09:55:55.872376'),(13,'admin','0003_logentry_add_action_flag_choices','2022-04-07 09:55:55.881398'),(14,'contenttypes','0002_remove_content_type_name','2022-04-07 09:55:56.031353'),(15,'auth','0002_alter_permission_name_max_length','2022-04-07 09:55:56.180780'),(16,'auth','0003_alter_user_email_max_length','2022-04-07 09:55:56.209473'),(17,'auth','0004_alter_user_username_opts','2022-04-07 09:55:56.219357'),(18,'auth','0005_alter_user_last_login_null','2022-04-07 09:55:56.288406'),(19,'auth','0006_require_contenttypes_0002','2022-04-07 09:55:56.294166'),(20,'auth','0007_alter_validators_add_error_messages','2022-04-07 09:55:56.304139'),(21,'auth','0008_alter_user_username_max_length','2022-04-07 09:55:56.367970'),(22,'auth','0009_alter_user_last_name_max_length','2022-04-07 09:55:56.494369'),(23,'auth','0010_alter_group_name_max_length','2022-04-07 09:55:56.521233'),(24,'auth','0011_update_proxy_permissions','2022-04-07 09:55:56.530210'),(25,'auth','0012_alter_user_first_name_max_length','2022-04-07 09:55:56.609546'),(26,'sessions','0001_initial','2022-04-07 09:55:56.653201'),(27,'Estacion','0009_estacion_archivo_csv','2022-04-19 16:20:05.296273'),(28,'Estacion','0010_alter_estacion_archivo_csv','2022-04-19 17:52:52.628663'),(29,'Estacion','0011_delete_datoscalamaca','2022-04-22 20:23:13.040686'),(30,'usuario','0001_initial','2022-05-17 10:19:08.540659'),(31,'usuario','0002_delete_usuario','2022-05-17 10:19:08.636518'),(32,'usuario','0003_initial','2022-05-17 10:38:45.397314'),(33,'usuario','0004_user_rol','2022-05-17 10:38:45.480621'),(34,'usuario','0005_delete_user','2022-05-17 10:38:45.591623'),(35,'Usuarios','0001_initial','2022-05-17 16:29:24.594115'),(36,'Usuarios','0002_rol_usuario_rol','2022-05-17 16:55:43.822805'),(37,'Usuarios','0003_rename_usuario_activo_usuario_is_active_and_more','2022-05-17 17:00:15.850238'),(38,'Usuarios','0004_usuario_groups_usuario_is_superuser_and_more','2022-05-17 17:02:07.832155'),(39,'Usuarios','0005_alter_usuario_is_superuser','2022-05-17 17:30:46.679062');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('08o9mwcjv9j02tqx0c5se8c7ewa1g28h','.eJxVjMsOgjAUBf-la9P00gfFpXu_obkvBDWQUFgZ_11JWOj2zMx5mYLbOpSt6lJGMWeTzOl3I-SHTjuQO0632fI8rctIdlfsQau9zqLPy-H-HQxYh2_NfeTUdAnEae4iBvA9AXmBgKjqnVNocqQ2SHYcElHIXcqgwE3rmcz7A-ZPN8Y:1nr16B:Gm9rjKgZQH_Q-foLzHNqlmZ8-NSamveexDFURiiuIsA','2022-05-31 17:35:07.912225'),('gxhrfaa02ezerdlx2mpxrcy4hsc9qzq2','.eJxVjDsOwjAQBe_iGln-e01JzxmsXX9wADlSnFSIu0OkFNC-mXkvFnFbW9xGWeKU2ZlJdvrdCNOj9B3kO_bbzNPc12Uiviv8oINf51yel8P9O2g42reGismQJG91CLaCIo9B-VCUA8rVFVGBTEhOo80ZtQAlHFjS6CChNOz9AerWN-Q:1nTiPQ:BIT5Do8rg_xmMsE5vRylZEZrGXShFu6GwTUJzhdt8q8','2022-03-28 10:58:40.434000'),('o577dxoyfondfd8xzcbnb6odi4m03dkw','.eJxVjDsOwjAQBe_iGln-e01JzxmsXX9wADlSnFSIu0OkFNC-mXkvFnFbW9xGWeKU2ZlJdvrdCNOj9B3kO_bbzNPc12Uiviv8oINf51yel8P9O2g42reGismQJG91CLaCIo9B-VCUA8rVFVGBTEhOo80ZtQAlHFjS6CChNOz9AerWN-Q:1nZrJv:riHGNVyfXan_6dhzNSqUa8ySjrPTgGZJxvpOL2uwF1s','2022-04-14 09:42:23.940000'),('ohzqkcf4d3in19r4ik93i5mqk0w7x37b','.eJxVjDsOwjAQBe_iGln-e01JzxmsXX9wADlSnFSIu0OkFNC-mXkvFnFbW9xGWeKU2ZlJdvrdCNOj9B3kO_bbzNPc12Uiviv8oINf51yel8P9O2g42reGismQJG91CLaCIo9B-VCUA8rVFVGBTEhOo80ZtQAlHFjS6CChNOz9AerWN-Q:1nPKWd:KBCXw2iHlIhrqtzRdnw8zWjSQhaYVO1YwXaIZ2bzlgk','2022-03-16 08:39:59.980000'),('s203yvgbhpbgfwuxa8rf8w3cshv3w2n9','.eJxVjDsOwjAQBe_iGln-e01JzxmsXX9wADlSnFSIu0OkFNC-mXkvFnFbW9xGWeKU2ZlJdvrdCNOj9B3kO_bbzNPc12Uiviv8oINf51yel8P9O2g42reGismQJG91CLaCIo9B-VCUA8rVFVGBTEhOo80ZtQAlHFjS6CChNOz9AerWN-Q:1nj1SC:AUzyps5_E-SA31-SJY5uP419zD6waYGPNSyhduq9wUc','2022-05-09 16:20:48.558237'),('yfmp1acv06luhilnashwl516oida67ri','.eJxVjDsOwjAQBe_iGln-e01JzxmsXX9wADlSnFSIu0OkFNC-mXkvFnFbW9xGWeKU2ZlJdvrdCNOj9B3kO_bbzNPc12Uiviv8oINf51yel8P9O2g42reGismQJG91CLaCIo9B-VCUA8rVFVGBTEhOo80ZtQAlHFjS6CChNOz9AerWN-Q:1njngl:rJkCkblVpgzHErMIwqBgNLbhc5FYGqSbj-O7YWyWpJo','2022-05-11 19:51:03.339949');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estacion_estacion`
--

DROP TABLE IF EXISTS `estacion_estacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estacion_estacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `provincia` varchar(255) NOT NULL,
  `estado` varchar(255) NOT NULL,
  `fecha_instalacion` date NOT NULL,
  `formato` varchar(50) NOT NULL,
  `latitud` varchar(50) NOT NULL,
  `longitud` varchar(50) NOT NULL,
  `archivo_csv` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacion_estacion`
--

LOCK TABLES `estacion_estacion` WRITE;
/*!40000 ALTER TABLE `estacion_estacion` DISABLE KEYS */;
INSERT INTO `estacion_estacion` VALUES (1,'M0029','BAÑOS','CP','TUNGURAHUA','FUNCIONANDO','1962-06-20','DMS','012329S','782505W',''),(2,'M0258','QUEROCHACA(UTA)','CP','TUNGURAHUA','FUNCIONANDO','1985-11-02','DMS','012202S','783620W',''),(3,'M1069','CALAMACA CONVENIO INAMHI HCPT','CP','TUNGURAHUA','FUNCIONANDO','1988-07-04','DMS','011634S','784908W','estacion_M1069/8310_5min_20181022.csv'),(4,'M0126','PATATE','CO','TUNGURAHUA','FUNCIONANDO','1963-05-01','DMS','011801S','783000W',''),(5,'M0127','PILLARO','CO','TUNGURAHUA','FUNCIONANDO','1963-12-01','DMS','011010S','783310W',''),(6,'M0128','PEDRO FERMIN CEVALLOS (COLEGIO)','CO','TUNGURAHUA','FUNCIONANDO','1978-05-01','DMS','012109S','783654W','estacion_M0128/8310_5min_20190416.csv'),(7,'M0376','PILAHUIN','PV','TUNGURAHUA','FUNCIONANDO','1964-07-16','DMS','011806S','784356W',''),(8,'M0377','TISALEO','PV','TUNGURAHUA','FUNCIONANDO','1964-07-16','DMS','012042S','783959W',''),(9,'M0378','RIO VERDE','PV','TUNGURAHUA','FUNCIONANDO','1964-07-18','DMS','012404S','781743W',''),(10,'M0380','HUAMBALO','PV','TUNGURAHUA','FUNCIONANDO','1964-07-17','DMS','012314S','783139W',''),(11,'M1243','CUNCHIBAMBA-ITLAM (INST.LUIS A. MARTINEZ)','CP','TUNGURAHUA','FUNCIONANDO','1964-07-17','DMS','010801S','783553W','estacion_M1243/8310_5min_20190128.csv');
/*!40000 ALTER TABLE `estacion_estacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_rol`
--

DROP TABLE IF EXISTS `usuarios_rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_rol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rol` (`rol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_rol`
--

LOCK TABLES `usuarios_rol` WRITE;
/*!40000 ALTER TABLE `usuarios_rol` DISABLE KEYS */;
INSERT INTO `usuarios_rol` VALUES (5,'Agricultor');
/*!40000 ALTER TABLE `usuarios_rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_usuario`
--

DROP TABLE IF EXISTS `usuarios_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `nombres` varchar(200) DEFAULT NULL,
  `apellidos` varchar(200) DEFAULT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `rol_id` int DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `Usuarios_usuario_rol_id_25cb73df_fk_Usuarios_rol_id` (`rol_id`),
  CONSTRAINT `Usuarios_usuario_rol_id_25cb73df_fk_Usuarios_rol_id` FOREIGN KEY (`rol_id`) REFERENCES `usuarios_rol` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_usuario`
--

LOCK TABLES `usuarios_usuario` WRITE;
/*!40000 ALTER TABLE `usuarios_usuario` DISABLE KEYS */;
INSERT INTO `usuarios_usuario` VALUES (6,'pbkdf2_sha256$320000$5xSEKO7DKKyHBvl3yfIeJI$H3oH//dlX17bFmz3b7XEZjcHyG8De/NlFrB6+/DU04I=','2022-05-17 17:35:07.901215','admin','admin@admin.com','Administrador',NULL,'',1,1,NULL,1);
/*!40000 ALTER TABLE `usuarios_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_usuario_groups`
--

DROP TABLE IF EXISTS `usuarios_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Usuarios_usuario_groups_usuario_id_group_id_974fbf5c_uniq` (`usuario_id`,`group_id`),
  KEY `Usuarios_usuario_groups_group_id_cf7bd56f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Usuarios_usuario_gro_usuario_id_f3985b6d_fk_Usuarios_` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`),
  CONSTRAINT `Usuarios_usuario_groups_group_id_cf7bd56f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_usuario_groups`
--

LOCK TABLES `usuarios_usuario_groups` WRITE;
/*!40000 ALTER TABLE `usuarios_usuario_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuarios_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Usuarios_usuario_user_pe_usuario_id_permission_id_d113e22f_uniq` (`usuario_id`,`permission_id`),
  KEY `Usuarios_usuario_use_permission_id_4a44c74d_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Usuarios_usuario_use_permission_id_4a44c74d_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Usuarios_usuario_use_usuario_id_9d2fc700_fk_Usuarios_` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_usuario_user_permissions`
--

LOCK TABLES `usuarios_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `usuarios_usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-17 21:30:26
