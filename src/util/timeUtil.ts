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
