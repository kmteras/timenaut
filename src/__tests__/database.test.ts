import Database from "@/services/database";

test("Create test database with initial tables", async () => {
    // No tables initialized
    try {
        await Database.db.one('SELECT * FROM processes');
        expect(true).toBe(false);
    } catch (e) {
        expect(e.name).toBe("SqliteError");
    }

    await Database.db.update();
    expect(await Database.db.all('SELECT * FROM processes')).toEqual([]);
});
