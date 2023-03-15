/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  listApi: '/myapp/index/order/list',
  createApi: '/myapp/index/order/create',
  cancelOrderApi: '/myapp/index/order/cancel_order',
  delayApi: '/myapp/index/order/delay'
}

/**
 * 列表
 */
export const listApi = function (params) {
  return axios({
    url: api.listApi,
    method: 'get',
    params: params
  })
}

/**
 * 新建
 */
export const createApi = function (data) {
  return axios({
    url: api.createApi,
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data;charset=utf-8'
    },
    data: data
  })
}

/**
 * 取消
 */
export const cancelOrderApi = function (params) {
  return axios({
    url: api.cancelOrderApi,
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data;charset=utf-8'
    },
    params: params,
  })
}
/**
 * 延期
 */
export const delayApi = function (params, data) {
  return axios({
    url: api.delayApi,
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data;charset=utf-8'
    },
    params: params,
    data: data
  })
}
