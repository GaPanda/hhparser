CREATE TABLE `Vacancy` (
	`id_vacancy` int NOT NULL,
	`id_name_vacancy` int NOT NULL,
	`id_name_company` int NOT NULL,
	`id_salary` int,
	`id_experience` int,
	`date_vacancy` DATE NOT NULL,
	PRIMARY KEY (`id_vacancy`)
);

CREATE TABLE `Company` (
	`id_company` int NOT NULL,
	`name_company` varchar(60) NOT NULL UNIQUE,
	PRIMARY KEY (`id_company`)
);

CREATE TABLE `Name_vacancy` (
	`id_name_vacancy` int NOT NULL,
	`name_vacancy` varchar(60) NOT NULL UNIQUE,
	PRIMARY KEY (`id_name_vacancy`)
);

CREATE TABLE `Salary` (
	`id_salary` int NOT NULL,
	`min_salary` int,
	`max_salary` int,
	`currency` varchar(3) NOT NULL,
	PRIMARY KEY (`id_salary`)
);

CREATE TABLE `Experience` (
	`id_experience` int NOT NULL,
	`min_experience` int,
	`max_experience` int,
	PRIMARY KEY (`id_experience`)
);

CREATE TABLE `Conditions` (
	`id_condition` int NOT NULL,
	`text_condition` varchar(200) NOT NULL UNIQUE,
	PRIMARY KEY (`id_condition`)
);

CREATE TABLE `Expectations` (
	`id_expectation` int NOT NULL,
	`text_expectations` varchar(200) NOT NULL UNIQUE,
	PRIMARY KEY (`id_expectation`)
);

CREATE TABLE `Requirements` (
	`id_requirement` int NOT NULL,
	`text_requirements` varchar(200) NOT NULL UNIQUE,
	PRIMARY KEY (`id_requirement`)
);

CREATE TABLE `Vac_req` (
	`id_desc_req` int NOT NULL,
	`id_vacancy` int NOT NULL,
	`id_requirement` int NOT NULL,
	PRIMARY KEY (`id_desc_req`)
);

CREATE TABLE `Vac_exp` (
	`id_desc_exp` int NOT NULL,
	`id_vacancy` int NOT NULL,
	`id_expectation` int NOT NULL,
	PRIMARY KEY (`id_desc_exp`)
);

CREATE TABLE `Vac_con` (
	`id_desc_con` int NOT NULL,
	`id_vacancy` int NOT NULL,
	`id_condition` int NOT NULL,
	PRIMARY KEY (`id_desc_con`)
);

ALTER TABLE `Vacancy` ADD CONSTRAINT `Vacancy_fk0` FOREIGN KEY (`id_name_vacancy`) REFERENCES `Name_vacancy`(`id_name_vacancy`);

ALTER TABLE `Vacancy` ADD CONSTRAINT `Vacancy_fk1` FOREIGN KEY (`id_name_company`) REFERENCES `Company`(`id_company`);

ALTER TABLE `Vacancy` ADD CONSTRAINT `Vacancy_fk2` FOREIGN KEY (`id_salary`) REFERENCES `Salary`(`id_salary`);

ALTER TABLE `Vacancy` ADD CONSTRAINT `Vacancy_fk3` FOREIGN KEY (`id_experience`) REFERENCES `Experience`(`id_experience`);

ALTER TABLE `Vac_req` ADD CONSTRAINT `Vac_req_fk0` FOREIGN KEY (`id_vacancy`) REFERENCES `Vacancy`(`id_vacancy`);

ALTER TABLE `Vac_req` ADD CONSTRAINT `Vac_req_fk1` FOREIGN KEY (`id_requirement`) REFERENCES `Requirements`(`id_requirement`);

ALTER TABLE `Vac_exp` ADD CONSTRAINT `Vac_exp_fk0` FOREIGN KEY (`id_vacancy`) REFERENCES `Vacancy`(`id_vacancy`);

ALTER TABLE `Vac_exp` ADD CONSTRAINT `Vac_exp_fk1` FOREIGN KEY (`id_expectation`) REFERENCES `Expectations`(`id_expectation`);

ALTER TABLE `Vac_con` ADD CONSTRAINT `Vac_con_fk0` FOREIGN KEY (`id_vacancy`) REFERENCES `Vacancy`(`id_vacancy`);

ALTER TABLE `Vac_con` ADD CONSTRAINT `Vac_con_fk1` FOREIGN KEY (`id_condition`) REFERENCES `Conditions`(`id_condition`);

