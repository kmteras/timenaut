import DatabaseConversionService from "@/services/database_conversion_service";

test("Test simple two part split", async () => {
    const dcs = new DatabaseConversionService();

    const result = dcs.splitWindowName("SomePage - Chromium");
    expect(result).toEqual(['SomePage', "Chromium"])
});

test("Test three part split", async () => {
    const dcs = new DatabaseConversionService();

    const result = dcs.splitWindowName("SomeTitle - SomePage - Chromium");
    expect(result).toEqual(['SomeTitle', 'SomePage', "Chromium"])
});

test("Test mixed split character title", async () => {
    const dcs = new DatabaseConversionService();

    const result = dcs.splitWindowName("SomeTitle | SomePage - Chromium");
    expect(result).toEqual(['SomeTitle', 'SomePage', "Chromium"]);

    const result2 = dcs.splitWindowName("SomeTitle - SomePage | Chromium");
    expect(result2).toEqual(['SomeTitle', 'SomePage', "Chromium"]);
});
