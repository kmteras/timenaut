export function getPrevDate(date: Date): Date {
    return new Date(date.getTime() - 24 * 60 * 60 * 1000);
}

export function getNextDate(date: Date): Date {
    return new Date(date.getTime() + 24 * 60 * 60 * 1000);
}

export function getToday(): Date {
    let date: Date = new Date();
    date = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    date.setHours(0);
    return date;
}

export function getDayLength(): number {
    return 24 * 60 * 60;
}

export function formatSeconds(totalSeconds: number): string {
    let hours = Math.floor(totalSeconds / 60 / 60);
    let minutes = Math.floor((totalSeconds - hours * 60 * 60) / 60);
    let seconds = totalSeconds - hours * 60 * 60 - minutes * 60;

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
    } else if (minutes > 0) {
        return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
    } else {
        return `00:${seconds.toString().padStart(2, "0")}`
    }
}

export function getDateWithNoTime(date: Date): Date {
    // Simplest but hacky way
    return new Date(date.toISOString().substr(0, 11) + "00:00:00.000Z");
}
