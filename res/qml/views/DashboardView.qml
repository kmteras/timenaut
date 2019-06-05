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
        width: main.width / 2 + 100
        height: main.height - 240
        color: "white"

        PieGraph {
            id: pieGraph
            objectName: "pieGraph"
            width: Math.min(parent.height, parent.width / 2)
            height: Math.min(parent.height, parent.width / 2)
        }

        BarGraph {
            id: barGraph
            objectName: "barGraph"
            x: parent.width / 2
            width: parent.width / 2 - 10
            height: parent.width / 2
        }
    }
}
