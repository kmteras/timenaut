const path = require('path');

module.exports = {
    pluginOptions: {
        electronBuilder: {
            chainWebpackMainProcess: chainWebpackMainProcess,
            externals: ['sqlite3'],
            mainProcessWatch: ['src/**/*.ts', 'src/**/*.vue'],
            builderOptions: {
                productName: "Timenaut",
                appId: "app.timenaut.timenaut",
                afterSign: "build/afterSignHook.js",
                linux: {
                    category: "Utility",
                    icon: "build/icons/",
                    target: ["AppImage"]
                },
                mac: {
                    hardenedRuntime: true,
                    entitlements: "build/timenaut.entitlements"
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
                    provider: "github",
                    owner: "kmteras",
                    repo: "timenaut",
                    vPrefixedTagName: true
                }
            }
        }
    }
};

function chainWebpackMainProcess(config) {
    config.resolve.alias.set('@', path.join(__dirname, 'src'))
}
