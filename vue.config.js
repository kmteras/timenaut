module.exports = {
    pluginOptions: {
        electronBuilder: {
            mainProcessWatch: ['src/**/*.ts', 'src/**/*.vue'],
            builderOptions: {
                productName: "Timechart",
                appId: "io.timechart.timechart",
                linux: {
                    category: "Utility"
                },
                fileAssociations: [
                    {
                        ext: "icon",
                        icon: "icons/"
                    }
                ]
            }
        }
    }
};
