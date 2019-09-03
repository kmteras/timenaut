module.exports = {
    pluginOptions: {
        electronBuilder: {
            mainProcessWatch: ['src/**/*.ts', 'src/**/*.vue'],
            builderOptions: {
                productName: "Timechart",
                appId: "io.timechart.timechart",
                linux: {
                    category: "Utility",
                    icon: "build/icons/"
                },
                fileAssociations: [
                    {
                        ext: "icon",
                        icon: "icons/"
                    }
                ],
                snap: {
                    confinement: "classic"
                }
            }
        }
    }
};
