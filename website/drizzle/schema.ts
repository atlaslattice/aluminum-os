import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, json, boolean } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 */
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Monitored feeds — RSS, regulatory APIs, news sources
 */
export const feeds = mysqlTable("feeds", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 256 }).notNull(),
  url: varchar("url", { length: 2048 }).notNull(),
  feedType: mysqlEnum("feedType", ["rss", "api", "scrape", "manual"]).default("rss").notNull(),
  category: mysqlEnum("category", [
    "regulation", "standard", "academic", "organization",
    "sovereign_infra", "news", "industry"
  ]).default("news").notNull(),
  /** Which VIP Elements this feed is relevant to (JSON array of IDs) */
  vipElements: json("vipElements").$type<string[]>(),
  /** Which dialect overlays this feed covers */
  dialectOverlay: varchar("dialectOverlay", { length: 64 }),
  enabled: boolean("enabled").default(true).notNull(),
  lastChecked: timestamp("lastChecked"),
  checkIntervalMinutes: int("checkIntervalMinutes").default(360).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Feed = typeof feeds.$inferSelect;
export type InsertFeed = typeof feeds.$inferInsert;

/**
 * Ingested references — entries discovered by autonomous monitoring
 */
export const references = mysqlTable("references", {
  id: int("id").autoincrement().primaryKey(),
  feedId: int("feedId"),
  title: varchar("title", { length: 512 }).notNull(),
  url: varchar("url", { length: 2048 }).notNull(),
  /** Brief summary/description */
  summary: text("summary"),
  /** Source organization or author */
  source: varchar("source", { length: 256 }),
  /** Category classification */
  category: mysqlEnum("category", [
    "regulation", "standard", "academic", "organization",
    "sovereign_infra", "news", "industry"
  ]).default("news").notNull(),
  /** Verification status */
  status: mysqlEnum("status", ["unverified", "verified", "rejected", "archived"]).default("unverified").notNull(),
  /** Relevance score 0-100 from LLM analysis */
  relevanceScore: int("relevanceScore"),
  /** VIP Elements this reference maps to (JSON array) */
  vipElements: json("vipElements").$type<string[]>(),
  /** Dialect overlay context */
  dialectOverlay: varchar("dialectOverlay", { length: 64 }),
  /** House/Sphere mapping (JSON array of H#-S# addresses) */
  ontologyMapping: json("ontologyMapping").$type<string[]>(),
  /** Raw metadata from the feed */
  metadata: json("metadata").$type<Record<string, unknown>>(),
  /** Who verified/rejected (user ID) */
  reviewedBy: int("reviewedBy"),
  reviewedAt: timestamp("reviewedAt"),
  /** Review notes */
  reviewNotes: text("reviewNotes"),
  discoveredAt: timestamp("discoveredAt").defaultNow().notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Reference = typeof references.$inferSelect;
export type InsertReference = typeof references.$inferInsert;

/**
 * Ingestion logs — track each autonomous ingestion run
 */
export const ingestionLogs = mysqlTable("ingestion_logs", {
  id: int("id").autoincrement().primaryKey(),
  feedId: int("feedId"),
  status: mysqlEnum("status", ["running", "success", "partial", "failed"]).default("running").notNull(),
  itemsFound: int("itemsFound").default(0).notNull(),
  itemsIngested: int("itemsIngested").default(0).notNull(),
  itemsDuplicate: int("itemsDuplicate").default(0).notNull(),
  errorMessage: text("errorMessage"),
  duration: int("duration"), // milliseconds
  startedAt: timestamp("startedAt").defaultNow().notNull(),
  completedAt: timestamp("completedAt"),
});

export type IngestionLog = typeof ingestionLogs.$inferSelect;
export type InsertIngestionLog = typeof ingestionLogs.$inferInsert;
