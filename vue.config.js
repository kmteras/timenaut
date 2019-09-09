module.exports = {
    pluginOptions: {
        electronBuilder: {
            externals: ['better-sqlite3'],
            mainProcessWatch: ['src/**/*.ts', 'src/**/*.vue'],
            builderOptions: {
                productName: "Timenaut",
                appId: "io.timechart.timenaut",
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
