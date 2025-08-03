/**
 * 基本工具
 * 不依赖其它代码
 */

const VESION = "v1"

/**
 * 写入缓存
 * @param {string} key 
 * @param {object} value 
 */
const setStorage = (key, value) => {
	wx.setStorageSync(`${VESION}.${key}`, value)
}

/**
 * 读取缓存
 * @param {string} key 
 * @param {*} defaultValue
 */
const getStorage = (key, defaultValue = null) => {
	const value = wx.getStorageSync(`${VESION}.${key}`);
	if (value === '')
		return defaultValue;
	return value;
}

/**
 * 显示 Loading
 * @param {*} msg 
 */
const showLoading = (msg) => {
	wx.showLoading({
		title: msg,
		mask: true,
	})
}

/**
 * 隐藏 Loading
 */
const hideLoading = () => {
	wx.hideLoading({
		noConflict: true,
	});
}

/**
 * 提示信息
 * @param {*} msg 
 * @param {*} icon 
 * @param {*} mask 
 * @param {*} duration 
 */
const showInfo = (msg, icon = "none", mask = false, duration = 1.5) => {
	wx.showToast({
		'title': msg,
		'mask': mask,
		'icon': icon,
		'duration': duration * 1000,
	})
}

/**
 * 返回上一个页面
 */
const back = () => {
	const pages = getCurrentPages();
	if (pages.length > 1)
		wx.navigateBack()
	else
		wx.reLaunch({
			url: '/pages/home/home',
		})
}

module.exports = {
	setStorage,
	getStorage,
	info: wx.getAccountInfoSync(),
	device: wx.getDeviceInfo(),
	showLoading,
	hideLoading,
	showInfo,
	back,
}