import Api from '@/services/API'

export default {
  postMission(theSolvedMission) {
    return Api().post('/api/solved_mission/', theSolvedMission)
  },
}
