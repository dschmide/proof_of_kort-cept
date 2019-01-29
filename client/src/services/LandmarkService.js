import Api from '@/services/API'

export default {
  getAllLandmarks() {
    return Api().get('/api/placed_landmarks/')
  },
  async newLandmark(LandmarkAttributes) {
    return Api().post('/api/placed_landmarks/', LandmarkAttributes)
  },
  deleteTower(id) {
    return Api().delete('/api/placed_landmarks/' + id + '/')
  },
  updateTower(LandmarkAttributes, id) {
    return Api().put('/api/placed_landmarks/' + id + '/', LandmarkAttributes)
  },
}
