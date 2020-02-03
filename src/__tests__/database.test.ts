import Database from "@/services/database";

test("Create Test Database", () => {
    const db = new Database();
    db.connect(true);
});

test("Create test database with initial tables", async () => {
    // We are expecting one sqlite error
    expect.assertions(1);
    const db = new Database();
    await db.connect(true);

    // No tables initialized
    try {
        await db.one('SELECT * FROM processes');
    } catch (e) {
        expect(e.name).toBe("SqliteError");
    }

    await db.update();
    await db.one('SELECT * FROM processes');
});
