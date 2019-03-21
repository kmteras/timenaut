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
        width: 500
        height: 600
        color: "white"

        PieGraph {
            id: pieGraph
            objectName: "pieGraph"
            width: 200
            height: 200
        }

        BarGraph {
            id: barGraph
            objectName: "barGraph"
            x: 200
            width: 400
            height: 200
        }
    }
}
