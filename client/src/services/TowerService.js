import Api from '@/services/API'

export default {
  getMyTowers() {
    return Api().get('/api/placed_towers/')
  },
  newTower(TowerAttributes) {
    return Api().post('/api/placed_towers/', TowerAttributes)
  },
  deleteTower(id) {
    return Api().delete('/api/placed_towers/' + id + '/')
  },
  updateTower(TowerAttributes, id) {
    return Api().put('/api/placed_towers/' + id + '/', TowerAttributes)
  },
}
