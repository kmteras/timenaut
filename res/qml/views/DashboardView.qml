import QtQuick 2.2
import QtQuick.Controls 1.0
import Graphs 1.0
import Views 1.0

DashboardViewBase {
    Rectangle {
        id: panel2
        radius: 10
        width: viewArea.width
        height: 200
        color: "white"

        TimelineGraph {
            id: timelineGraph
            objectName: "timelineGraph"
            width: panel2.width
            height: panel2.height
        }
    }

    Rectangle {
        id: panel
        y: 220
        radius: 10
        width: main.width / 2
        height: main.height - 240
        color: "white"

        PieGraph {
            id: pieGraph
            objectName: "pieGraph"
            width: Math.min(parent.height, parent.width)
            height: Math.min(parent.height, parent.width)
        }
    }

    Rectangle {
        id: panel3
        x: panel.width + 10
        y: 220
        radius: 10
        width: main.width - panel.width - 110
        height: main.height - 240
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
