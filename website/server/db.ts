import { eq, desc, and, sql } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { InsertUser, users, feeds, references, ingestionLogs, InsertFeed, InsertReference, InsertIngestionLog } from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

// ==================== USER HELPERS ====================

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ==================== FEED HELPERS ====================

export async function listFeeds() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(feeds).orderBy(desc(feeds.createdAt));
}

export async function createFeed(feed: InsertFeed) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  const result = await db.insert(feeds).values(feed);
  return result[0].insertId;
}

export async function updateFeed(id: number, data: Partial<InsertFeed>) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  await db.update(feeds).set(data).where(eq(feeds.id, id));
}

export async function deleteFeed(id: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  await db.delete(feeds).where(eq(feeds.id, id));
}

export async function getEnabledFeeds() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(feeds).where(eq(feeds.enabled, true));
}

// ==================== REFERENCE HELPERS ====================

export async function listReferences(options?: {
  status?: string;
  category?: string;
  limit?: number;
  offset?: number;
}) {
  const db = await getDb();
  if (!db) return { items: [], total: 0 };

  const conditions = [];
  if (options?.status) {
    conditions.push(eq(references.status, options.status as any));
  }
  if (options?.category) {
    conditions.push(eq(references.category, options.category as any));
  }

  const whereClause = conditions.length > 0 ? and(...conditions) : undefined;

  const items = await db
    .select()
    .from(references)
    .where(whereClause)
    .orderBy(desc(references.discoveredAt))
    .limit(options?.limit ?? 50)
    .offset(options?.offset ?? 0);

  const countResult = await db
    .select({ count: sql<number>`count(*)` })
    .from(references)
    .where(whereClause);

  return { items, total: countResult[0]?.count ?? 0 };
}

export async function createReference(ref: InsertReference) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  const result = await db.insert(references).values(ref);
  return result[0].insertId;
}

export async function createReferences(refs: InsertReference[]) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  if (refs.length === 0) return 0;
  const result = await db.insert(references).values(refs);
  return result[0].affectedRows;
}

export async function updateReferenceStatus(
  id: number,
  status: "verified" | "rejected" | "archived",
  reviewedBy: number,
  reviewNotes?: string
) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  await db.update(references).set({
    status,
    reviewedBy,
    reviewedAt: new Date(),
    reviewNotes: reviewNotes ?? null,
  }).where(eq(references.id, id));
}

export async function getReferenceStats() {
  const db = await getDb();
  if (!db) return { total: 0, unverified: 0, verified: 0, rejected: 0 };

  const result = await db.select({
    status: references.status,
    count: sql<number>`count(*)`,
  }).from(references).groupBy(references.status);

  const stats = { total: 0, unverified: 0, verified: 0, rejected: 0, archived: 0 };
  for (const row of result) {
    stats[row.status as keyof typeof stats] = row.count;
    stats.total += row.count;
  }
  return stats;
}

export async function checkDuplicateReference(url: string) {
  const db = await getDb();
  if (!db) return false;
  const result = await db.select({ id: references.id }).from(references).where(eq(references.url, url)).limit(1);
  return result.length > 0;
}

// ==================== INGESTION LOG HELPERS ====================

export async function createIngestionLog(log: InsertIngestionLog) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  const result = await db.insert(ingestionLogs).values(log);
  return result[0].insertId;
}

export async function updateIngestionLog(id: number, data: Partial<InsertIngestionLog>) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");
  await db.update(ingestionLogs).set(data).where(eq(ingestionLogs.id, id));
}

export async function listIngestionLogs(limit = 20) {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(ingestionLogs).orderBy(desc(ingestionLogs.startedAt)).limit(limit);
}
