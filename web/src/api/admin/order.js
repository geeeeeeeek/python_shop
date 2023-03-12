/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  listApi: '/myapp/admin/order/list',
  createApi: '/myapp/admin/order/create',
  cancelOrderApi: '/myapp/admin/order/cancel_order',
  deleteApi: '/myapp/admin/order/delete',
  updateApi: '/myapp/admin/order/update',
  delayApi: '/myapp/admin/order/delay'
}

/**
 * 列表
 */
export const listApi = function (data) {
  return axios({
    url: api.listApi,
    method: 'get',
    params: data
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
 * 删除
 */
export const deleteApi = function (params) {
  return axios({
    url: api.deleteApi,
    method: 'post',
    params: params
  })
}
/**
 * 更新
 */
export const updateApi = function (params, data) {
  return axios({
    url: api.updateApi,
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data;charset=utf-8'
    },
    params: params,
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
    params: params
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
