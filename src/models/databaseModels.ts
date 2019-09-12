export interface TimelineRowData {
    time: string,
    type: string,
    value: number,
    offset: number
}

export interface TimelineTypeData {
    rows: TimelineRowData[],
    color: string
}

export interface TimelineData {
    labels: string[],
    types: TimelineTypeData[]
}
