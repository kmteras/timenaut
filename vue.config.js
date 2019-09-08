module.exports = {
    pluginOptions: {
        electronBuilder: {
            mainProcessWatch: ['src/**/*.ts', 'src/**/*.vue'],
            builderOptions: {
                externals: ['better-sqlite3'],
                productName: "Timechart",
                appId: "io.timechart.timechart",
                linux: {
                    category: "Utility",
                    icon: "build/icons/",
                    target: ["AppImage"]
                },
                fileAssociations: [
                    {
                        ext: "icon",
                        icon: "icons/"
                    }
                ],
                snap: {
                    confinement: "classic"
                },
                publish: {
                    provider: "spaces",
                    name: "timenaut",
                    region: "fra1",
                    path: "timenaut"
                }
            }
        }
    }
};
