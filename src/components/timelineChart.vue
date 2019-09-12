<template>
    <svg id="timelineSVG" ref="svg" height="100%" width="100%"></svg>
</template>
<script lang="ts">
    import * as d3 from 'd3';
    import {ipcRenderer} from 'electron';
    import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
    import {TimelineData, TimelineRowData, TimelineTypeData} from "@/models/databaseModels";

    @Component
    export default class Timeline extends Vue {
        data: TimelineData = this.getTimelineData();
        @Prop() date?: Date;

        margin: number = 30;

        width: number = 0;
        height: number = 0;

        svgWidth: number = 0;
        svgHeight: number = 0;

        svg: any;
        tooltip: any;

        x: any;
        y: any;

        groups: any;

        mounted() {
            // @ts-ignore
            this.width = this.$refs.svg.clientWidth;
            // @ts-ignore
            this.height = this.$refs.svg.clientHeight;

            this.svgWidth = this.width - 2 * this.margin;
            this.svgHeight = this.height - 2 * this.margin;

            this.svg = d3.select('#timelineSVG')
                .append("g")
                .attr("transform", `translate(${this.margin}, ${this.margin})`);

            this.createAxis();
            this.createTooltip();
            this.drawChart();
        }

        update(): any {
            // TODO: update graph somehow so it does not refresh everything
            // TODO: if this tab is in focus
            this.data = this.getTimelineData();
            this.groups.selectAll(".bar")
                .remove();

            this.groups.remove();

            this.drawChart();
        }

        createAxis() {
            this.x = d3.scaleBand()
                .domain(this.data.labels)
                .range([0, this.svgWidth])
                .paddingInner(0.2);

            this.y = d3.scaleLinear()
                .domain([0, 600])
                .range([this.svgHeight, 0]);

            let xAxis = d3.axisBottom(this.x)
            // @ts-ignore
                .tickValues(this.x.domain().filter((value: string, i: number) => {
                    return !(i % 6)
                }));

            this.svg.append("g")
                .attr('transform', `translate(0, ${this.svgHeight})`)
                .call(xAxis)
                .selectAll("text")
                .attr("transform", "rotate(-45)")
                .attr("dx", "-2em")
                .attr("dy", "0.2em");

            let yAxis = d3.axisLeft(this.y)
                .ticks(6);

            this.svg.append("g")
                .call(yAxis);
        }

        drawChart() {
            this.groups = this.svg.selectAll(".type")
                .data(this.data.types)
                .enter()
                .append("g")
                .style('fill', (d: TimelineTypeData) => {
                    return d.color
                });

            this.groups.selectAll(".bar")
                .data((d: TimelineTypeData): TimelineRowData[] => {
                    return d.rows
                })
                .enter()
                .append("rect")
                .attr("x", (d: TimelineRowData) => {
                    return this.x(d.time)
                })
                .attr("y", (d: TimelineRowData) => {
                    return this.y(d.value + d.offset)
                })
                .attr('width', this.x.bandwidth())
                .attr('height', (d: TimelineRowData) => {
                    return this.svgHeight - this.y(d.value)
                })
                .on('mouseover', () => {
                    this.tooltip.style('display', null)
                });
        }

        createTooltip() {
            this.tooltip = this.svg.append("g")
                .attr("class", "tooltip")
                .style("display", "none");

            this.tooltip.append("rect")
                .attr("width", 30)
                .attr("height", 20)
                .attr("fill", "white")
                .style("opacity", 0.5);

            this.tooltip.append("text")
                .attr("x", 15)
                .attr("dy", "1.2em")
                .style("text-anchor", "middle")
                .attr("font-size", "12px")
                .attr("font-weight", "bold");
        }

        startDate() {
            let date = new Date();
            date.setHours(0);
            date.setMinutes(0);
            date.setSeconds(0);
            return date;
        }

        endDate() {
            let date = new Date();
            date.setHours(23);
            date.setMinutes(59);
            date.setSeconds(59);
            return date;
        }

        getTimelineData(): TimelineData {
            return ipcRenderer.sendSync('get-timeline-data', this.date!.getTime());
        }

        @Watch("date")
        onDateChange() {
            this.update()
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
