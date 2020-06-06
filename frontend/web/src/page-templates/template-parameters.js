const themeColor = '#000000';
const webAppCapable = 'no';
const webAppTitle = 'Home Automation Network';
const startUrl = '/';

module.exports = {
    defaultTitle: 'Home Automation Network',
    appMountId: 'app-root',
    charset: 'utf-8',
    viewport: 'width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no',
    description: '',
    androidMeta: {
        themeColor,
        androidMeta: webAppCapable,
    },
    iOSMeta: {
        mobileWebAppTitle: webAppTitle,
        mobileWebAppCapable: webAppCapable,
        mobileWebAppStatusBarStyle: themeColor,
    },
    windowsMeta: {
        navbuttonColor: themeColor,
        tileColor: themeColor,
        tileImage: '',
        config: '',
    },
    pinnedSitesMeta: {
        applicationName: webAppTitle,
        toolTip: webAppTitle,
        startUrl: startUrl,
    },
};
