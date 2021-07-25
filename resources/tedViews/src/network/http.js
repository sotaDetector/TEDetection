import { request } from './axios'
// 封装的post get 方法
// postJsonRequest--RequestBody
export const postJsonRequest = (url, params) => {
  return request({
    method: 'post',
    url: url,
    data: params,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
// postRequest--new formData--上传文件的格式
export const postRequest2 = (url, params) => {
  return request({
    method: 'post',
    url: url,
    data: params,
    transformRequest: [function (data1) {
      let data = data1;
      if (typeof data1 == "string") {
        data = JSON.parse(data1);
      }
      return data;
    }],
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}
// postRequest--formData
export const postRequest = (url, params) => {
  return request({
    method: 'post',
    url: url,
    data: params,
    transformRequest: [function (data) {
      let ret = ''
      for (let it in data) {
        ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      }
      return ret
    }],
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
}
// getRequest  
export const getRequest = (url, data = '') => {
  return request({
    method: 'get',
    params: data,
    url: url,
  });
}