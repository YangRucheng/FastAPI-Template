import config from './config';
import util from './util';

const checkError = err => {}
const checkRes = res => {}

class HTTP {
	static __request = (...args) => {
		if (args[0].showLoading !== false) util.showLoading("请稍候");
		return new Promise((resolve, reject) => {
			let url = args[0].url;
			if (!url.startsWith('http')) url = `${config.baseUrl}${url}`;
			wx.request({
				...args[0],
				'url': url,
				success: res => {
					checkRes(res);
					console.debug(`请求 ${args[0].url.split('?')[0]}`, res.data, args[0]);
					resolve(res.data);
				},
				fail: err => {
					checkError(err);
					reject(err);
				},
				complete: () => {
					util.hideLoading();
				},
			})
		})
	}

	static get = async (...args) => await this.__request({
		...args[0],
		'method': "GET",
		'data': args[0].params || {},
	})

	static post = async (...args) => {
		const query = Object.entries(args[0].params || {})
			.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
			.join('&');
		return await this.__request({
			...args[0],
			'method': "POST",
			'url': `${args[0].url}?${query}`,
			'data': args[0].body || {},
		})
	}
}

module.exports = HTTP;