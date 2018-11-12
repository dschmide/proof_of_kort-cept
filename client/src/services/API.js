import axios from 'axios'
import store from '@/store/store'


export default () => {
  var service = {
    baseURL: '/api/kort-cept/',
    headers: {}
  }
  if (store.state.token !== null) {
    service.headers.Authorization = `JWT ${store.state.token}`;
  }
  return axios.create(service);
}
