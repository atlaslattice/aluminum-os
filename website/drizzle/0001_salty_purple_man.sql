CREATE TABLE `feeds` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(256) NOT NULL,
	`url` varchar(2048) NOT NULL,
	`feedType` enum('rss','api','scrape','manual') NOT NULL DEFAULT 'rss',
	`category` enum('regulation','standard','academic','organization','sovereign_infra','news','industry') NOT NULL DEFAULT 'news',
	`vipElements` json,
	`dialectOverlay` varchar(64),
	`enabled` boolean NOT NULL DEFAULT true,
	`lastChecked` timestamp,
	`checkIntervalMinutes` int NOT NULL DEFAULT 360,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `feeds_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `ingestion_logs` (
	`id` int AUTO_INCREMENT NOT NULL,
	`feedId` int,
	`status` enum('running','success','partial','failed') NOT NULL DEFAULT 'running',
	`itemsFound` int NOT NULL DEFAULT 0,
	`itemsIngested` int NOT NULL DEFAULT 0,
	`itemsDuplicate` int NOT NULL DEFAULT 0,
	`errorMessage` text,
	`duration` int,
	`startedAt` timestamp NOT NULL DEFAULT (now()),
	`completedAt` timestamp,
	CONSTRAINT `ingestion_logs_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `references` (
	`id` int AUTO_INCREMENT NOT NULL,
	`feedId` int,
	`title` varchar(512) NOT NULL,
	`url` varchar(2048) NOT NULL,
	`summary` text,
	`source` varchar(256),
	`category` enum('regulation','standard','academic','organization','sovereign_infra','news','industry') NOT NULL DEFAULT 'news',
	`status` enum('unverified','verified','rejected','archived') NOT NULL DEFAULT 'unverified',
	`relevanceScore` int,
	`vipElements` json,
	`dialectOverlay` varchar(64),
	`ontologyMapping` json,
	`metadata` json,
	`reviewedBy` int,
	`reviewedAt` timestamp,
	`reviewNotes` text,
	`discoveredAt` timestamp NOT NULL DEFAULT (now()),
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `references_id` PRIMARY KEY(`id`)
);
