import QtQuick 2.2
import QtQuick.Controls 1.0
import Graphs 1.0
import Views 1.0

MainWindow {
    id: main
    objectName: "mainWindow"
    width: 800
    height: 600
    color: "grey"

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
