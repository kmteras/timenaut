import Database from "@/services/database";

beforeEach(async () => {
    const tables = await Database.db.all("SELECT name FROM sqlite_master WHERE type='table'");
    for (let table of tables) {
        await Database.db.run("DROP TABLE IF EXISTS ?", [table]);
    }
});

test.only("Create test database with initial tables", async () => {
    // No tables initialized
    try {
        await Database.db.one('SELECT * FROM processes');
        expect(true).toBe(false);
    } catch (e) {
        expect(e.name).toEqual("SqliteError");
    }


    await Database.db.update();
    expect(await Database.db.all('SELECT * FROM processes')).toEqual([]);
});
