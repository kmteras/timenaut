<template>
    <svg id="timelineSVG" ref="svg" height="100%" width="100%"></svg>
</template>
<script lang="ts">
    import * as d3 from 'd3';
    import {ipcRenderer} from 'electron';
    import {Component, Prop, Provide, Vue, Watch} from 'vue-property-decorator';

    interface TimelineDataDataset {
        backgroundColor: string,
        label: string,
        data: number[]
    }

    interface TimelineDataLabel {
        time: string
    }

    interface TimelineData {
        datasets: TimelineDataDataset[],
        labels: TimelineDataLabel[]
    }

    @Component
    export default class Timeline extends Vue {
        data: TimelineData = this.getTimelineData();
        @Prop() date?: Date;

        margin: number = 30;

        width: number = 0;
        height: number = 0;

        svg: any;

        mounted() {
            // @ts-ignore
            this.width = this.$refs.svg.clientWidth;
            // @ts-ignore
            this.height = this.$refs.svg.clientHeight;

            console.log(this.getTimelineData());

            this.drawChart(true);
        }

        update(): any {
            // TODO: update graph somehow so it does not refresh everything
            // TODO: if this tab is in focus
            // this.data = this.getTimelineData();
            // this.drawChart(false);
        }

        drawChart(animation: boolean) {
            let svgWidth = this.width - 2 * this.margin;
            let svgHeight = this.height - 2 * this.margin;

            let dat = this.data.datasets[0];

            this.svg = d3.select('#timelineSVG')
                .append("g")
                .attr("transform", `translate(${this.margin}, ${this.margin})`);

            let x = d3.scaleTime()
                .domain([this.startDate(), this.endDate()])
                .range([0, svgWidth]);

            let y = d3.scaleLinear()
                .domain([0, 600])
                .range([svgHeight, 0]);

            console.log(dat.data);

            let histogram = d3.histogram()
                .value((d) => {return d})(dat.data);

            let xAxis = d3.axisBottom(x)
                .ticks(24)
                // @ts-ignore
                .tickFormat(d3.timeFormat("%H:%M"));

            this.svg.append("g")
                .attr('transform', `translate(0, ${svgHeight})`)
                .call(xAxis)
                .selectAll("text")
                    .attr("transform", "rotate(-45)")
                    .attr("dx", "-2em")
                    .attr("dy", "0.2em");

            let yAxis = d3.axisLeft(y)
                .ticks(6);

            this.svg.append("g")
                .call(yAxis);

            this.svg.selectAll("rect")
                .data(histogram)
                .enter()
                .append("rect")
                    .attr("x", 1)
                    .attr('transform', (d: any, i: any) => { console.log(d, i); return `translate(${i * 30}, 0)`})
                    .attr('width', 10)
                    .attr('height', 100)
                    .style('fill', this.data.datasets[0].backgroundColor);
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
