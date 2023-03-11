/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  listApi: '/myapp/index/thing/list',
  detailApi: '/myapp/index/thing/detail',
  addWishUserApi: '/myapp/index/thing/addWishUser',
  removeWishUserApi: '/myapp/index/thing/removeWishUser',
  getWishThingListApi: '/myapp/index/thing/getWishThingList',
  addCollectUserApi: '/myapp/index/thing/addCollectUser',
  removeCollectUserApi: '/myapp/index/thing/removeCollectUser',
  getCollectThingListApi: '/myapp/index/thing/getCollectThingList',
  // increaseRecommendCountApi: '/myapp/index/thing/increaseRecommendCount',
}

/**
 * list
 */
export const listApi = function (data) {
  return axios({
    url: api.listApi,
    method: 'get',
    params: data
  })
}
/**
 * detail
 */
export const detailApi = function (data) {
  return axios({
    url: api.detailApi,
    method: 'get',
    params: data
  })
}

export const addWishUserApi = function (data) {
  return axios({
    url: api.addWishUserApi,
    method: 'post',
    params: data
  })
}

export const removeWishUserApi = function (data) {
  return axios({
    url: api.removeWishUserApi,
    method: 'post',
    params: data
  })
}

export const getWishThingListApi = function (params) {
  return axios({
    url: api.getWishThingListApi,
    method: 'get',
    params: params
  })
}

export const addCollectUserApi = function (data) {
  return axios({
    url: api.addCollectUserApi,
    method: 'post',
    params: data
  })
}

export const removeCollectUserApi = function (data) {
  return axios({
    url: api.removeCollectUserApi,
    method: 'post',
    params: data
  })
}

export const getCollectThingListApi = function (params) {
  return axios({
    url: api.getCollectThingListApi,
    method: 'get',
    params: params
  })
}

// export const increaseRecommendCountApi = function (data) {
//   return axios({
//     url: api.increaseRecommendCountApi,
//     method: 'post',
//     params: data
//   })
// }
