import QtQuick 2.2
import QtQuick.Controls 1.0
import Graphs 1.0
import Views 1.0

DashboardViewBase {
    id: dashboard
    Rectangle {
        id: timePanel
        width: parent.width
        height: 40
        x: 0
        y: 0

        Text {
            x: 5
            y: 5

            text: dashboard.date
        }

        Button {
            x: main.width - 200
            height: 30
            width: 40
            text: "<"
            onClicked: dashboard.prev_day()
        }

        Button {
            x: main.width - 150
            height: 30
            width: 40
            text: ">"
            onClicked: dashboard.next_day()
        }
    }

    Rectangle {
        id: panel2
        radius: 10
        width: viewArea.width
        height: 210
        color: "white"
        y: 40

        TimelineGraph {
            id: timelineGraph
            objectName: "timelineGraph"
            width: panel2.width
            height: panel2.height
        }
    }

    Rectangle {
        id: panel
        y: 260
        radius: 10
        width: main.width / 2
        height: main.height - 280
        color: "white"

        PieGraph {
            id: pieGraph
            objectName: "pieGraph"
            width: parent.width
            height: Math.min(parent.height, parent.width / 1.7)
        }
    }

    Rectangle {
        id: panel3
        x: panel.width + 10
        y: 260
        radius: 10
        width: main.width - panel.width - 110
        height: main.height - 280
        color: "white"

        BarGraph {
            id: barGraph
            objectName: "barGraph"
            x: 10
            width: parent.width - 20
            height: parent.height
        }
    }
}
