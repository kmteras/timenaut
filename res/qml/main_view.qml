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
    height: 480
    title: "Timechart"

    minimumWidth: 800
    minimumHeight: 480

    color: "#D9D9D9"

    Component.onCompleted: main.ready()

    FontLoader {
        id: logoFont
        source: "qrc:/font/Slabo13px-Regular.ttf"
    }

    FontLoader {
        id: font
        source: "qrc:/font/Montserrat-Regular.ttf"
    }

    Rectangle {
        id: viewArea

        // 720 (700) x 600 (580)

        x: 80
        y: 0

        width: main.width - 100
        height: main.height - 20
        color: "transparent"

        DashboardView {
            id: dashboardView
        }

        ActivityView {
            id: activityView
            visible: false
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
