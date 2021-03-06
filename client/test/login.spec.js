import LoginComp from '../src/components/Login.vue'

// Here are some Jasmine 2.0 tests, though you can
// use any test runner / assertion library combo you prefer
describe('LoginComp', () => {
  // Evaluate the results of functions in
  // the raw component options
  it('checks if component is mounted and the correct default data is set', () => {
    expect(typeof LoginComp.data).toBe('function')
    const defaultData = LoginComp.data()
    expect(defaultData.password).toBe('')
    expect(defaultData.displayname).toBe('')
    expect(defaultData.email).toBe('')
  })
})
