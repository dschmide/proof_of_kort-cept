import Api from '@/services/API'

export default {
  getUserAttributes() {
    return Api().get('/api/user_attributes/')
  },
  newUser(UserAttributes) {
    return Api().post('/api/user_attributes/', UserAttributes)
  },
  deleteUserAttributes(id) {
    return Api().delete('/api/user_attributes/' + id + '/')
  },
  updateUserAttributes(UserAttributes, id) {
    return Api().put('/api/user_attributes/' + id + '/', UserAttributes)
  },
}
