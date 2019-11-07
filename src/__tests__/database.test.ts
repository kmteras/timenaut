import Database from "@/services/database";

test("Create Test Database", () => {
    let db = new Database();
    db.connect(true);
});
