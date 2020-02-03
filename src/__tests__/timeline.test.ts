import Database from "@/services/database";
import Timeline from "@/services/timeline";
import HeartbeatMock from "@/test/heartbeat_mock";

const db = Database.db;

async function setup(): Promise<HeartbeatMock> {
    await db.update();
    return new HeartbeatMock();
}

test("Test timeline calculates something", async () => {
    const hb = await setup();

    const startDate = new Date("2020-01-01T00:00:00");

    await hb.mockLength(startDate.getTime(), 1, "process", "window");
    const tl = new Timeline();
    let timelineData = await tl.getData(startDate);

    // Float value returned
    expect(timelineData!.datasets[0].data[0]).toBe(1);
});


test("Test process start on one day and end on the other", async () => {
    const hb = await setup();

    const startDate = new Date("2020-01-01T00:00:00");
    const startTime = new Date("2020-01-01T23:50:00");
    const endDate = new Date("2020-01-02T00:00:00");
    const endTime = new Date("2020-01-02T00:10:00");

    await hb.mock(startTime.getTime(), endTime.getTime(), "process", "window");

    const tl = new Timeline();
    let timelineData = await tl.getData(startDate);

    const data: number[] = timelineData!.datasets[0].data;

    // The second to last element should contain no data
    expect(data[data.length - 2]).toBe(0);

    // The second to last element should contain 600 seconds
    expect(data[data.length - 1]).toBe(600);

    const timelineData2 = await tl.getData(endDate);
    const data2: number[] = timelineData2!.datasets[0].data;

    // The first element should contain the remainder of last days tracked time
    expect(data2[0]).toBe(600);

    // No more time should be tracked after that
    expect(data2[1]).toBe(0);
});


test("Test only look at data in lookup timeframe", async () => {
    // TODO
});
