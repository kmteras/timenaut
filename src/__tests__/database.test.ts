import Database from "@/services/database";

beforeEach(async () => {
    const db = new Database();
    await db.connect(true);
});

test.only("Create test database with initial tables", async () => {
    expect.assertions(2);

    // No tables initialized
    try {
        await Database.one('SELECT * FROM processes');
    } catch (e) {
        expect(e.code).toEqual("SQLITE_ERROR");
    }

    await Database.db.update();
    expect(await Database.all('SELECT * FROM processes')).toEqual([]);
});
