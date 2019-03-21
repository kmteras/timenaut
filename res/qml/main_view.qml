import QtQuick 2.2
import QtQuick.Controls 1.0
import QtGraphicalEffects 1.0
import Graphs 1.0
import Views 1.0
import "qrc:/qml/fragments"
import "qrc:/qml/views"

MainWindow {
    id: main
    objectName: "mainWindow"
    width: 800
    height: 600

    minimumWidth: 800
    minimumHeight: 600

    color: "#D9D9D9"

    Component.onCompleted: main.ready()

    FontLoader {
        id: logoFont
        source: "qrc:/font/Slabo13px-Regular.ttf"
    }

    Rectangle {
        id: viewArea

        x: 90
        y: 10

        width: main.width - 100
        height: main.height - 20
        color: "transparent"

        DashboardView {
            id: dashboardView
            visible: false
        }

        ActivityView {
            id: activityView
        }

        SettingsView {
            id: settingsView
            visible: false
        }
    }

    Navigation {
        closedSize: 80
        openSize: 200
    }
 }
