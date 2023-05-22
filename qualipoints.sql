-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 07-Maio-2023 às 02:13
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `qualipoints`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `campanha`
--

CREATE TABLE `campanha` (
  `id_campanha` int(11) NOT NULL,
  `json` longtext NOT NULL,
  `ultimo_input` datetime NOT NULL,
  `criado_por` varchar(100) NOT NULL,
  `prazo` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `campanha`
--

INSERT INTO `campanha` (`id_campanha`, `json`, `ultimo_input`, `criado_por`, `prazo`) VALUES
(3, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpbmRpY2Fkb3IxIjoie1wibWV0YVwiOjEwLFwicG9udHVhY2FvXCI6MyxcImNvbXBhcmFjYW9cIjpcIj49XCJ9IiwiaW5kaWNhZG9yMiI6IntcIm1ldGFcIjo1LFwicG9udHVhY2FvXCI6MSxcImNvbXBhcmFjYW9cIjpcIjw9XCJ9IiwiaW5kaWNhZG9yMyI6IntcIm1ldGFcIjo1LFwicG9udHVhY2FvXCI6MSxcImNvbXBhcmFjYW9cIjpcIj49XCJ9IiwiaW5kaWNhZG9yNCI6IntcIm1ldGFcIjo1LFwicG9udHVhY2FvXCI6MSxcImNvbXBhcmFjYW9cIjpcIjw9XCJ9IiwiaW5kaWNhZG9yNSI6IntcIm1ldGFcIjo1LFwicG9udHVhY2FvXCI6MSxcImNvbXBhcmFjYW9cIjpcIj49XCJ9IiwiaW5kaWNhZG9yNiI6IntcIm1ldGFcIjo1LFwicG9udHVhY2FvXCI6MSxcImNvbXBhcmFjYW9cIjpcIjw9XCJ9In0.AsYJXh8Q2hO7dbESyKz9yEk9jRpnvFc2Eptr11poBAs', '2023-04-19 00:00:00', 'teste', '2023-04-20 00:00:00');

-- --------------------------------------------------------

--
-- Estrutura da tabela `pontos`
--

CREATE TABLE `pontos` (
  `matricula_operador` varchar(20) NOT NULL,
  `pontos` int(11) NOT NULL DEFAULT 0,
  `ultima_atualizacao` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `pontos`
--

INSERT INTO `pontos` (`matricula_operador`, `pontos`, `ultima_atualizacao`) VALUES
('1411080', 0, '2023-05-06 21:13:01'),
('1411107', 0, '2023-05-06 21:13:01'),
('1411952', 0, '2023-05-06 21:13:01'),
('1411953', 6, '2023-05-06 21:13:01');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `campanha`
--
ALTER TABLE `campanha`
  ADD PRIMARY KEY (`id_campanha`);

--
-- Índices para tabela `pontos`
--
ALTER TABLE `pontos`
  ADD PRIMARY KEY (`matricula_operador`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `campanha`
--
ALTER TABLE `campanha`
  MODIFY `id_campanha` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
