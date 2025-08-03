import util from '@utils/util';

App({
	onLaunch(options) {
		console.info("App 启动参数", options, util.info, util.device)

		this.autoUpdate();
		this.setCaptureListener();
		this.loadFonts();
		this.loadSDK();
	},

	autoUpdate() { // 更新小程序
		const updateManager = wx.getUpdateManager();
		updateManager.onCheckForUpdate(res => {
			if (res.hasUpdate) {
				updateManager.onUpdateReady(() => {
					updateManager.applyUpdate();
				})
				updateManager.onUpdateFailed(() => {
					wx.showModal({
						title: '已经有新版本了哟~',
						content: '请您重新打开当前小程序哟~',
						showCancel: false,
					})
				})
			}
		})
	},

	setCaptureListener() { // 监听截屏事件
		wx.onUserCaptureScreen(() => {
			return {
				'query': "from=capture",
				'promise': new Promise(resolve => {
					const pages = getCurrentPages();
					const currentPage = pages[pages.length - 1]; // 当前页面
					const query = currentPage.options
						.map(([key, value]) => `${key}=${value}`)
						.join('&');
					util.showInfo("您已截屏\n请注意隐私安全")
					resolve({
						'query': `${query}&from=capture`,
					})
				})
			}
		})
		wx.onScreenRecordingStateChanged(res => {
			if (res.state == 'start')
				util.showInfo("您正在录屏\n请注意隐私安全", "none", false, 6)
			if (res.state == 'stop')
				util.showInfo("录屏完成\n请注意隐私安全")
		})
	},

	onPageNotFound() { // 页面不存在
		wx.redirectTo({
			url: '/pages/home/home',
		})
	},

	loadFonts() { // 加载字体
		wx.loadFontFace({
			global: true,
			family: 'MyFont',
			source: 'url("https://cdn.micono.eu.org/fonts/微软雅黑.ttf")',
			scopes: ['webview', 'native'],
		});
	},

	loadSDK() { // 加载数据统计 SDK
		if (util.device.platform != "devtools") {
			const sdk = require('@utils/sdk/mtj-wx-sdk')
		}
	},
})